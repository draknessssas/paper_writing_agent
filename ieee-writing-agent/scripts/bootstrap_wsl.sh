#!/usr/bin/env bash
# Backwards-compatible entry point kept for existing docs and muscle memory.
# The real logic lives in scripts/bootstrap.sh, which is portable across
# Linux, WSL, and macOS (the previous version used GNU-only `ln -sfnT`).
set -euo pipefail
exec "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/bootstrap.sh" "$@"
