# Postroom for OpenClaw — 0.1.1

Generate content in your configured assistant, transfer images automatically, review the exact preview, approve scheduling and inspect delivery. Postroom is published on ClawHub. A live OpenClaw 2026.9.6 test on 2 November 2026 completed image generation, caption writing, automatic image upload, exact-preview approval, scheduling and confirmed Bluesky delivery.

## Install or upgrade

```sh
openclaw plugins install clawhub:@notacompanynameyet/postroom
openclaw plugins inspect postroom
```

For this version before it appears on ClawHub, install the reviewed versioned ZIP:

```sh
openclaw plugins install ./postroom-openclaw-0.1.1.zip
```

If Postroom is already installed, use your host's supported update/reinstall flow and inspect that it reports version 0.1.1. Do not install the standalone skill as well; it contains the same instructions and helper.

## Connect one native MCP server

Version 0.1.1 intentionally contains no bundled MCP server definition. OpenClaw 2026.9.6 can inject an unsupported cwd field into a bundled HTTP server when projecting it into Codex; using one native server avoids this path. Existing 0.1.0 installations should update the whole bundle, not edit user credentials or Codex configuration. Restart the Gateway at a safe point after updating; this interrupts other active runs.

Review any existing Postroom server before replacing it. Run these commands in Terminal, not the OpenClaw chat:

```sh
openclaw mcp set postroom '{"url":"https://social.notacompanynameyet.com/mcp","transport":"streamable-http","auth":"oauth","oauth":{"scope":"social.read social.write"}}'
openclaw mcp login postroom
openclaw mcp probe postroom --json
```

For a first read-only test request social.read only. OAuth belongs to your own workspace. Do not paste passwords, cookies, tokens or OAuth codes into chat. Keep normal tool approvals enabled. Use a private operator-controlled session.

## Generated image → approved post

The skill includes scripts/postroom-upload.py so agents do not need to download a separate helper into Downloads. It runs only when explicitly invoked by the host; there are no install hooks or background processes. Python 3 is required; no third-party Python packages are needed.

Image generation uses the host's configured image tool/API and its own allowance. A chat model alone does not provide image generation. The agent takes the actual generated file, invokes the bundled uploader internally and uses its owned media_url in yet_preview. The user should not manually download or re-upload the generated image or pass it through Composer.

The uploader needs a separate one-time browser OAuth grant for publishing access. It verifies the requested workspace and stores only its own credentials in ~/.postroom/image-uploader/oauth.json (0600 in a 0700 directory), refreshing them for later uploads. It does not read OpenClaw credentials. The agent explains this authorization before starting --login. Revoke it through Postroom's authorized-assistants page when no longer needed.

Supported uploads: PNG, JPEG and WebP, up to 3 MB. Signed storage URLs and tokens stay inside one process and are never printed or reconstructed by the model. No arbitrary external URL import or redirects are allowed.

Example request inside OpenClaw:

> Create a new image and caption in my brand voice for my enabled Bluesky account. Upload the image automatically and prepare a preview for five minutes after upload, using my timezone. Show the exact image, caption, account and time. Wait for my approval before scheduling, then verify delivery.

The agent reads your actual workspace, accounts and brand guidance. An exact preview is not scheduled. Changed or expired details require a new preview and approval. After approval, the existing draft is submitted once; uncertain writes are inspected before retrying. Publication requires a confirmed provider receipt.

## Verified scope and limitations

Live evidence: Bluesky image post published on 2 November 2026 at 20:09:17 Asia/Kolkata:
https://bsky.app/profile/did:plc:zfy6te5ly7cyu44vlldch4ta/post/3mzdki4ph7k2r

The live run used this uploader and native-MCP approach. This 0.1.1 packaging is covered by reproducible archive and mocked transport tests; a clean-install live acceptance run of the new archive remains separate. One Bluesky workflow does not establish every network, revocation, concurrency or stress-test coverage. Hermes catalog review and other client approvals are separate.

Tools call https://social.notacompanynameyet.com/mcp. Requested workspace data enters the host/model context. Social provider credentials remain server-side. Publishing media is publicly accessible. Hosted tools can change independently of this bundle. TikTok uses creator-completed inbox upload through this connector. Provider permissions, limits, Postroom terms and billing apply. Missing metrics are unavailable, not zero.

Privacy: https://social.notacompanynameyet.com/privacy-policy
Terms: https://social.notacompanynameyet.com/terms-of-service
Source: https://github.com/notacompanynameyet/postroom-agent-plugin

