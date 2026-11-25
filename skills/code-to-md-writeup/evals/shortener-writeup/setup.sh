#!/usr/bin/env bash
set -e
mkdir -p shortener
cat > README.md <<'EOF'
# shortener

A small URL-shortener service.
EOF
cat > shortener/codes.py <<'EOF'
import hashlib


def make_code(url: str, length: int = 7) -> str:
    return hashlib.sha256(url.encode()).hexdigest()[:length]
EOF
cat > shortener/store.py <<'EOF'
class Store:
    def __init__(self) -> None:
        self.by_code: dict[str, str] = {}

    def put(self, code: str, url: str) -> None:
        if code in self.by_code and self.by_code[code] != url:
            raise KeyError("collision")
        self.by_code[code] = url

    def get(self, code: str) -> str | None:
        return self.by_code.get(code)
EOF
cat > shortener/app.py <<'EOF'
from .codes import make_code
from .store import Store

store = Store()


def shorten(url: str) -> str:
    code = make_code(url)
    store.put(code, url)
    return code


def resolve(code: str) -> str | None:
    return store.get(code)
EOF
