"""Hermetic regression coverage for the publishing boundary, not the LLM."""
import datetime as dt
import importlib.util
import json
from pathlib import Path
import sqlite3
import subprocess
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('roundup', Path(__file__).parents[1] / 'scripts/weekly_roundup.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)
NOW = dt.datetime(2026, 11, 7, 8, tzinfo=dt.timezone.utc)
PASSAGE = 'RAN4 asks RAN1 to evaluate receiver performance before deciding on the waveform.'


def row(key='1', doc='R1-2609005', fingerprint='new', days=1):
    return {'key': key, 'tdoc_id': doc, 'fingerprint': fingerprint,
            'latest': (NOW - dt.timedelta(days=days)).isoformat(),
            'tdoc_url': 'https://www.3gpp.org/ftp/test/' + doc + '.zip',
            'raw_text': PASSAGE, 'wg_name': 'RAN4' if key in ('3', '4') else 'RAN1', 'meeting_number': '127', 'agenda_item': key}


ANALYSIS = 'Receiver performance remains unresolved, so the transmitter results alone cannot establish the net gain.'


def source_ledger():
    return {
        'editorial': {
            'decision': 'publish', 'question': 'Does the evaluation establish a net gain?',
            'answer': 'Receiver effects still need to be evaluated.',
            'mechanism': 'A transmit power gain can be offset by a receiver penalty.',
            'tradeoff': 'Transmitter output and receiver performance require joint evaluation.',
            'consequence': 'Waveform selection needs a net-gain comparison.',
            'novelty': 'Connects the new request to the earlier evaluation baseline.',
            'uncertainty': 'The receiver evaluation could change the result.',
            'source_ids': ['R1-2609005', 'R1-2609006'],
            'analysis_excerpt': ANALYSIS,
        },
        'claims': [{'claim': 'Receiver evaluation requested', 'tdoc_id': doc, 'passage': PASSAGE}
                   for doc in ('R1-2609005', 'R1-2609006', 'R1-2609007', 'R1-2609008', 'R1-2609009', 'R1-2609010')],
        'coverage': {'topics': [
            {'domain': domain, 'heading': heading, 'working_groups': [group], 'source_ids': ids,
             'finding': 'Conditional evaluation result', 'mechanism': 'Receiver and transmitter constraints interact',
             'tradeoff': 'Efficiency versus implementation cost', 'next_step': 'Verify the assumptions',
             'analysis_excerpt': ANALYSIS}
            for domain, heading, group, ids in [
                ('waveform_modulation', 'Waveform losses', 'RAN1', ['R1-2609005', 'R1-2609006']),
                ('mobility_measurements', 'Measurement scheduling', 'RAN4', ['R1-2609007', 'R1-2609008']),
                ('energy_saving', 'Wake-up operation', 'RAN1', ['R1-2609009', 'R1-2609010'])]]},
    }


def fixture_sources():
    return [row(str(n + 1), 'R1-' + str(2609005 + n)) for n in range(6)]


def fixture_body():
    blocks = []
    for topic in source_ledger()['coverage']['topics']:
        blocks.append('## ' + topic['heading'] + '\n\n' + ANALYSIS + ' ' + ' '.join(
            '[' + doc + '](' + row(doc=doc)['tdoc_url'] + ')' for doc in topic['source_ids']))
    return '\n\n'.join(blocks) + '\n'


class EvidenceTests(unittest.TestCase):
    def test_bootstrap_excludes_published_and_old_evidence(self):
        self.assertEqual(r.select_candidates([row(), row('2', 'R1-2609006', days=20)], {}, {'R1-2609005'}, NOW), [])

    def test_delayed_analysis_changed_fingerprint_and_backlog(self):
        rows = [row(), row('2', fingerprint='changed', days=30), row('3', fingerprint='same')]
        state = {'seen': {'2': 'old', '3': 'same'}}
        self.assertEqual([x['key'] for x in r.select_candidates(rows, state, set(), NOW)], ['1', '2'])

    def test_new_source_scope_does_not_backfill_old_material(self):
        state = {'seen': {}, 'initial_since': (NOW - dt.timedelta(days=14)).isoformat()}
        self.assertEqual(r.select_candidates([row(days=30)], state, set(), NOW), [])
        self.assertEqual(len(r.select_candidates([row(days=10)], state, set(), NOW)), 1)

    def test_research_inventory_preserves_both_agendas_without_raw_text(self):
        rows = fixture_sources()
        index = r.research_inventory(rows, rows)
        self.assertEqual({x['working_group'] for x in index['agenda']}, {'RAN1', 'RAN4'})
        self.assertEqual(sum(len(x['documents']) for x in index['agenda']), 6)
        self.assertNotIn('raw_text', json.dumps(index))

    def test_snapshot_and_partial_failure_diagnostics(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'source.db'
            with sqlite3.connect(path) as conn:
                conn.executescript('''CREATE TABLE tdocs(id,tdoc_id,title,source,tdoc_url,meeting_id);
                CREATE TABLE tdoc_content(tdoc_id,raw_text,extracted_at);
                CREATE TABLE meetings(id,wg_name,meeting_number);
                CREATE TABLE tdoc_analysis(tdoc_id,topic_id,analyzed_at);
                CREATE TABLE crawl_log(source,source_key,last_fetched_at,status);
                CREATE TABLE meeting_analysis_status(status);
                INSERT INTO meetings VALUES(1,'RAN4','121');
                INSERT INTO meetings VALUES(2,'Plenary','111');
                INSERT INTO tdocs VALUES(2,'RP-260232','Mobility','RAN2','https://www.3gpp.org/context.zip',2);
                INSERT INTO tdoc_content VALUES(2,'Layer 1 Layer 2 Triggered Mobility definition','2026-11-06T23:00:00Z');
                INSERT INTO tdocs VALUES(1,'R1-2609005','Reply','RAN4','https://www.3gpp.org/test.zip',1);
                INSERT INTO tdoc_content VALUES(1,'Verified raw evidence','2026-11-06T23:00:00Z');
                INSERT INTO crawl_log VALUES('tdoc-content','Rel-20','2026-11-06','Extracted 45, failed 222');
                INSERT INTO meeting_analysis_status VALUES('pending');''')
            target = Path(tmp) / 'snapshot.db'
            r.snapshot(path, target)
            rows, health = r.evidence(target)
            self.assertEqual(len(rows), 2)
            self.assertEqual(health['pending_analysis_batches'], 1)
            self.assertIn('222', health['crawl_log'][0]['status'])
            self.assertEqual(len(r.select_candidates(rows, {}, set(), NOW)), 2)


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.work = Path(self.tmp.name)
        self.article = self.work / 'article.md'
        self.ledger = self.work / 'ledger.json'
        self.source = row()
        self.context = row('2', 'R1-2609006')
        self.sources = fixture_sources()
        self.article.write_text('---\ntitle: Radio study\ndescription: Receiver work\ndate: 2026-11-07\ntags: [3GPP]\ndraft: false\nfeatured: true\nllm: generated\n---\n' + fixture_body())
        self.ledger.write_text(json.dumps(source_ledger()))

    def validate(self):
        return r.validate(self.work, self.article, self.ledger, self.sources, {'status': 'ready'})

    def test_verified_citation(self):
        self.assertEqual(len(self.validate()), 6)

    def test_wrong_url_rejected(self):
        self.article.write_text(self.article.read_text().replace('/ftp/test/', '/wrong/'))
        with self.assertRaisesRegex(ValueError, 'Unverified citation'):
            self.validate()

    def test_fabricated_evidence_rejected(self):
        self.ledger.write_text(self.ledger.read_text().replace(PASSAGE, PASSAGE + ' Adopted.'))
        with self.assertRaisesRegex(ValueError, 'contiguous passage'):
            self.validate()

    def test_old_context_alone_cannot_make_new_post(self):
        with self.assertRaisesRegex(ValueError, 'no new candidate'):
            r.validate(self.work, self.article, self.ledger, [row('99', 'R1-2699999')], {'status': 'ready'}, self.sources)

    def test_no_news_must_not_leave_article(self):
        with self.assertRaisesRegex(ValueError, 'unexpectedly includes'):
            r.validate(self.work, self.article, self.ledger, [], {'status': 'no_news', 'reason': 'Insufficient new evidence'})

    def test_non_verbatim_quote_rejected(self):
        self.article.write_text(self.article.read_text() + '\n“Agreed and adopted by all.”\n')
        with self.assertRaisesRegex(ValueError, 'quotation'):
            self.validate()


    def test_verified_summary_without_editorial_argument_rejected(self):
        data = source_ledger()
        del data['editorial']
        self.ledger.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, 'editorial publish decision'):
            self.validate()

    def test_single_source_argument_rejected(self):
        data = source_ledger()
        data['editorial']['source_ids'] = ['R1-2609005']
        self.ledger.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, 'two distinct verified'):
            self.validate()

    def test_private_analysis_missing_from_article_rejected(self):
        data = source_ledger()
        data['editorial']['analysis_excerpt'] = 'A conclusion that appears only in the private memo.'
        self.ledger.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, 'excerpt must appear'):
            self.validate()

    def test_missing_consequence_rejected(self):
        data = source_ledger()
        data['editorial']['consequence'] = ''
        self.ledger.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, 'Missing editorial reasoning: consequence'):
            self.validate()

    def test_one_issue_with_several_headings_rejected(self):
        data = source_ledger()
        for topic in data['coverage']['topics']:
            topic['domain'] = 'sensing'
        self.ledger.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, 'distinct technical areas'):
            self.validate()

    def test_single_working_group_report_rejected_when_both_have_evidence(self):
        data = source_ledger()
        data['coverage']['topics'][1]['working_groups'] = ['RAN1']
        self.ledger.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, 'working groups must match'):
            self.validate()

    def test_coverage_reasoning_must_be_in_the_claimed_section(self):
        data = source_ledger()
        data['coverage']['topics'][1]['analysis_excerpt'] = 'Private reasoning only'
        self.ledger.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, 'relevant article section'):
            self.validate()

    def test_new_working_group_cannot_be_silently_omitted(self):
        data = source_ledger()
        sources = fixture_sources()
        for source in sources:
            source['wg_name'] = 'RAN1'
        for topic in data['coverage']['topics']:
            topic['working_groups'] = ['RAN1']
        self.ledger.write_text(json.dumps(data))
        new_ran4 = row('99', 'R4-2639999')
        new_ran4['wg_name'] = 'RAN4'
        with self.assertRaisesRegex(ValueError, 'omits a working group'):
            r.validate(self.work, self.article, self.ledger, sources + [new_ran4], {'status': 'ready'}, sources)

    def test_sources_from_other_sections_do_not_establish_coverage(self):
        data = source_ledger()
        data['coverage']['topics'][0]['source_ids'] = ['R1-2609007', 'R1-2609008']
        self.ledger.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, 'cited in its section'):
            self.validate()

    def test_legacy_single_issue_ledger_rejected(self):
        data = source_ledger()
        del data['coverage']
        self.ledger.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, 'three distinct technical areas'):
            self.validate()


