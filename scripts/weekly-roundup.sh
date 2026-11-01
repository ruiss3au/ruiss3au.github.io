#!/usr/bin/env bash
set -euo pipefail
export PATH="/home/lucas/.npm-global/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
repo=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
logs="${XDG_STATE_HOME:-$HOME/.local/state}/ruisseau-roundup"
mkdir -p "$logs"
exec 9>"$logs/run.lock"
flock -n 9 || exit 0
exec >>"$logs/$(TZ=Europe/Berlin date +%F).log" 2>&1
date -Is
cd "$repo"
[[ $(git branch --show-current) == main ]]
[[ -z $(git status --porcelain) ]] || { echo 'Checkout is dirty; deferred.'; exit 1; }
command -v codex >/dev/null
command -v node >/dev/null
command -v sqlite3 >/dev/null
[[ -x ../hugo ]]
# Snapshot via SQLite backup, including any committed WAL data.
snapshot=$(mktemp -d /tmp/ruisseau-roundup.XXXXXX)
trap 'rm -rf -- "$snapshot"' EXIT
sqlite3 -readonly ../3gppedia/data/threegppedia.db ".timeout 10000" ".backup '$snapshot/evidence.db'"
export ROUNDUP_DATABASE="$snapshot/evidence.db"
timeout 3h codex exec -C "$repo" -s workspace-write -c approval_policy='"never"' -o "$logs/latest-summary.txt" - < scripts/weekly-roundup-prompt.md
