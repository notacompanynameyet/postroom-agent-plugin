#!/usr/bin/env python3
"""Upload one local image with Postroom OAuth. Never schedules or publishes."""
import argparse
import base64
import hashlib
import http.server
import json
import os
from pathlib import Path
import secrets
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser

ORIGIN = 'https://social.notacompanynameyet.com'
RESOURCE = ORIGIN + '/mcp'
ISSUER = ORIGIN + '/oauth/agent'
STORAGE = 'craleuctdsfhvmtjcznn.supabase.co'
CACHE = Path.home() / '.postroom' / 'image-uploader' / 'oauth.json'
MAX_BYTES = 3 * 1024 * 1024

class UploadError(Exception):
    pass

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None

def request(url, data=None, headers=None, method=None):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    try:
        with urllib.request.build_opener(NoRedirect).open(req, timeout=60) as response:
            raw = response.read(1024 * 1024)
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as error:
        # Never print an exception containing a credential-bearing URL or body.
        raise UploadError('HTTP %s from %s. No publication was requested.' %
                          (error.code, urllib.parse.urlsplit(url).hostname)) from None
    except (urllib.error.URLError, TimeoutError, ValueError):
        raise UploadError('Network timeout or invalid server response; no publication was requested.') from None

def save_cache(value):
    parent = CACHE.parent
    parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    if parent.is_symlink() or CACHE.is_symlink():
        raise UploadError('Refusing a symlink credential location.')
    os.chmod(parent, 0o700)
    fd, name = tempfile.mkstemp(prefix='.oauth-', dir=parent)
    try:
        with os.fdopen(fd, 'w') as output:
            json.dump(value, output)
        os.replace(name, CACHE)
    finally:
        if os.path.exists(name):
            os.unlink(name)

def load_cache():
    if not CACHE.exists():
        return None
    if CACHE.is_symlink() or CACHE.stat().st_mode & 0o077:
        raise UploadError('Credential file must be a private regular file (mode 600).')
    try:
        return json.loads(CACHE.read_text())
    except (OSError, ValueError):
        raise UploadError('Could not read the local OAuth cache; run again with --login.') from None

def token_request(values):
    return request(ISSUER + '/token', urllib.parse.urlencode(values).encode(),
                   {'Content-Type': 'application/x-www-form-urlencoded'}, 'POST')

