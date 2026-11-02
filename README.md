# Postroom agent integration package

Multi-host integration package. OpenClaw Bluesky image automation passed a live test on 2 November 2026; Hermes catalog review and live OAuth testing, and Gemini/Antigravity verification remain pending. Postroom is a product by Not a Company Name Yet, operated by Vardhiva Innovations.

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

The plugin and standalone skill are published on ClawHub:
- https://clawhub.ai/notacompanynameyet/plugins/postroom
- https://clawhub.ai/notacompanynameyet/postroom

Updated source releases: OpenClaw bundle **0.1.1** and standalone skill **1.0.1**. Registry publication is a separate step; check the version displayed on ClawHub before installing. Both include the automatic image uploader and use one native OAuth MCP connection instead of bundled HTTP metadata, avoiding the OpenClaw 2026.9.6 Codex cwd issue.

Read [the installation and automation guide](distributions/openclaw/README.md).

## Behaviour and disclosures

- Every tool call goes to https://social.notacompanynameyet.com/mcp, as the user's own Postroom workspace.
- Requested account, brand, post, media and analytics results enter the host session and may reach its model provider.
- The hosted tool list can change independently of this package's pinned source.
- Writes can change publishing queues and publish to connected accounts. Show the exact immutable preview and obtain explicit approval first. A connection grant is not post approval.
- Inspect status after uncertain writes; never create another draft as an automatic retry.
- TikTok in this MCP uses inbox upload and requires completion in TikTok. Availability depends on provider permissions.
- The root Hermes portable package has no executable hooks. OpenClaw distributions include an explicitly invoked Python image uploader; no install hooks, background processes or added telemetry. It stores only its own OAuth grant, never reads host credentials.
- Postroom terms, privacy policy, allowances and provider limits apply. This package grants no billing bypass.

## Microsoft 365 Copilot readiness

This package is not a Microsoft marketplace app package. See Microsoft's MCP plugin guide:
https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/build-mcp-plugins

A compatibility check on 2 November 2026 found a concrete blocker: Microsoft's current DCR authentication requires the authorization server to issue a client secret. Postroom currently advertises only `token_endpoint_auth_methods_supported: ["none"]`. Do not configure the server as unauthenticated to work around this. Implement and review confidential-client support (or an approved static OAuth client flow), validate the tenant OAuth flow, then use Microsoft 365 Agents Toolkit to generate the tenant-specific authentication configuration and app package. Publisher onboarding and marketplace review are separate steps.

Official requirement: https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/plugin-authentication-dynamic-client-registration

## Validation boundary

Passing the portable package validator and installing an extension do not prove a user can complete OAuth or invoke every hosted tool. An end-to-end test must authorize a dedicated workspace, inspect its accounts, save an unscheduled preview, verify it remains unscheduled, and revoke the grant. Any scheduling test requires explicit approval of that exact preview. Do not use a production post as an unapproved test. Gallery discovery remains pending until live client tests are completed.

## Build and publish OpenClaw releases

- Bundle: `downloads/postroom-openclaw-0.1.1.zip`
- Standalone skill: `downloads/postroom-skill-1.0.1.zip`
- Rebuild: `python3 scripts/build-openclaw-bundle.py`
- Validate: `python3 -m unittest discover -s tests -v`

Publish the dedicated bundle directory, not the complete multi-host repository:

```sh
clawhub package publish ./distributions/openclaw --family bundle-plugin --name @notacompanynameyet/postroom --owner notacompanynameyet --version 0.1.1 --bundle-format codex --host-targets openclaw --wait
clawhub skill publish ./openclaw/postroom --slug postroom --name "Postroom" --version 1.0.1
```

Both commands require the intended publisher's ClawHub authorization. A source release does not imply the new registry version passed review.

## Local image uploader

The reusable uploader is `scripts/postroom-upload.py`; identical copies ship inside both OpenClaw skill distributions. On first use run with `--login --workspace YOUR_WORKSPACE_ID /actual/image.png`, complete browser authorization, then omit --login for subsequent runs. See the bundled guide for permissions and data handling. The image-generation and transfer steps are performed by the host automatically; the user reviews only the exact publishing preview.

Live Mac OAuth, image upload and Bluesky publication succeeded on 2 November 2026. Delivery was independently confirmed with yet_queue and yet_post_status for post 6d517e38-654e-4a4c-8326-c60f091230fd. New archive clean-install testing, other platforms and load/revocation testing remain separate.
