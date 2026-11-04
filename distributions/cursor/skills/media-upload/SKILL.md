---
name: media-upload
description: Use when a Postroom user wants to upload an existing image or video to their workspace and attach it to a publishing preview.
---

# Postroom media upload

Postroom transfers existing media and does not itself generate AI images, audio or video. Verify `yet_profile` and use only media owned by the authenticated workspace.

Call `yet_create_media_upload` using an allowed MIME type: JPEG, PNG or WebP images up to 3 MiB, or MP4 videos up to 20 MiB. The resulting ticket is short-lived.

When the client can transfer actual file bytes, PUT the media to the returned signed upload URL, then call `yet_complete_media_upload`. Never display or disclose the signed upload URL or credentials.

When file bytes cannot be transferred directly, use the returned `browser_upload_url`: the user signs into the same Postroom workspace, selects the file, uploads and verifies completion. Call `yet_get_media_upload` with the ticket's `upload_id` to retrieve the workspace-owned media reference.

Use the completed reference with `yet_preview` or `yet_run_workflow` for a supported destination. To update an existing held Content Brain batch, use `yet_held_previews`, then `yet_attach_preview_media` only for a genuine same-workspace held batch. Uploaded media and attached media do not automatically schedule or publish.