def authorize():
    verifier = secrets.token_urlsafe(48)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).decode().rstrip('=')
    state = secrets.token_urlsafe(32)
    result = {}
    class Callback(http.server.BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass
        def do_GET(self):
            query = urllib.parse.urlsplit(self.path)
            values = urllib.parse.parse_qs(query.query)
            valid = query.path == '/callback' and secrets.compare_digest(values.get('state', [''])[0], state)
            if valid and values.get('code'):
                result['code'] = values['code'][0]
            elif valid and values.get('error'):
                result['denied'] = True
            self.send_response(200 if 'code' in result else 400)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(b'Return to Terminal. You may close this tab.')
    with http.server.HTTPServer(('127.0.0.1', 0), Callback) as server:
        server.timeout = 1
        redirect = 'http://127.0.0.1:%s/callback' % server.server_port
        client = request(ISSUER + '/register', json.dumps({
            'client_name': 'Postroom local image uploader',
            'redirect_uris': [redirect], 'token_endpoint_auth_method': 'none'
        }).encode(), {'Content-Type': 'application/json'}, 'POST')
        client_id = client.get('client_id')
        if not isinstance(client_id, str):
            raise UploadError('OAuth client registration failed.')
        url = ISSUER + '/authorize?' + urllib.parse.urlencode({
            'response_type': 'code', 'client_id': client_id,
            'redirect_uri': redirect, 'scope': 'social.read social.write',
            'resource': RESOURCE, 'state': state,
            'code_challenge': challenge, 'code_challenge_method': 'S256'
        })
        print('Opening Postroom sign-in. Select your YET workspace and publishing access.')
        if not webbrowser.open(url):
            raise UploadError('Could not open your browser. No credentials were printed.')
        deadline = time.monotonic() + 180
        while not result and time.monotonic() < deadline:
            server.handle_request()
        if 'code' not in result:
            raise UploadError('Authorization was declined or timed out.')
        token = token_request({'grant_type': 'authorization_code', 'client_id': client_id,
                               'code': result['code'], 'redirect_uri': redirect,
                               'code_verifier': verifier, 'resource': RESOURCE})
    return store_token(token, client_id)

def store_token(token, client_id):
    if not isinstance(token.get('access_token'), str):
        raise UploadError('No OAuth access token was returned.')
    if 'social.write' not in token.get('scope', '').split():
        raise UploadError('Publishing access was not granted. Run --login and select publishing access.')
    value = {**token, 'client_id': client_id,
             'expires_at': time.time() + int(token.get('expires_in', 3600))}
    save_cache(value)
    return value

def credentials(login=False):
    if login:
        return authorize()
    value = load_cache()
    if not value:
        raise UploadError('First run requires --login for browser authorization.')
    if value.get('expires_at', 0) <= time.time() + 60:
        if not value.get('refresh_token'):
            raise UploadError('Sign-in expired. Run again with --login.')
        token = token_request({'grant_type': 'refresh_token', 'client_id': value['client_id'],
                               'refresh_token': value['refresh_token'], 'resource': RESOURCE})
        value = store_token(token, value['client_id'])
    return value

def find(value, field):
    if isinstance(value, dict):
        if field in value:
            return value
        for child in value.values():
            match = find(child, field)
            if match:
                return match
    elif isinstance(value, list):
        for child in value:
            match = find(child, field)
            if match:
                return match
    elif isinstance(value, str):
        try:
            return find(json.loads(value), field)
        except (ValueError, TypeError):
            return None
    return None

def call_tool(token, name, args, field):
    response = request(RESOURCE, json.dumps({'jsonrpc': '2.0', 'id': 1,
                       'method': 'tools/call', 'params': {'name': name, 'arguments': args}}).encode(),
                       {'Content-Type': 'application/json', 'Accept': 'application/json',
                        'Authorization': 'Bearer ' + token}, 'POST')
    if response.get('error') or response.get('result', {}).get('isError'):
        raise UploadError('Postroom rejected ' + name + '. No scheduling was attempted.')
    result = find(response.get('result', {}), field)
    if not result:
        raise UploadError('Missing expected result from ' + name)
    print(name + ': success')
    return result

def image_bytes(path):
    with Path(path).expanduser().open('rb') as image:
        data = image.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise UploadError('Image exceeds the current 3 MB limit.')
    if data.startswith(b'\x89PNG\r\n\x1a\n'):
        return data, 'image/png'
    if data.startswith(b'\xff\xd8\xff'):
        return data, 'image/jpeg'
    if data[:4] == b'RIFF' and data[8:12] == b'WEBP':
        return data, 'image/webp'
    raise UploadError('Use a PNG, JPEG or WebP file.')

def upload(path, token):
    data, mime = image_bytes(path)
    ticket = call_tool(token, 'yet_create_image_upload', {'mime_type': mime}, 'upload_url')
    parsed = urllib.parse.urlsplit(ticket['upload_url'])
    jwt = urllib.parse.parse_qs(parsed.query).get('token', [''])[0]
    expected = '/storage/v1/object/upload/sign/social-media/'
    if (parsed.scheme != 'https' or parsed.hostname != STORAGE or parsed.port
            or parsed.username or parsed.password or parsed.fragment
            or not parsed.path.startswith(expected) or len(jwt.split('.')) != 3):
        raise UploadError('Unexpected or redacted upload destination; transfer stopped.')
    request(ticket['upload_url'], data, {'Content-Type': mime}, 'PUT')
    print('Image transfer: success')
    done = call_tool(token, 'yet_complete_image_upload', {'upload_id': ticket['upload_id']}, 'media_url')
    print('UPLOAD COMPLETE')
    print('media_url: ' + done['media_url'])
    print('Nothing scheduled or published.')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('image', help='Path to the image selected for publishing')
    parser.add_argument('--login', action='store_true', help='Authorize this local uploader in your browser')
    parser.add_argument('--workspace', help='Stop before upload unless the signed-in workspace ID matches')
    args = parser.parse_args()
    # Validate the file before creating an OAuth client or making any network call.
    image_bytes(args.image)
    value = credentials(args.login)
    profile = call_tool(value['access_token'], 'yet_profile', {}, 'id')
    if args.workspace and profile['id'] != args.workspace:
        raise UploadError('Wrong workspace selected. Run --login and select the intended workspace.')
    print('Workspace: ' + str(profile.get('name', profile['id'])))
    upload(args.image, value['access_token'])

if __name__ == '__main__':
    try:
        main()
    except (UploadError, OSError) as error:
        print('STOPPED: ' + (str(error) if isinstance(error, UploadError) else type(error).__name__))
        raise SystemExit(1)

