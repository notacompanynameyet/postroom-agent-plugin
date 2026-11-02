import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('uploader', Path(__file__).parents[1] / 'scripts/postroom-upload.py')
u = importlib.util.module_from_spec(spec)
spec.loader.exec_module(u)

class UploadTests(unittest.TestCase):
    def test_upload_keeps_credentials_in_process_and_never_schedules(self):
        with tempfile.TemporaryDirectory() as folder:
            image = Path(folder) / 'image.png'
            image.write_bytes(b'\x89PNG\r\n\x1a\n\x00')
            url = 'https://' + u.STORAGE + '/storage/v1/object/upload/sign/social-media/owner/file?token=header.payload.signature'
            calls = []
            def network(destination, data=None, headers=None, method=None):
                calls.append((destination, data, headers, method))
                if destination == url:
                    self.assertEqual(data, image.read_bytes())
                    self.assertEqual(headers, {'Content-Type': 'image/png'})
                    return {}
                body = json.loads(data)
                name = body['params']['name']
                if name == 'yet_create_image_upload':
                    value = {'upload_id': 'upload-id', 'upload_url': url}
                else:
                    self.assertEqual(name, 'yet_complete_image_upload')
                    self.assertEqual(body['params']['arguments'], {'upload_id': 'upload-id'})
                    value = {'media_url': 'https://' + u.STORAGE + '/storage/v1/object/public/social-media/owner/image.png'}
                return {'result': {'content': [{'type': 'text', 'text': json.dumps(value)}]}}
            output = io.StringIO()
            with patch.object(u, 'request', network), contextlib.redirect_stdout(output):
                u.upload(image, 'oauth-private-secret')
            self.assertEqual(len(calls), 3)
            self.assertNotIn('oauth-private-secret', output.getvalue())
            self.assertNotIn('header.payload.signature', output.getvalue())
            self.assertIn('UPLOAD COMPLETE', output.getvalue())

    def test_redacted_or_foreign_destination_stops_before_transfer(self):
        with tempfile.TemporaryDirectory() as folder:
            image = Path(folder) / 'image.png'
            image.write_bytes(b'\x89PNG\r\n\x1a\n\x00')
            for url in ['https://attacker.example/upload?token=a.b.c',
                        'https://' + u.STORAGE + '/storage/v1/object/upload/sign/social-media/file?token=REDACTED']:
                with patch.object(u, 'call_tool', return_value={'upload_url': url}), patch.object(u, 'request') as network:
                    with self.assertRaises(u.UploadError):
                        u.upload(image, 'private')
                    network.assert_not_called()

    def test_private_cache_and_explicit_write_permission(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(u, 'CACHE', Path(folder) / 'private/oauth.json'):
            with self.assertRaises(u.UploadError):
                u.store_token({'access_token': 'x', 'scope': 'social.read'}, 'client')
            u.store_token({'access_token': 'private', 'scope': 'social.read social.write'}, 'client')
            self.assertEqual(u.CACHE.stat().st_mode & 0o777, 0o600)
            self.assertEqual(u.CACHE.parent.stat().st_mode & 0o777, 0o700)
            self.assertEqual(u.load_cache()['client_id'], 'client')

    def test_invalid_and_oversized_files_are_rejected_locally(self):
        with tempfile.TemporaryDirectory() as folder:
            image = Path(folder) / 'image.png'
            for data in [b'<svg/>', b'\x89PNG\r\n\x1a\n' + b'0' * u.MAX_BYTES]:
                image.write_bytes(data)
                with self.assertRaises(u.UploadError):
                    u.image_bytes(image)

if __name__ == '__main__':
    unittest.main()
