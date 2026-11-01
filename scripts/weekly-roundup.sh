#!/usr/bin/env bash
set -euo pipefail
export PATH="/home/lucas/.npm-global/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
repo=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
exec python3 "$repo/scripts/weekly_roundup.py" "$@"
