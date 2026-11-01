# Weekly 3GPP roundup

Ruiss3au owns drafting, evidence verification, coverage tracking, Hugo validation and local commits. 3gppedia owns extraction and analysis; its database is read-only input. Friday's existing 22:00 host-time cron runs refresh-db. Saturday's cron runs at 09:00 on this Europe/Berlin host, including daylight saving changes.

## Operation

Run `bash scripts/weekly-roundup.sh` from any directory. Requires Codex CLI with working unattended authentication, Node, SQLite, flock, timeout, sibling 3gppedia checkout and ../hugo. Uses the configured Codex model. Generation consumes the configured Codex allowance. No extraction API calls are initiated.

Cron entry:

```cron
0 9 * * 6 /bin/bash /media/data2/lab/ruiss3au.github.io/scripts/weekly-roundup.sh
```

The runner locks concurrent invocations, requires clean main and takes a SQLite backup snapshot. The prompt checks refresh completion, selects evidence, verifies claims and builds Hugo into temporary output before committing. No push is performed. Failed runs can leave uncommitted drafts: review or remove those manually before retrying. Authentication or sandbox failures are logged and require operator attention; sandbox restrictions are never bypassed.

Logs and latest-summary.txt live in ~/.local/state/ruisseau-roundup (or $XDG_STATE_HOME). Check these after each run. Review `git show`, the source ledger and a local Hugo preview; then push main yourself to publish. Reject a committed roundup with a reviewed git revert, including its tracking state. Cron misses runs while this machine is off; manually rerun afterward. The next successful run uses saved evidence fingerprints to catch up.

First run considers seven days of extraction/analysis timestamps. Coverage state and source ledgers are committed beside the article, outside Hugo content. No-news runs make no commit and preserve the checkpoint, allowing sparse material to accumulate. Failed refreshes and insufficient evidence defer publication. No automatic historical backfill or existing-post rewrites.
