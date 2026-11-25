#!/usr/bin/env bash
set -e
mkdir -p docs
cat > docs/design-note.md <<'EOF'
# Upload retries

## 1. Goal

Uploads to object storage must survive short outages.

## 2. Limits

At most 3 retries. Base delay 200 ms, doubled after each retry.

## 3. Retry state machine

An upload is in one of four states: `pending`, `uploading`, `waiting`, `failed`.

- `pending` -> `uploading` when a worker takes the job.
- `uploading` -> `pending` is not allowed.
- `uploading` -> `waiting` on a 503 or a timeout, when retries < 3.
- `waiting` -> `uploading` after the delay.
- `uploading` -> `failed` on a 4xx, or when retries = 3.
- A success ends the job (not a state).
EOF
