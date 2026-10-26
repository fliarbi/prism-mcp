"""Offline regression gates derived from the live 50-case audit."""
import copy
import unittest
from unittest.mock import patch

from test_regressions import TEMP, P
from prism import api, article, cache, ch, compose, evidence, llm, news, query, requests, workflows


class WorkflowTests(unittest.TestCase):
    def test_optional_list_rest_schema_and_nested_json_coercion(self):
        params = {p['name']: p for p in api._params(P.trend_scenarios)}
        self.assertEqual(params['observations']['type'], 'array')
        self.assertTrue(params['observations']['nullable'])
        self.assertEqual(api._coerce('[{"year": 2020, "value": 5}]', 'array'),
                         [{'year': 2020, 'value': 5}])
    def test_plan_no_model_or_sql(self):
        with patch.object(llm, 'call_json') as model, patch.object(ch, 'chq_rows') as sql:
            out = workflows.plan('Do shorter weeks improve output?', ['four day week'], ['productivity'])
            self.assertFalse(out['facts_generated'])
            self.assertFalse(out['needs_scope'])
            model.assert_not_called(); sql.assert_not_called()

    def test_scope_and_year_validation_before_database(self):
        with patch.object(ch, 'coverage_of') as check:
            for kw in ({'subject_phrases': []}, {'subject_phrases': ['x']},
                       {'subject_phrases': ['battery'], 'last_year': 2026},
                       {'subject_phrases': ['battery'], 'limit': 90}):
                self.assertFalse(workflows.packet('A claim.', **kw)['available'])
            check.assert_not_called()

    def test_outage_not_empty_evidence(self):
        with patch.object(cache, 'get', return_value=None), \
             patch.object(ch, 'coverage_of', return_value={'partial': True}), \
             patch.object(ch, 'chq_rows') as sql:
            self.assertEqual(workflows.packet('A claim.', ['solar'])['kind'], 'upstream')
            sql.assert_not_called()

    def test_packet_one_query_and_snapshot_original_abstract(self):
        row = ['W123', 'Solar energy efficiency', 'Results show no improvement. '*30,
               '[]', 'Journal', '2024', '10.1234/test', '1', 'article', '[]', '']
        with patch.object(ch, 'coverage_of', return_value={'partial': False}), \
             patch.object(ch, 'chq_rows', return_value=[row, row]) as sql, \
             patch.object(evidence, 'stance', return_value=[]) as read:
            out = workflows.packet('Solar energy is efficient fixture.', ['solar energy'], ['efficiency'], read=False)
            self.assertEqual(len(out['sources']), 1)
            self.assertEqual(sql.call_count, 1); read.assert_not_called()
            statement = sql.call_args.args[0]
            self.assertIn('PREWHERE publication_year BETWEEN 2020 AND 2025', statement)
            self.assertIn(' AND ', statement)
            self.assertNotIn('ORDER BY', statement)
            page = workflows.packet_read(out['packet_id'], chars_per_source=400)
            self.assertTrue(page['sources'][0]['abstract_truncated'])
            self.assertFalse(page['sources'][0]['grounded'])
            self.assertIsNone(page['next_offset'])
            hit = workflows.packet('Solar energy is efficient fixture.', ['solar energy'], ['efficiency'], read=False)
            self.assertTrue(hit['cached']); self.assertEqual(sql.call_count, 1)

    def test_path_injection_is_not_a_packet(self):
        self.assertFalse(workflows.packet_read('../../etc/passwd')['available'])

    def test_editor_reuses_scope_locked_packet_without_query(self):
        doc = {'id': 'x', 'stance': 'supports', 'quote': 'Output improved in this trial.',
               'quote_verified': True, 'source_fit': {'passed': True}}
        pid = workflows._save('packet', {'claim': 'The original claim.', 'sources': [doc],
                                        'coverage': {'partial': False}, 'window': {}})
        with patch.object(query, 'build') as lookup:
            self.assertFalse(workflows.context_from_packet(pid, 'A different claim.')['available'])
            ctx = workflows.context_from_packet(pid, 'The original claim.')
            self.assertTrue(ctx['available'])
            self.assertTrue(ctx['research']['documents'][0]['grounded'])
            with patch.object(compose, 'section_candidates', return_value={'available': True}) as suggest:
                out = P.suggest_sections('The original claim.', packet_id=pid)
                self.assertTrue(out['ok']); self.assertEqual(suggest.call_args.kwargs['ctx']['packet_id'], pid)
            lookup.assert_not_called()

    def test_empty_snapshot_is_inspectable_but_not_evidence(self):
        with patch.object(cache, 'get', return_value=None), \
             patch.object(ch, 'coverage_of', return_value={'partial': False}), \
             patch.object(ch, 'chq_rows', return_value=[]):
            out = workflows.packet('No such topic fixture.', ['invented substance'])
            self.assertFalse(out['available'])
            self.assertIn('packet_id', out)

    def test_history_sql_failure_is_not_zero_series(self):
        with patch.object(cache, 'get', return_value=None), \
             patch.object(ch, 'coverage_of', return_value={'partial': False}), \
             patch.object(ch, 'chq_rows', side_effect=ch.CHError('timed out')):
            with self.assertRaises(ch.CHError):
                workflows.history(['battery'])

    def test_history_fills_only_successful_query_window(self):
        with patch.object(ch, 'coverage_of', return_value={'partial': False}), \
             patch.object(ch, 'chq_rows', return_value=[['2023', '3'], ['2025', '5']]):
            out = workflows.history(['sparse fixture'], first_year=2023)
            self.assertEqual([x['value'] for x in out['series']], [3, 0, 5])
            self.assertIn('history_id', out)

    def test_scenario_backtest_no_future_leakage(self):
        rows = [{'year': 2016+i, 'value': 100+10*i} for i in range(10)]
        out = workflows.scenarios(observations=rows, horizon=2)
        self.assertTrue(out['available']); self.assertEqual(out['selected_baseline'], 'linear_drift')
        self.assertEqual(out['scenarios'][0]['central'], 200)
        self.assertIsNone(out['probabilities'])
        self.assertFalse(out['backtest']['independent_holdout'])
        for fold in out['backtest']['folds']:
            self.assertLess(fold['training_through'], fold['year'])
        changed = copy.deepcopy(rows); changed[-1]['value'] = 99999
        later = workflows.scenarios(observations=changed)
        self.assertEqual(out['backtest']['folds'][0], later['backtest']['folds'][0])

    def test_no_change_wins_ties(self):
        out = workflows.scenarios(observations=[{'year': 2018+i, 'value': 10} for i in range(8)])
        self.assertEqual(out['selected_baseline'], 'no_change')

    def test_scenarios_reject_invalid_and_partial_years(self):
        rows = [{'year': 2018+i, 'value': 10} for i in range(8)]
        for change in ({'year': 2026}, {'value': float('nan')}, {'value': -1}, {'year': 2024}, {'value': True}):
            bad = copy.deepcopy(rows); bad[-1].update(change)
            self.assertFalse(workflows.scenarios(observations=bad)['available'])
        self.assertFalse(workflows.scenarios(observations=rows[:7])['available'])
        self.assertFalse(workflows.scenarios(history_id='x', observations=rows)['available'])

    def test_local_arithmetic_routes_before_retrieval(self):
        with patch.object(query, 'build') as search:
            out = P.find_statistics('In this supplied dataset, revenue was 100 in 2023 and 120 in 2024. Calculate the percentage increase using only these two values.')
            self.assertTrue(out['ok']); self.assertEqual(out['data']['percentage_change'], 20)
            search.assert_not_called()

    def test_zero_and_ambiguous_supplied_data(self):
        out = workflows.supplied_change('Provided data was 0 in 2023 and 120 in 2024. Calculate the percentage increase.')
        self.assertIsNone(out['percentage_change'])
        self.assertFalse(workflows.supplied_change('Our private revenue grew 30%. Verify it.')['available'])
        self.assertIsNone(workflows.supplied_change('Does exercise help?'))

    def test_no_false_balance(self):
        text = evidence.recommendation({'supports': 0, 'contradicts': 2})
        self.assertIn('No document read directly supports', text)
        self.assertNotIn('mixed', text)

    def test_source_fit_rejects_wrong_comparator_and_missing_judge(self):
        doc = {'id': 'x', 'title': 'Vertical farming solar panels', 'abstract': 'Electricity use decreased after adding solar panels.'}
        proposed = {'id': 'x', 'grounded': True, 'stance': 'supports', 'quote': doc['abstract']}
        with patch.object(llm, 'call_json', return_value={'checks': [
                {'id': 'x', 'same_question': False, 'quote_justifies_stance': False,
                 'reason': 'No open-field comparator.'}]}):
            verdict = workflows.source_fit('Less than open-field farming.', [doc], [proposed])[0]
            self.assertEqual(verdict['stance'], 'unrelated')
        with patch.object(llm, 'call_json', return_value=None):
            verdict = workflows.source_fit('Less than open-field farming.', [doc], [proposed])[0]
            self.assertEqual(verdict['stance'], 'unread')

    def test_synthetic_biology_is_not_private_data(self):
        self.assertIsNone(workflows.supplied_change('Synthetic biology improves metabolic engineering.'))

    def test_systematic_review_not_automatically_pooled(self):
        self.assertEqual(evidence._tier_of('pubmed', article_types='Systematic Review'), 'review')
        self.assertEqual(evidence._tier_of('pubmed', article_types='Systematic Review, Meta-Analysis'), 'meta_analysis')

    def test_unread_source_cannot_compose(self):
        ctx = {'available': True, 'research': {'documents': [
            {'id': 'test', 'abstract': 'Plausible claims.', 'stance': 'unread'}]}}
        self.assertFalse(compose._usable_context(ctx)['available'])

    def test_citation_lookup_failure_is_not_invalid_reference(self):
        with patch.object(ch, 'chq_rows', side_effect=ch.CHError('offline')):
            out = article.inspect_citations('See doi:10.1234/example.')
            self.assertIsNotNone(out['lookup_error'])
            self.assertEqual(out['unresolved_dois'], ['10.1234/example'])
            self.assertIn('does not mean fabricated', out['verification_note'])

    def test_news_visible_match_and_url_deduplication(self):
        rows = [[str(i), '2025-01-01', '3', 'neutral', '', '[]', '[]', ''] for i in range(3)]
        records = [{'url': 'https://example.org/a', 'title': 'Nvidia introduces a product'},
                   {'url': 'https://example.org/b', 'title': 'An unrelated horse race'},
                   {'url': 'https://example.org/a', 'title': 'Nvidia introduces a product'}]
        with patch.object(ch, 'chq_rows', return_value=rows), \
             patch.object(news.articles, 'resolve', return_value=records), \
             patch.object(ch, 'coverage_of', return_value={'partial': False}):
            out = news._feed('Nvidia', [], 'datetime DESC', 3, '2025-01-01', '2025-02-01', 'news.recent', 'entity_central')
            self.assertEqual(out['returned'], 1)
            self.assertEqual(out['relevance_or_duplicate_rejections'], 2)
            self.assertFalse(out['entity_identity_verified'])

    def test_html_offsets_include_inline_markup_and_entities(self):
        text = '<p>Regular <strong>physical activity</strong> &amp; rest are helpful.</p>'
        sentence = article.sentences(text)[0]
        original = text[sentence['start']:sentence['end']]
        self.assertIn('<strong>', original); self.assertIn('&amp;', original)
        self.assertIn('& rest', sentence['text']); self.assertTrue(original.endswith('helpful.'))

    def test_async_new_endpoints_and_no_publishing(self):
        for name in ('research.plan', 'research.packet', 'research.packet_read', 'analysis.history',
                     'analysis.scenarios', 'research.radar', 'news.geography'):
            self.assertIn(name, requests.ALLOWED)
            self.assertIn(name, requests._REGISTRY)
        self.assertNotIn('compose.article', requests.ALLOWED)


if __name__ == '__main__':
    unittest.main()