class RunnerTests(unittest.TestCase):
    def test_dirty_checkout_defers_without_snapshot_or_model(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(['git', 'init', '-b', 'main', str(root / 'repo')], check=True, capture_output=True)
            (root / 'repo/user-draft.md').write_text('Unfinished user work')
            with patch.object(r, 'snapshot', side_effect=AssertionError('must not snapshot')):
                self.assertEqual(r.run(root / 'repo', root / 'runs'), 1)
            self.assertEqual(json.loads((root / 'runs/latest-status.json').read_text())['status'], 'deferred')
            self.assertEqual((root / 'repo/user-draft.md').read_text(), 'Unfinished user work')

    def test_validated_commit_recovery_without_model(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, logs = root / 'repo', root / 'runs'
            logs.mkdir()
            subprocess.run(['git', 'init', '-b', 'main', str(repo)], check=True, capture_output=True)
            r.git(repo, 'config', 'user.email', 'test@example.com')
            r.git(repo, 'config', 'user.name', 'Test')
            r.git(repo, 'commit', '--allow-empty', '-m', 'base')
            base = r.git(repo, 'rev-parse', 'HEAD')
            r.git(repo, 'checkout', '-b', 'review')
            r.git(repo, 'commit', '--allow-empty', '-m', 'validated article')
            commit = r.git(repo, 'rev-parse', 'HEAD')
            r.git(repo, 'checkout', 'main')
            r.write_json(logs / 'pending-commit.json', {'commit': commit, 'branch': 'review', 'base': base})
            with patch.object(r, 'snapshot', side_effect=AssertionError('must recover first')):
                self.assertEqual(r.run(repo, logs), 0)
            self.assertEqual(r.git(repo, 'rev-parse', 'HEAD'), commit)
            self.assertFalse((logs / 'pending-commit.json').exists())
            self.assertEqual(json.loads((logs / 'latest-status.json').read_text())['status'], 'recovered')



class PublishingTests(unittest.TestCase):
    def exercise(self, build_ok=True, change_main=False, no_news=False, summary_only=False):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        repo, logs = root / 'repo', root / 'runs'
        subprocess.run(['git', 'init', '-b', 'main', str(repo)], check=True, capture_output=True)
        r.git(repo, 'config', 'user.email', 'test@example.com')
        r.git(repo, 'config', 'user.name', 'Test')
        (repo / 'scripts').mkdir()
        (repo / 'content').mkdir()
        (repo / 'scripts/weekly-roundup-prompt.md').write_text('Test drafting contract')
        (repo / 'AGENTS.md').write_text('Test guide')
        r.git(repo, 'add', '.')
        r.git(repo, 'commit', '-m', 'base')
        initial = r.git(repo, 'rev-parse', 'HEAD')
        original_command = r.command
        source = row()
        source['latest'] = dt.datetime.now(dt.timezone.utc).isoformat()
        context_source = row('2', 'R1-2609006')
        context_source['latest'] = source['latest']
        sources = fixture_sources()
        for item in sources:
            item['latest'] = source['latest']
        def fake_command(args, **kwargs):
            if 'codex' in args and 'exec' in args:
                prompt = kwargs['input']
                params = json.JSONDecoder().raw_decode(prompt.split('Run parameters (absolute paths):\n')[1])[0]
                work = Path(args[args.index('-C') + 1])
                if no_news:
                    r.write_json(Path(params['result']), {'status': 'no_news', 'reason': 'Only old procedural material'})
                    return subprocess.CompletedProcess(args, 0)
                article = work / params['article']
                article.parent.mkdir(parents=True, exist_ok=True)
                article.write_text('---\ntitle: Radio study\ndescription: Receiver work\ndate: ' + params['date'] + '\ntags: [3GPP]\ndraft: false\nfeatured: true\nllm: generated\n---\n' + fixture_body())
                ledger = source_ledger()
                if summary_only:
                    ledger.pop('editorial')
                r.write_json(work / params['ledger'], ledger)
                r.write_json(Path(params['result']), {'status': 'ready'})
                return subprocess.CompletedProcess(args, 0)
            if args[0] == str(root / 'hugo'):
                if not build_ok:
                    raise subprocess.CalledProcessError(1, args)
                if change_main:
                    (repo / 'user-draft.md').write_text('User work created during drafting')
                return subprocess.CompletedProcess(args, 0)
            return original_command(args, **kwargs)
        with patch.object(r, 'command', side_effect=fake_command), patch.object(r, 'snapshot', side_effect=lambda source, dest: sqlite3.connect(dest).close()), patch.object(r, 'evidence', return_value=(sources, {'partial_failures': 222})):
            code = r.run(repo, logs)
        return repo, logs, initial, code

    def test_ready_build_commits_only_article_ledger_and_state(self):
        repo, logs, initial, code = self.exercise()
        self.assertEqual(code, 0)
        self.assertNotEqual(r.git(repo, 'rev-parse', 'HEAD'), initial)
        self.assertEqual(len(r.git(repo, 'diff', '--name-only', initial).splitlines()), 3)
        self.assertFalse(r.git(repo, 'status', '--porcelain'))
        self.assertEqual(json.loads((logs / 'latest-status.json').read_text())['status'], 'committed')
        with patch.object(r, 'snapshot', side_effect=AssertionError('must not rescan same week')):
            self.assertEqual(r.run(repo, logs), 0)
        self.assertEqual(json.loads((logs / 'latest-status.json').read_text())['status'], 'already_prepared')

    def test_summary_without_editorial_case_cannot_commit(self):
        repo, logs, initial, code = self.exercise(summary_only=True)
        self.assertEqual(code, 1)
        self.assertEqual(r.git(repo, 'rev-parse', 'HEAD'), initial)
        status = json.loads((logs / 'latest-status.json').read_text())
        self.assertIn('editorial publish decision', status['reason'])
        self.assertFalse(r.git(repo, 'status', '--porcelain'))

    def test_failed_build_preserves_draft_without_committing_main(self):
        repo, logs, initial, code = self.exercise(build_ok=False)
        self.assertEqual(code, 1)
        self.assertEqual(r.git(repo, 'rev-parse', 'HEAD'), initial)
        status = json.loads((logs / 'latest-status.json').read_text())
        self.assertEqual(status['status'], 'failed')
        self.assertTrue(Path(status['recovery_worktree']).exists())
        self.assertFalse((logs / 'pending-commit.json').exists())

    def test_user_edit_during_draft_keeps_validated_commit_on_branch(self):
        repo, logs, initial, code = self.exercise(change_main=True)
        self.assertEqual(code, 1)
        self.assertEqual(r.git(repo, 'rev-parse', 'HEAD'), initial)
        self.assertEqual((repo / 'user-draft.md').read_text(), 'User work created during drafting')
        self.assertTrue((logs / 'pending-commit.json').exists())
        self.assertEqual(json.loads((logs / 'latest-status.json').read_text())['status'], 'needs_review')

    def test_no_news_preserves_candidates_and_creates_no_commit(self):
        repo, logs, initial, code = self.exercise(no_news=True)
        self.assertEqual(code, 0)
        self.assertEqual(r.git(repo, 'rev-parse', 'HEAD'), initial)
        self.assertNotIn('1', json.loads((logs / 'bootstrap-state.json').read_text())['seen'])
        self.assertEqual(json.loads((logs / 'latest-status.json').read_text())['status'], 'no_news')

    def test_resume_revalidates_failed_draft_without_model_call(self):
        repo, logs, initial, code = self.exercise(build_ok=False)
        self.assertEqual(code, 1)
        saved = json.loads((logs / 'latest-status.json').read_text())['run_directory']
        original_command = r.command
        source = row()
        source['latest'] = dt.datetime.now(dt.timezone.utc).isoformat()
        context_source = row('2', 'R1-2609006')
        context_source['latest'] = source['latest']
        sources = fixture_sources()
        for item in sources:
            item['latest'] = source['latest']
        def no_model(args, **kwargs):
            if 'codex' in args:
                raise AssertionError('Resume must not invoke a model')
            if args[0] == str(repo.parent / 'hugo'):
                return subprocess.CompletedProcess(args, 0)
            return original_command(args, **kwargs)
        with patch.object(r, 'command', side_effect=no_model), patch.object(r, 'snapshot', side_effect=lambda source, dest: sqlite3.connect(dest).close()), patch.object(r, 'evidence', return_value=(sources, {})):
            self.assertEqual(r.run(repo, logs, resume=saved), 0)
        self.assertNotEqual(r.git(repo, 'rev-parse', 'HEAD'), initial)
        self.assertEqual(json.loads((logs / 'latest-status.json').read_text())['status'], 'committed')


if __name__ == '__main__':
    unittest.main()
