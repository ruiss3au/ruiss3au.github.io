"""Local-only, recoverable weekly editorial runner. Uses only the standard library."""
import argparse
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
import subprocess
import sys
import time
from zoneinfo import ZoneInfo

UTC = dt.timezone.utc
STATE = 'docs/weekly-roundup-state.json'
ID = r'(?:R[1-6]|RP|S[1-6]|SP|C[1-6]|CP)-\d{6,}'
DOMAINS = {'waveform_modulation', 'control_access', 'mimo_csi_beamforming',
           'mobility_measurements', 'energy_saving', 'ai_ml', 'spectrum_rf',
           'satellite_ntn', 'sensing', 'release20_features'}


def research_inventory(rows, candidates):
    """Make the whole candidate agenda visible before the writer selects coverage."""
    groups = {}
    for row in candidates:
        group = row.get('wg_name', 'Context')
        key = (group, str(row.get('meeting_number', '')), row.get('agenda_item') or 'Unassigned')
        entry = groups.setdefault(key, {'working_group': group, 'meeting': key[1],
                                      'agenda': key[2], 'description': row.get('agenda_description'),
                                      'documents': []})
        entry['documents'].append({k: row.get(k) for k in ('tdoc_id', 'title', 'source')})
    return {'agenda': [groups[k] for k in sorted(groups)],
            'context_available': sorted({r.get('wg_name', 'Context') for r in rows}),
            'instruction': 'Survey all RAN1 and RAN4 agenda areas. Classifications are research leads, not evidence.'}


def validate_coverage(verified, body, sources, candidates):
    coverage = verified.get('coverage', {})
    topics = coverage.get('topics', []) if isinstance(coverage, dict) else []
    if len(topics) < 3:
        raise ValueError('Roundup requires at least three distinct technical areas')
    domains, headings, groups, used = set(), set(), set(), set()
    for topic in topics:
        domain, heading = topic.get('domain'), topic.get('heading')
        if domain not in DOMAINS or domain in domains:
            raise ValueError('Coverage domains must be distinct technical areas')
        if not isinstance(heading, str) or heading in headings:
            raise ValueError('Each coverage area requires its own article section')
        match = re.search(r'^## ' + re.escape(heading) + r'\s*\n(.*?)(?=^## |\Z)', body, re.M | re.S)
        if not match:
            raise ValueError('Coverage heading missing from article')
        section = match[1]
        ids = topic.get('source_ids', [])
        cited = set(re.findall(r'\[(' + ID + r')\]\(', section))
        if not isinstance(ids, list) or len(set(ids)) < 2 or not set(ids) <= (cited & sources.keys()):
            raise ValueError('Each coverage area requires two verified sources cited in its section')
        for field in ('finding', 'mechanism', 'tradeoff', 'next_step', 'analysis_excerpt'):
            value = topic.get(field)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f'Missing coverage reasoning: {field}')
        if topic['analysis_excerpt'] not in section:
            raise ValueError('Coverage analysis must appear in the relevant article section')
        claimed_groups = set(topic.get('working_groups', []))
        actual_groups = {sources[i].get('wg_name') for i in ids}
        if not claimed_groups or not claimed_groups <= (actual_groups & {'RAN1', 'RAN4'}):
            raise ValueError('Coverage working groups must match their primary sources')
        groups.update(claimed_groups)
        used.update(ids)
        domains.add(domain)
        headings.add(heading)
    if len(used) < 6:
        raise ValueError('Roundup coverage requires six distinct primary sources')
    available = {r.get('wg_name') for r in candidates} & {'RAN1', 'RAN4'}
    if not available <= groups:
        raise ValueError('Roundup omits a working group with new candidate evidence')
    for group in groups:
        if not any(r['tdoc_id'] in used and r.get('wg_name') == group for r in candidates):
            raise ValueError('Each covered working group needs new evidence')


def command(args, cwd=None, timeout=120, **kwargs):
    return subprocess.run(args, cwd=cwd, check=True, text=True,
                          timeout=timeout, **kwargs)


def git(repo, *args):
    return command(['git', *args], cwd=repo, capture_output=True).stdout.strip()


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')
    temp.replace(path)


def timestamp(value):
    try:
        parsed = dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
        return parsed.replace(tzinfo=parsed.tzinfo or UTC).astimezone(UTC)
    except (ValueError, AttributeError):
        return dt.datetime.min.replace(tzinfo=UTC)


