#!/usr/bin/env bash
set -e
mkdir -p docs/design
cat > docs/design/cache.md <<'EOF'
# Read cache for the profile service

Clients call the profile API. Today each call reads Postgres. We add a Redis read cache.

- Read path: API -> Redis; on a miss, API -> Postgres, then write to Redis with a TTL of 300 s.
- Write path: API -> Postgres, then delete the Redis key.
- Option A: cache whole profiles (2 KB each). Option B: cache only the hot fields (200 B each).
- Risk: stale reads for up to 300 s when the delete fails.
EOF
