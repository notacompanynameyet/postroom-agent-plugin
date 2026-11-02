# Postroom agent integration package

Development package 0.1.0. Host-specific authenticated acceptance tests are pending. This repository is not evidence of Hermes catalog approval, Gemini app approval or ClawHub publication. Postroom is a product by Not a Company Name Yet, operated by Vardhiva Innovations.

## Hermes Agent

Portable Agent Plugins v1 package: plugin.json, mcp.json and skills. The legacy optional-mcps catalog is closed to new entries; public proposals must use plugin-catalog after validation.

Install and explicitly enable:
```sh
hermes plugins install notacompanynameyet/postroom-agent-plugin --no-enable
hermes plugins enable postroom
```

Portable MCP configuration alone does not enable OAuth. Merge the following native server definition into the active profile's existing config; do not replace other settings:
```yaml
mcp_servers:
  postroom:
    url: https://social.notacompanynameyet.com/mcp
    auth: oauth
    oauth:
      scope: "social.read social.write"
    trust: untrusted
```
```sh
hermes mcp login postroom
hermes chat
```

Hermes owns sign-in, token storage and refresh. Native configuration takes precedence, so keep its untrusted approval gate too. Before catalog submission, run the full validator at the exact proposed commit:
```sh
hermes plugins validate /path/to/postroom-agent-plugin --install-deps
```
Hermes portable admission validation and the security scan passed on 2 November 2026 against upstream e8639fd4312e5102d6f10c76b56406cb01c19092. The catalog structure validator also passed. Fresh Hermes OAuth and tool acceptance tests are still pending. Do not describe this as a Nous-approved catalog plugin.

## Gemini CLI

This is separate from the Gemini app / Search Connected Apps program and does not implement A2A.
```sh
npx --yes @google/gemini-cli@0.66.0 extensions install https://github.com/notacompanynameyet/postroom-agent-plugin
```

Wait for installation to finish. Then open Gemini with a separate command:
```sh
npx --yes @google/gemini-cli@0.66.0
```
Inside the CLI:
```text
/mcp auth postroom
/mcp list
```
The root manifest uses Streamable HTTP and native OAuth discovery/DCR. No API key is embedded. Preserve normal approval prompts. Installation with Gemini CLI 0.66.0 passed on 2 November 2026. The CLI recognized the Postroom skill and MCP server and correctly required authorization. Live OAuth and tool calls remain unverified. Add the gemini-cli-extension discovery topic only after host OAuth/tool tests succeed; gallery validation and listing are not asserted.

## OpenClaw / ClawHub

Publishable skill folder: openclaw/postroom. It documents native OAuth MCP setup.
```sh
clawhub login
clawhub whoami
clawhub skill publish ./openclaw/postroom --slug postroom --name "Postroom" --version 1.0.0
```
Verify the publisher owner and registry scan result. No successful ClawHub upload is asserted.

## Behaviour and disclosures

- Every tool call goes to https://social.notacompanynameyet.com/mcp, as the user's own Postroom workspace.
- Requested account, brand, post, media and analytics results enter the host session and may reach its model provider.
- The hosted tool list can change independently of this package's pinned source.
- Writes can change publishing queues and publish to connected accounts. Show the exact immutable preview and obtain explicit approval first. A connection grant is not post approval.
- Inspect status after uncertain writes; never create another draft as an automatic retry.
- TikTok in this MCP uses inbox upload and requires completion in TikTok. Availability depends on provider permissions.
- No local executables, install scripts, background processes, credential readers or added telemetry are bundled.
- Postroom terms, privacy policy, allowances and provider limits apply. This package grants no billing bypass.

## Microsoft 365 Copilot readiness

This package is not a Microsoft marketplace app package. See Microsoft's MCP plugin guide:
https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/build-mcp-plugins