def snapshot(source, destination):
    # SQLite backup provides a consistent view even if extraction is running.
    start = time.monotonic()
    def progress(*_):
        if time.monotonic() - start > 120:
            raise TimeoutError('Database snapshot exceeded two minutes')
    with sqlite3.connect(source.resolve().as_uri() + '?mode=ro', uri=True, timeout=10) as src:
        with sqlite3.connect(destination) as dest:
            src.backup(dest, pages=1024, progress=progress, sleep=0.1)


def evidence(database):
    with sqlite3.connect(database.as_uri() + '?mode=ro', uri=True) as conn:
        conn.row_factory = sqlite3.Row
        analyses = {}
        for row in conn.execute('SELECT * FROM tdoc_analysis ORDER BY tdoc_id, topic_id'):
            analyses.setdefault(row['tdoc_id'], []).append(dict(row))
        rows = []
        for row in conn.execute('''SELECT t.*, c.raw_text, c.extracted_at,
                m.wg_name, m.meeting_number FROM tdocs t
                JOIN tdoc_content c ON c.tdoc_id=t.id
                JOIN meetings m ON m.id=t.meeting_id
                WHERE trim(COALESCE(c.raw_text,'')) != '' '''):
            item = dict(row)
            if item['wg_name'] not in ('RAN', 'RAN1', 'RAN4') and not (item['wg_name'] == 'Plenary' and item['tdoc_id'].startswith('RP-')):
                continue
            if not item['tdoc_url'] or not item['tdoc_url'].startswith('https://www.3gpp.org/'):
                continue
            analysis = analyses.get(item['id'], [])
            material = [item['title'], item['source'], item['tdoc_url'], item['raw_text'], analysis]
            item['fingerprint'] = hashlib.sha256(json.dumps(material, sort_keys=True).encode()).hexdigest()
            item['latest'] = max([timestamp(item['extracted_at'])] +
                                 [timestamp(a['analyzed_at']) for a in analysis]).isoformat()
            item['key'] = str(item['id'])
            item.pop('raw_text')  # Keep historical raw text out of memory and run manifests.
            rows.append(item)
        logs = [dict(row) for row in conn.execute(
            'SELECT source,source_key,last_fetched_at,status FROM crawl_log ORDER BY last_fetched_at DESC')]
        pending = conn.execute("SELECT COUNT(*) FROM meeting_analysis_status WHERE status='pending'").fetchone()[0]
    return rows, {'crawl_log': logs, 'pending_analysis_batches': pending,
                  'policy': 'Partial/stale refresh and pending analysis are warnings, not drafting gates.'}


def select_candidates(rows, state, existing, now):
    seen = state.get('seen', {})
    candidates = []
    initial_since = timestamp(state.get('initial_since')) if state.get('initial_since') else timestamp(state.get('scan_cutoff', now.isoformat())) - dt.timedelta(days=7)
    for row in rows:
        key, fingerprint = row['key'], row['fingerprint']
        if seen.get(key) == fingerprint:
            continue
        # First-run bootstrap avoids republishing sources already used by the blog.
        if not state and row['tdoc_id'] in existing:
            continue
        if key not in seen and timestamp(row['latest']) < initial_since:
            continue
        candidates.append(row)
    return candidates


