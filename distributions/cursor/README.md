# Postroom for Cursor

Postroom's free-to-install Cursor Marketplace plugin bundles a secure remote MCP connection with three skills. It uses the existing Postroom service; it does not ship Postroom's application source code, customer credentials, local scripts, hooks or executable services.

## Included

- **Social publishing:** discover connected accounts, read brand guidance, prepare channel-specific publishing previews, review and explicitly approve exact previews, schedule and verify post statuses.
- **Media upload:** transfer existing media through secure workspace uploads, with a browser-assisted fallback when direct file transfer is unavailable.
- **Analytics and reporting:** retrieve available cached analytics, queued posts and delivery state.

## Connect

MCP URL: `https://social.notacompanynameyet.com/mcp/claude`.
Connection requires Postroom OAuth authorization in the browser. Sign in to the intended workspace and verify with `yet_profile`. No passwords or OAuth tokens should be pasted in agent chat. Account connection is not approval to publish.

All publishing actions operate on the user's connected accounts and provider-granted permissions. `yet_preview` saves an immutable preview, not a scheduled post. `yet_approve` requires approval of the exact content, media, destination and time; `yet_cancel` requires separate approval. Inspect `yet_post_status` when publication state is unclear. The plugin itself requires no payment and contains no purchase flow. Postroom service capabilities are subject to your authorized account and its service terms.

## Data handling

The plugin connects exclusively to Postroom's declared MCP endpoint. Authorized Postroom services store relevant workspace and publishing data and may send user-approved posts and media to authorized third-party social platforms. Media uploaded for publication may be publicly accessible for the intended post. Analytics are provider-cached and may be unavailable for some connected accounts. No user content is sent to additional services by bundled skills.

## Links

- Product: https://social.notacompanynameyet.com
- Documentation: https://social.notacompanynameyet.com/docs/claude-connector
- Media: https://social.notacompanynameyet.com/docs/media-gateway
- Privacy: https://social.notacompanynameyet.com/privacy-policy
- Terms: https://social.notacompanynameyet.com/terms-of-service
- Support: https://social.notacompanynameyet.com/support

The integration package is open-source (MIT). The Postroom backend and service are not part of this source release. Postroom names and trademarks remain reserved.
