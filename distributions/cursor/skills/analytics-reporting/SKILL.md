---
name: analytics-reporting
description: Use when a Postroom user wants to inspect connected social accounts, queued posts, delivery status, or available platform analytics.
---

# Postroom analytics and reporting

Call `yet_profile` to confirm the workspace and `yet_accounts` to list enabled and authorized destinations. Use `yet_queue` and `yet_post_status` to inspect scheduling and confirmed delivery.

Call `yet_analytics` only for connected accounts in the authenticated workspace. Reports are provider-cached snapshots; preserve any freshness timestamps, source limitations and missing-field indicators. Unavailable metrics are not zero. Do not invent engagement, follower or performance figures.

Explain the difference among saved previews, scheduled queue items, cancelled items and successfully published posts. Report a live publication URL only when `yet_post_status` provides one. For troubleshooting media, use `yet_get_media_upload` for a specific upload ticket; do not browse unrelated workspace assets.

This skill reads data. It must not approve, schedule or cancel a post as part of an analytics request.
