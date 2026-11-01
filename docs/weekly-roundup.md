# Weekly 3GPP roundup

Ruiss3au owns drafting, verification, coverage tracking, Hugo validation and local publication commits. 3gppedia owns extraction and analysis; its database is read-only input. The existing Friday 22:00 host-time cron runs `refresh-db`. This Europe/Berlin host runs the roundup on Saturday at 09:00, including daylight saving changes.

```cron
0 9 * * 6 /bin/bash /media/data2/lab/ruiss3au.github.io/scripts/weekly-roundup.sh
```

## Running and checking

Run `bash scripts/weekly-roundup.sh` from any directory. Use `bash scripts/weekly-roundup.sh --check` to snapshot the database and count candidates without calling Codex or creating publication commits. Requires Python 3.9+, Node, Codex CLI with unattended authentication, GNU timeout, the sibling 3gppedia checkout and `../hugo`. The runner uses the configured Codex model and its allowance. It never starts extraction or paid extraction analysis.

The machine must be on. Cron does not catch up after downtime: run manually if missed. The next run detects changes since saved evidence fingerprints, including delayed analysis of older documents.

## Publication boundary

The runner uses a process lock and requires clean `main`. It snapshots SQLite using its backup API, including committed WAL data. Download failures (including HTTP 403), stale crawl timestamps and pending LLM batches are recorded as coverage warnings. Successfully extracted documents remain eligible; no complete-refresh requirement exists. Missing raw text cannot substantiate technical claims.

The first scan considers the previous seven days and excludes sources already cited in the blog. A durable local bootstrap baseline keeps unused candidates eligible beyond that week. Subsequent successful posts commit schema-version-2 evidence fingerprints in `docs/weekly-roundup-state.json`; only used evidence is consumed. Unused candidates remain eligible. No-news runs make no commit and do not consume candidates. One existing roundup per Saturday prevents repeat posts.

Codex drafts in a dedicated Git worktree. It cannot decide which files to commit: the runner allows only the new article and JSON source ledger, adds tracking state itself, checks citation IDs and exact URLs, checks contiguous supporting passages and verbatim quotations, and builds Hugo into a temporary preview. At least one new candidate must be cited. Automated substring checks do not establish that a passage logically supports a claim; the editorial prompt requires that review, and you retain final publication approval.

The runner creates a local commit after validation. It advances `main` only if the checkout is still clean and its original HEAD is unchanged. If you edit during the run, your work stays intact and the validated commit remains on its review branch. No pushes or deployments occur.

## Logs and recovery

Status lives in `~/.local/state/ruisseau-roundup/latest-status.json` (or beneath `$XDG_STATE_HOME`). `runner.log` captures runner errors. Each timestamped run directory contains coverage diagnostics, selected evidence, `codex.log`, the editorial summary and, when drafted, a preview. Database snapshots are deleted after the run. Model execution is limited to three hours; validation and Git commands also have timeouts.

- `committed`: inspect `git show`, the JSON claim ledger and the preview. Push `main` yourself to publish.
- `already_prepared`, `no_candidates`, `no_news`: successful skip with a recorded reason. No duplicate or empty commit.
- `deferred`: clean or commit your checkout before rerunning. User changes are never reset or stashed.
- `failed`: inspect the reason and run logs. Failed drafts remain in their isolated worktree; `main` and committed coverage stay unchanged. Fix the cause and rerun. To reuse a completed editorial draft after a validation or build failure, run `bash scripts/weekly-roundup.sh --resume <timestamped-run-directory>`. This copies only its article, ledger and result into a fresh worktree and revalidates them against a new snapshot without another model call. Authentication and sandbox failures are reported, never bypassed.
- `needs_review`: a validated commit is recorded in `pending-commit.json`. Once your checkout is clean, rerunning fast-forwards it if possible without another model call. If `main` diverged, review and merge the recorded branch manually, then rerun to acknowledge recovery. Do not delete a pending branch before recovery.
- `recovered`: an earlier validated commit was recovered; no text was regenerated.

Retained failed worktrees can be inspected with `git worktree list`. Remove one with `git worktree remove <path>` only after saving any desired draft; remove its branch separately. Completed run previews and logs can be removed when no longer needed. To reject a committed post, revert the article, ledger and tracking-state changes together. No historical backfill or existing-post rewrites are automatic.

## Verification

`python3 -m unittest discover -s tests -v` runs hermetic tests with temporary databases and Git repositories. Coverage includes partial extraction and pending analysis, first-run exclusions, delayed/changed evidence, exact evidence checks, dirty checkouts, failed builds, publication commits, duplicate runs, no-news retention, edits during drafting, validated-commit recovery, and resuming a failed build without another model call. LLM output is stubbed; test runs do not call a provider.