def validate(work, article, ledger, candidates, result, context=None):
    if result.get('status') not in ('ready', 'no_news'):
        raise ValueError('Missing ready/no_news editorial result')
    if result['status'] == 'no_news':
        if article.exists() or ledger.exists():
            raise ValueError('no_news result unexpectedly includes publication files')
        if not result.get('reason'):
            raise ValueError('no_news requires a reason')
        return []
    text = article.read_text()
    body = text.split('---', 2)[-1]
    if not text.startswith('---\n') or len(text.split('---', 2)) != 3:
        raise ValueError('Missing YAML front matter')
    front = text.split('---', 2)[1]
    for field in ('title', 'description', 'date', 'tags'):
        if not re.search(rf'^{field}:\s*\S', front, re.M):
            raise ValueError(f'Missing front matter: {field}')
    for field, value in [('draft', 'false'), ('featured', 'true'), ('llm', 'generated')]:
        if not re.search(rf'^{field}:\s*{value}\s*$', front, re.M):
            raise ValueError(f'Invalid publication setting: {field}')
    if any(token in body for token in ('—', '--', 'FR3')):
        raise ValueError('Prohibited editorial wording')
    sources = {row['tdoc_id']: row for row in (context or candidates)}
    citations = re.findall(r'\[(' + ID + r')\]\(([^)]+)\)', body)
    expected_date = re.search(r'3gpp-weekly-(\d{4}-\d{2}-\d{2})', article.name)
    if expected_date and not re.search(r'^date:\s*' + expected_date[1] + r'\s*$', front, re.M):
        raise ValueError('Article date does not match scheduled week')
    if not citations:
        raise ValueError('Article has no primary citations')
    if not {doc for doc, _ in citations} & {row['tdoc_id'] for row in candidates}:
        raise ValueError('Article cites no new candidate evidence')
    verified = json.loads(ledger.read_text())
    claims = verified.get('claims', [])
    if not claims:
        raise ValueError('Source ledger has no claims')
    supported = set()
    for claim in claims:
        source = sources.get(claim.get('tdoc_id'))
        passage = claim.get('passage', '')
        if not claim.get('claim') or not source or len(passage.strip()) < 30 or passage not in source['raw_text']:
            raise ValueError('Ledger evidence is not a contiguous passage of the cited TDoc')
        supported.add(source['tdoc_id'])
    for doc, url in citations:
        if doc not in sources or sources[doc]['tdoc_url'].strip() != url or doc not in supported:
            raise ValueError(f'Unverified citation: {doc}')
    # Require an auditable editorial argument, not merely valid citations.
    # These checks establish provenance/completeness; they cannot judge prose quality.
    editorial = verified.get('editorial', {})
    if not isinstance(editorial, dict) or editorial.get('decision') != 'publish':
        raise ValueError('Source ledger requires an editorial publish decision')
    for field in ('question', 'answer', 'mechanism', 'tradeoff', 'consequence', 'novelty', 'uncertainty'):
        if not isinstance(editorial.get(field), str) or not editorial[field].strip():
            raise ValueError(f'Missing editorial reasoning: {field}')
    cited_ids = {doc for doc, _ in citations}
    analysis_sources = editorial.get('source_ids', [])
    if not isinstance(analysis_sources, list) or not all(isinstance(doc, str) for doc in analysis_sources):
        raise ValueError('Invalid editorial source IDs')
    if len(set(analysis_sources)) < 2 or not set(analysis_sources) <= (cited_ids & supported):
        raise ValueError('Editorial argument requires two distinct verified cited sources')
    excerpt = editorial.get('analysis_excerpt', '')
    if not isinstance(excerpt, str) or not excerpt.strip() or excerpt not in body:
        raise ValueError('Editorial analysis excerpt must appear verbatim in the article')
    validate_coverage(verified, body, sources, candidates)
    # Quotes are optional; if used they must be an exact contiguous source substring.
    for quote in re.findall(r'“([^”]+)”|"([^"\n]+)"', body):
        value = next(part for part in quote if part)
        if not any(value in sources[doc]['raw_text'] for doc, _ in citations):
            raise ValueError('Non-verbatim quotation')
    return sorted(set(doc for doc, _ in citations))


