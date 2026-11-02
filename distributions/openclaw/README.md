# Postroom for OpenClaw — preview bundle 0.1.0

This is a Codex-format content bundle supported by OpenClaw, containing the Postroom skill and hosted MCP connection metadata. It contains no executable plugin code and does not require a Claude subscription. This is not the ChatGPT upload ZIP. ClawHub acceptance, automated security review and live OAuth/tool verification are separate milestones; none is implied by downloading this archive.

## Install

```sh
openclaw plugins install ./postroom-openclaw-0.1.0.zip
openclaw plugins list
openclaw plugins inspect postroom
```

If you install the complete bundle, do not separately install the standalone Postroom skill; the same instructions are included.

## Authorize your own workspace

Installing the bundle grants no account access and no permission to publish. Review an existing server definition before changing it. In your private operator session, configure the native MCP server and complete its OAuth flow:

```sh
openclaw mcp set postroom '{"url":"https://social.notacompanynameyet.com/mcp","transport":"streamable-http","auth":"oauth","oauth":{"scope":"social.read social.write"}}'
openclaw mcp login postroom
openclaw mcp probe postroom --json
```

For read-only testing request only social.read. Keep tool approvals enabled. OpenClaw stores OAuth credentials; never paste passwords, tokens, cookies or authorization codes into chat. Do not expose your workspace through an agent serving unrelated users.

First test: List my Postroom accounts. Do not publish or schedule anything. Confirm the workspace and account names. Then prepare an unscheduled preview, inspect its exact text/destination/media/time, and verify it remains unscheduled. Scheduling requires explicit approval of that exact preview. Check receipts before claiming publication. Revoke the grant after disposable testing.

## Data and limitations

Tools call https://social.notacompanynameyet.com/mcp. Requested workspace information enters the host/model context. Social provider credentials remain server-side. Publishing media is publicly accessible. The hosted tool list can change independently of this bundle. ChatGPT attachment imports accept trusted ChatGPT URLs; OpenClaw users should upload media to their Postroom workspace. TikTok uses creator-completed inbox upload in this connector. Provider approvals, permissions, limits and Postroom terms apply. Missing metrics are unavailable, not zero. Installing the bundle does not bypass billing or provider reviews.

Privacy: https://social.notacompanynameyet.com/privacy-policy
Terms: https://social.notacompanynameyet.com/terms-of-service
Source: https://github.com/notacompanynameyet/postroom-agent-plugin
