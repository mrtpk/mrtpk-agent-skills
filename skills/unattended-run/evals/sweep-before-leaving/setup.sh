#!/usr/bin/env bash
set -e
cat > sweep.yaml <<'EOF'
script: train.py
learning_rates: [1.0e-4, 3.0e-4, 1.0e-3]
epochs: 20
EOF
cat > train.py <<'EOF'
import sys, time
lr = float(sys.argv[1])
for epoch in range(20):
    time.sleep(60)
    print(f"epoch {epoch} lr {lr} loss {1.0 / (epoch + 1):.3f}", flush=True)
EOF
