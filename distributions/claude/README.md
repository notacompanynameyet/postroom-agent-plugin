# Postroom — social media publishing for Claude

Postroom connects Claude to your own Postroom workspace, helping you inspect connected social accounts, work with saved brand voice, prepare previews, upload media, review publishing queues, schedule only content you explicitly approve, and read available analytics. This bundle combines three reusable workflow skills with Postroom's hosted, OAuth-protected MCP connector.

## What is included

- **Social publishing:** choose connected accounts, use brand guidelines, prepare channel-specific previews, approve a specific preview before scheduling, and inspect delivery states.
- **Media uploads:** create a secure workspace upload, upload existing media through a compatible client or authenticated Postroom browser page, then retrieve the saved media reference.
- **Analytics and reporting:** inspect connected accounts, queued posts, published status and available cached analytics without treating unavailable metrics as zero.

The plugin does not create or publish content autonomously. Connecting an account or installing a plugin does not approve a post. Any scheduling must be separately authorized against the exact saved preview; cancellation needs separate user authorization.

## Data access, processing, and destinations

The bundled MCP endpoint is `https://social.notacompanynameyet.com/mcp/claude` (Streamable HTTP). It uses Postroom-managed OAuth 2.0 authorization. Users sign in through the Postroom browser OAuth flow; this bundle contains **no account credentials or API tokens** and does not request passwords in a chat.

With authorization, Postroom can read workspace identity, connected account metadata, brand guidance, queued posts, status, held previews, Pinterest boards, and cached analytics. It can store user-directed workspace previews, media, scheduling decisions, and status receipts. The remote Postroom service may send approved content and media to the relevant authorized social platform APIs to fulfil publishing requests. Media files uploaded to Postroom may be made publicly accessible for their intended publishing purpose. No undisclosed server or analytics recipient is added by this bundle. Data processing and retention are governed by the [Postroom privacy policy](https://social.notacompanynameyet.com/privacy-policy).

## Connecting and testing

Install the plugin from the Claude directory or load this folder in Claude Code. Connect Postroom through the OAuth prompt and verify `yet_profile` is the intended workspace. Use `yet_accounts` and `yet_brand` to identify the authorized destination and brand voice. For Pinterest, choose a board returned by `yet_pinterest_boards`. Create a preview using `yet_preview` or `yet_run_workflow`; these actions do **not** schedule publication. Review and explicitly approve the exact preview before `yet_approve`. Use `yet_post_status` to distinguish a queued post from a published one.

A valid image or video upload may be provided through `yet_create_media_upload`. If the client cannot upload file bytes directly, open the returned authenticated browser upload URL, select a local file, then retrieve the workspace reference through `yet_get_media_upload`. Some social platforms have different media restrictions. The connector does not generate AI images, video or audio.

No hooks, local executables, package installation, telemetry, third-party scripts, or secret-bearing headers are included in this bundle.

## Support

- [Claude setup documentation](https://social.notacompanynameyet.com/docs/claude-connector)
- [Media Gateway documentation](https://social.notacompanynameyet.com/docs/media-gateway)
- [Support](https://social.notacompanynameyet.com/support)
- [Terms](https://social.notacompanynameyet.com/terms-of-service)
- [Privacy](https://social.notacompanynameyet.com/privacy-policy)

Published by Vardhiva Innovations. Directory acceptance and publication remain subject to Anthropic's review.
