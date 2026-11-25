#!/usr/bin/env bash
set -e
mkdir -p reports
cat > reports/ablation.md <<'EOF'
# Cache ablation study

## Verdict

Keep the LRU cache and the prefetch. Drop the compression. p95 latency fell from 412 ms to 268 ms.

## Setup

Load test with 50 rps for 10 minutes on one worker. 3 seeds per variant.

## Results

| Variant | p95 ms | Hit rate | Memory MB | Kept |
|---|---|---|---|---|
| baseline | 412 | 0.00 | 310 | no |
| LRU cache | 301 | 0.71 | 520 | yes |
| LRU + prefetch | 268 | 0.78 | 560 | yes |
| LRU + prefetch + compression | 275 | 0.78 | 430 | no |

## Notes

Compression saved 130 MB but added 7 ms p95. The seed spread was at most 9 ms.
EOF