A compatibility check on 2 November 2026 found a concrete blocker: Microsoft's current DCR authentication requires the authorization server to issue a client secret. Postroom currently advertises only `token_endpoint_auth_methods_supported: ["none"]`. Do not configure the server as unauthenticated to work around this. Implement and review confidential-client support (or an approved static OAuth client flow), validate the tenant OAuth flow, then use Microsoft 365 Agents Toolkit to generate the tenant-specific authentication configuration and app package. Publisher onboarding and marketplace review are separate steps.

Official requirement: https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/plugin-authentication-dynamic-client-registration

## Validation boundary

Passing the portable package validator and installing an extension do not prove a user can complete OAuth or invoke every hosted tool. An end-to-end test must authorize a dedicated workspace, inspect its accounts, save an unscheduled preview, verify it remains unscheduled, and revoke the grant. Any scheduling test requires explicit approval of that exact preview. Do not use a production post as an unapproved test. Gallery discovery remains pending until live client tests are completed.

## OpenClaw downloadable bundle

ClawHub accepts the dedicated Codex-format bundle in `distributions/openclaw/`. This is separate from the root Hermes Agent Plugins package: ClawHub CLI 0.25.0 currently accepts Codex/Claude/Cursor bundle markers, not the root portable Agent Plugins marker.

- Preview bundle ZIP: `downloads/postroom-openclaw-0.1.0.zip`
- Standalone skill ZIP: `downloads/postroom-skill-1.0.0.zip`
- Source-only skill: `openclaw/postroom/SKILL.md`
- Rebuild archives deterministically: `python3 scripts/build-openclaw-bundle.py`

The bundle includes the skill. Users should install either the bundle or standalone skill, not both. Bundles include connection metadata; each user still needs their own Postroom OAuth grant. The standalone skill supplies instructions only.

Validated using ClawHub CLI 0.25.0: package publish preflight/dry-run passed; Plugin Inspector target OpenClaw 2026.10.9 returned pass with zero issues/warnings. This is local preflight, not registry approval or completed live OAuth testing. Upload to ClawHub remains pending.

Publishing from an authorized owner session:
```sh
clawhub package publish ./distributions/openclaw --family bundle-plugin --name @notacompanynameyet/postroom --owner notacompanynameyet --version 0.1.0 --bundle-format codex --host-targets openclaw --wait
```

For the standalone skill, use ClawHub's Skill → Import from GitHub with `openclaw/postroom`, or upload the SKILL.md folder. For the plugin use Plugin → Bundle plugin and the dedicated bundle ZIP. Do not upload the complete multi-platform repository ZIP as the ClawHub plugin.


## Local image upload helper (OpenClaw / terminal hosts)

The content bundle does not execute local code. For hosts where a signed upload URL cannot safely move from an MCP result into a file-transfer tool, the optional standard-library Python helper `scripts/postroom-upload.py` performs the whole transfer inside one local process. It has its own public OAuth/PKCE browser authorization and does not read OpenClaw credentials or change Gateway configuration.

Run `python3 scripts/postroom-upload.py --login --workspace YOUR_WORKSPACE_ID "/absolute/path/to/image.png"`. Select your intended Postroom workspace and publishing access. It verifies workspace identity and uploads only that local image. Publishing media is publicly accessible. It prints the owned media URL, never the signed upload URL, access token or refresh token. OAuth credentials are stored locally in `~/.postroom/image-uploader/oauth.json` (0600 in a 0700 directory). Later runs omit `--login` and refresh credentials when necessary. Revoke its grant in Postroom's assistant-access page when no longer needed.

Supported images: JPEG, PNG and WebP, up to 3 MB. No third-party Python dependencies. Network redirects are refused. The helper does not prepare previews, schedule or publish. Use its media URL in your normal OpenClaw preview and exact-approval flow.

Validation: `python3 -m unittest discover -s tests -p test_local_upload.py -v`. Local mocked transport/security tests pass. Live Mac OAuth, image upload and OpenClaw publication acceptance must still be observed; this helper is not evidence of completed publishing verification.