def run(repo, base, check_only=False, resume=None):
    now = dt.datetime.now(UTC)
    saturday = now.astimezone(ZoneInfo('Europe/Berlin')).date()
    saturday -= dt.timedelta(days=(saturday.weekday() - 5) % 7)
    label = saturday.isoformat()
    saved_draft = None
    if resume:
        resume = Path(resume).resolve()
        if not resume.is_relative_to(base.resolve()) or not (resume / 'result.json').is_file():
            raise ValueError('Resume requires a saved editorial result within the state directory')
        draft_paths = [p for p in git(resume / 'worktree', 'ls-files', '--others', '--exclude-standard').splitlines()
                       if re.fullmatch(r'content/posts/3gpp-weekly-\d{4}-\d{2}-\d{2}\.md', p)]
        if len(draft_paths) != 1:
            raise ValueError('Resume requires exactly one uncommitted roundup draft')
        saved_draft = resume / 'worktree' / draft_paths[0]
        label = saved_draft.stem.removeprefix('3gpp-weekly-')
    run_dir = base / now.strftime('%Y%m%dT%H%M%S.%fZ')
    run_dir.mkdir(parents=True)
    report = {'started_at': now.isoformat(), 'status': 'running', 'run_directory': str(run_dir)}
    def status(name, **fields):
        report.update(status=name, **fields)
        write_json(base / 'latest-status.json', report)
        print(json.dumps(report), flush=True)
    status('checking')
    work = None
    database = run_dir / 'evidence.db'
    try:
        if git(repo, 'branch', '--show-current') != 'main' or git(repo, 'status', '--porcelain'):
            status('deferred', reason='Main checkout must be clean; user changes preserved')
            return 1
        head = git(repo, 'rev-parse', 'HEAD')
        pending = base / 'pending-commit.json'
        if pending.exists():
            saved = json.loads(pending.read_text())
            if check_only:
                status('recovery_pending', **saved)
                return 0
            commit = saved['commit']
            if git(repo, 'rev-parse', saved['branch']) != commit:
                raise ValueError('Recovery branch changed; inspect pending-commit.json')
            if head == saved['base']:
                git(repo, 'merge', '--ff-only', commit)
            elif subprocess.run(['git', 'merge-base', '--is-ancestor', commit, head], cwd=repo).returncode != 0:
                status('needs_review', **saved, reason='Main diverged from validated commit; merge manually')
                return 1
            pending.unlink()
            status('recovered', **saved)
            return 0
        state_path = repo / STATE
        baseline = base / 'bootstrap-state.json'
        state = json.loads(state_path.read_text()) if state_path.exists() else (json.loads(baseline.read_text()) if baseline.exists() else {})
        if state and state.get('schema_version') != 2:
            raise ValueError('Unknown tracking-state version; manual migration required')
        if (repo / f'content/posts/3gpp-weekly-{label}.md').exists():
            status('already_prepared', reason=f'Roundup for {label} already exists')
            return 0
        database = run_dir / 'evidence.db'
        snapshot(repo.parent / '3gppedia/data/threegppedia.db', database)
        rows, health = evidence(database)
        write_json(run_dir / 'coverage.json', health)
        existing = set()
        for post in (repo / 'content').rglob('*.md'):
            existing.update(re.findall(ID, post.read_text()))
        candidates = select_candidates(rows, state, existing, now)
        write_json(run_dir / 'research-index.json', research_inventory(rows, candidates))
        if not state and not check_only:
            candidate_keys = {row['key'] for row in candidates}
            state = {'schema_version': 2, 'initial_since': (now - dt.timedelta(days=7)).isoformat(), 'seen': {row['key']: row['fingerprint'] for row in rows if row['key'] not in candidate_keys}}
            write_json(baseline, state)
        with sqlite3.connect(database.as_uri() + '?mode=ro', uri=True) as conn:
            for item in candidates:
                if 'raw_text' in item:
                    continue
                item['raw_text'] = conn.execute('SELECT raw_text FROM tdoc_content WHERE tdoc_id=?', (int(item['key']),)).fetchone()[0]
        write_json(run_dir / 'candidates.json', candidates)
        if check_only:
            status('checked', candidates=len(candidates), coverage=str(run_dir / 'coverage.json'))
            return 0
        if not candidates:
            status('no_candidates', reason='No new unreviewed raw evidence; no model invocation')
            return 0
        branch = 'automation/roundup-' + run_dir.name
        work = run_dir / 'worktree'
        git(repo, 'worktree', 'add', '-b', branch, str(work), head)
        article_rel = f'content/posts/3gpp-weekly-{label}.md'
        ledger_rel = f'docs/weekly-roundup-ledgers/{label}.json'
        article, ledger = work / article_rel, work / ledger_rel
        result_path = run_dir / 'result.json'
        if resume:
            article.parent.mkdir(parents=True, exist_ok=True)
            ledger.parent.mkdir(parents=True, exist_ok=True)
            article.write_text(saved_draft.read_text())
            ledger.write_text((resume / 'worktree' / ledger_rel).read_text())
            result_path.write_text((resume / 'result.json').read_text())
        prompt = (repo / 'scripts/weekly-roundup-prompt.md').read_text()
        prompt += '\n\nRun parameters (absolute paths):\n' + json.dumps({
            'date': label, 'database': str(database), 'candidates': str(run_dir / 'candidates.json'),
            'coverage': str(run_dir / 'coverage.json'), 'result': str(result_path),
            'research_index': str(run_dir / 'research-index.json'),
            'article': article_rel, 'ledger': ledger_rel,
            'source_guide': str(repo.parent / '3gppedia/knowledge-base/AGENTS.md')}, indent=2)
        # AGENTS.md is locally ignored; carry its editorial rules into the isolated run.
        prompt += '\nPublication repository editorial rules:\n' + (repo / 'AGENTS.md').read_text()
        status('drafting', candidates=len(candidates), branch=branch)
        if not resume:
            with (run_dir / 'codex.log').open('w') as log:
                command(['timeout', '--kill-after=30s', '3h', 'codex', 'exec', '-C', str(work), '--add-dir', str(run_dir),
                         '-s', 'workspace-write', '-c', 'approval_policy="never"',
                         '-o', str(run_dir / 'summary.txt'), '-'], input=prompt,
                        timeout=10900, stdout=log, stderr=subprocess.STDOUT)
        if git(work, 'rev-parse', 'HEAD') != head:
            raise ValueError('Editorial process committed unexpectedly; main left unchanged')
        result = json.loads(result_path.read_text())
        context = list(candidates)
        if result.get('status') == 'ready':
            cited = set(re.findall(ID, article.read_text()))
            with sqlite3.connect(database.as_uri() + '?mode=ro', uri=True) as conn:
                for item in rows:
                    if item['tdoc_id'] in cited and 'raw_text' not in item:
                        item['raw_text'] = conn.execute('SELECT raw_text FROM tdoc_content WHERE tdoc_id=?', (int(item['key']),)).fetchone()[0]
                        context.append(item)
        used = validate(work, article, ledger, candidates, result, context)
        allowed = {article_rel, ledger_rel}
        changed = set(git(work, 'ls-files', '--others', '--exclude-standard').splitlines())
        changed.update(git(work, 'diff', '--name-only', 'HEAD').splitlines())
        if changed - allowed:
            raise ValueError(f'Unexpected draft changes: {sorted(changed - allowed)}')
        # no_news defers candidates for later accumulation rather than losing sparse evidence.
        if result['status'] == 'no_news':
            status('no_news', reason=result['reason'], branch=branch)
            git(repo, 'worktree', 'remove', str(work))
            git(repo, 'branch', '-d', branch)
            return 0
        seen = dict(state.get('seen', {}))
        # Bootstrap already published and older evidence; new unused candidates stay pending.
        candidate_keys = {row['key'] for row in candidates}
        for row in rows:
            if row['tdoc_id'] in used or row['key'] not in candidate_keys:
                seen[row['key']] = row['fingerprint']
        write_json(work / STATE, {'schema_version': 2, 'scan_cutoff': now.isoformat(),
                                  'initial_since': state.get('initial_since', (timestamp(state.get('scan_cutoff', now.isoformat())) - dt.timedelta(days=7)).isoformat()), 'seen': seen, 'last_article': article_rel})
        command([str(repo.parent / 'hugo'), '--minify', '--noBuildLock',
                 '--destination', str(run_dir / 'preview')], cwd=work)
        git(work, 'diff', '--check')
        git(work, 'add', '--', article_rel, ledger_rel, STATE)
        git(work, 'commit', '-m', f'content: 3GPP weekly roundup {label}')
        commit = git(work, 'rev-parse', 'HEAD')
        write_json(pending, {'commit': commit, 'branch': branch, 'base': head, 'worktree': str(work)})
        # A retry after this point can recover this branch without regenerating text.
        if git(repo, 'rev-parse', 'HEAD') != head or git(repo, 'status', '--porcelain') or git(repo, 'branch', '--show-current') != 'main':
            status('needs_review', commit=commit, branch=branch, reason='Main changed during drafting; review isolated commit')
            return 1
        git(repo, 'merge', '--ff-only', branch)
        pending.unlink()
        status('committed', commit=commit, article=article_rel, branch=branch)
        git(repo, 'worktree', 'remove', str(work))
        git(repo, 'branch', '-d', branch)
        return 0
    except Exception as exc:
        status('failed', reason=str(exc), recovery_worktree=str(work) if work else None)
        return 1
    finally:
        database.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--check', action='store_true', help='Snapshot and select evidence without invoking Codex')
    group.add_argument('--resume', metavar='RUN_DIRECTORY', help='Revalidate a saved draft without another model call')
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    base = Path(os.environ.get('XDG_STATE_HOME', str(Path.home() / '.local/state'))) / 'ruisseau-roundup'
    base.mkdir(parents=True, exist_ok=True)
    with (base / 'run.lock').open('w') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print('Another roundup run is active; skipped.', flush=True)
            return 0
        # Keep diagnostics even when preflight or executable lookup fails.
        with (base / 'runner.log').open('a', buffering=1) as log:
            os.dup2(log.fileno(), 1)
            os.dup2(log.fileno(), 2)
            return run(repo, base, args.check, args.resume)


if __name__ == '__main__':
    sys.exit(main())
