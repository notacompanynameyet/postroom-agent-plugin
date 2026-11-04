# Postroom for Claude

This plugin wraps the same Postroom hosted MCP connector. Each customer signs in through OAuth to their own workspace. It contains no credentials, local MCP process, cwd override, hooks or image-generation service.

## Local validation and test

Requires Claude Code 2.1.281 or later. From this directory, run `claude plugin validate . --strict`. Load with `claude --plugin-dir .`, open `/mcp`, and authorize Postroom through its OAuth flow. Verify the workspace using yet_profile before preparing content. Connector directory submission and plugin bundle submission are separate; this package is not a claim of directory approval.

## Publishing and media

Previews are saved drafts, not scheduled posts. Review exact content, destinations and time before authorizing yet_approve. Cancellation needs explicit approval. Reuse existing receipts after uncertain responses; do not create duplicate posts.

The MCP server does not generate images. A separately configured host capability may generate them. ChatGPT attachment import remains client-specific; Claude web attachment URLs are not supported. Direct image transfer requires a client capable of reading actual file bytes and PUTting them to the exact returned signed URL, then completing the upload. Do not claim Claude web can perform this merely because the server exposes upload tools.

See the linked documentation, privacy policy and support page. No account connection authorizes publication automatically.

## Submission readiness

This is a prepared package, not a submitted or approved listing. Strict manifest validation passes on Claude Code 2.1.318. The directory profile additionally requires a repository/plugin license; no license grant has been invented for this business-owned package. Choose and supply the distribution license before directory submission, then run `claude plugin validate . --strict --profile directory`. Complete authenticated Claude tool testing separately.
