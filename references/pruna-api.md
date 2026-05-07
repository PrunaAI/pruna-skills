# Pruna P-API (shared reference)

Official docs: [Developer Portal](https://docs.api.pruna.ai/), [Quickstart](https://docs.api.pruna.ai/guides/quickstart), [Models](https://docs.api.pruna.ai/guides/models).

## Authentication

Send your API key in the **`apikey`** header on every request (not `Authorization: Bearer`).

```bash
-H "apikey: ${PRUNA_API_KEY}"
```

Use the same header on delivery URLs when downloading bytes.

## Base URL

- Predictions: `https://api.pruna.ai/v1/predictions`
- File upload: `https://api.pruna.ai/v1/files` (multipart form field `content=@file`)
- Status: `https://api.pruna.ai/v1/predictions/status/{id}`
- Delivery: use `generation_url` from a succeeded status (may be relative; prefix with `https://api.pruna.ai` if needed)

## Request shape

All generative calls use:

- `POST /v1/predictions`
- Headers: `Content-Type: application/json`, `apikey`, **`Model: <model-id>`** (for example `p-image`, `p-image-edit`, `p-video`, `p-video-avatar`, `p-image-upscale`)
- JSON body: `{ "input": { ... } }` where `input` fields match the model page (see each skill).

## Sync vs async

| Mode | Header | When to use |
|------|--------|--------------|
| Synchronous | `Try-Sync: true` | Fast jobs (many images, simple edits). Completes within ~60s or may time out. |
| Asynchronous | omit `Try-Sync` | Video, long edits, production reliability. Poll `get_url` / status until `succeeded` or `failed`. |

Official guidance: prefer **async for video**; sync is acceptable for quick **p-image** / **p-image-edit** / **p-image-upscale** when latency is low.

## File uploads

1. `POST /v1/files` with `-F "content=@/path/to/file.jpg"` and `apikey` header.
2. Use `urls.get` from the response (or construct `https://api.pruna.ai/v1/files/{id}`) as the **`image`**, **`images[]`**, **`audio`**, etc. value in `input`.

Uploaded files expire (see upload response `expires_at`).

## Typical success response

- **Sync:** `{ "status": "succeeded", "generation_url": "..." }`
- **Async (create):** `{ "id": "...", "get_url": "https://api.pruna.ai/v1/predictions/status/..." }`
- **Async (poll):** eventually `{ "status": "succeeded", "generation_url": "..." }`

Download binary output with `GET` to `generation_url` and the same `apikey` header.

## Environment variable

Skills in this repo assume **`PRUNA_API_KEY`** is set in the shell when running `curl` examples.
