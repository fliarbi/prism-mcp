# Citations for a sugar-tax story

[Journalism & fact-checking](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Ready-to-paste citations, rendered from stored metadata, with source ranking.  
> **Why it is hard.** Models invent DOIs; every citation here comes from the corpus record.  
> **Data.** Captured 2026-10-23 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [citations-sugar-tax.json](../../examples/citations-sugar-tax.json).

**The question:**

> Give me APA citations for the claim that sugar taxes reduce sugary drink consumption, ranked by weight.

## What Prism returned

### APA citations, rendered from stored metadata

1. Smith, B. T., Warren, C. M., Anderson, L. N., Hammond, D., Manuel, D. G., Li, Y., Andreacchi, A. T., Rosella, L. C., Fu, S. H., & Hobin, E. (2024) The equitable impact of sugary drink taxation structures on sugary drink consumption among Canadians: a modelling study using the 2015 Canadian Community Health Survey-Nutrition. Public Health Nutrition. https://doi.org/10.1017/s1368980024000545 <sub>[article, moderate]</sub>
2. Zhang, Y., Palma, M. A., Yunjunjie, Z., & A., P. M. (2020) Revisiting Sugar Taxes and Sugary Drink Consumption: Evidence from the Random-Coefficient Demand Model. ANU Open Research (Australian National University). https://doi.org/10.22004/ag.econ.303601 <sub>[article, moderate]</sub>
3. Snowdon, C. (2016) Sugar Taxes: A Briefing. SSRN Electronic Journal. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3852694 <sub>[article, moderate]</sub>

Inline markers: `(Smith and colleagues (2024))` · `(Zhang and colleagues (2020))` · `(Snowdon (2016))`

### Source ladder

| Rank | Source | Tier | Why this tier carries the weight it does |
| ---: | --- | --- | --- |
| 1 | [Insights on the Influence of Sugar Taxes on Obesity Prevention Efforts](https://doi.org/10.1007/s13668-019-00282-4) (2019) | review | summarises a field rather than adding a measurement |
| 2 | [Are Australians ready for warning labels, marketing bans and sugary drink taxes? Two cross-sectional surveys measuring s](https://doi.org/10.1136/bmjopen-2018-027962) (2019) | article | peer-reviewed research article |
| 3 | [Partisan Responses to Public Health Messages: Motivated Reasoning and Sugary Drink Taxes](https://doi.org/10.1215/03616878-4193606) (2017) | article | peer-reviewed research article |
| 4 | [Funding quality pre-kindergarten slots with Philadelphia’s new ‘sugary drink tax’: simulating effects of using an excise](https://doi.org/10.1017/s1368980017001756) (2017) | article | peer-reviewed research article |
| 5 | [Can sugar taxes be used for financing surgical systems in Nigeria? A mixed-methods political economy analysis](https://doi.org/10.1093/heapol/czae021) (2024) | article | peer-reviewed research article |
| 6 | [Revisiting Sugar Taxes and Sugary Drink Consumption: Evidence from the Random-Coefficient Demand Model](https://doi.org/10.22004/ag.econ.303601) (2020) | article | peer-reviewed research article |
| 7 | [Predicting the potential health and economic impact of a sugary drink tax in Canada: a modelling study](http://hdl.handle.net/10012/13021) (2018) | article | peer-reviewed research article |
| 8 | [Sugar Taxes: A Briefing](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3852694) (2016) | article | peer-reviewed research article |

![Source tiers](../img/citations-sugar-tax-ladder.svg)

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/citations-sugar-tax-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Data export with provenance | 3.0 | 4.0 | 0.5 | 0.0 |
| Reproducibility | 3.0 | 4.5 | 1.0 | 1.0 |
| Traceable references | 4.0 | 4.0 | 3.0 | 0.0 |
| Accuracy against the corpus | 3.0 | 4.0 | 2.0 | 0.5 |
| Calibration and limits | 3.5 | 3.0 | 3.0 | 3.0 |
| Decision-grade verdict | 3.5 | 4.0 | 3.0 | 2.5 |
| Facet coverage | 3.5 | 3.5 | 1.0 | 1.0 |
| **Score /100** | 66.4 | **78.5** | 39.4 | 23.6 |

**Claude Opus judge:** A and D both built their citation lists from the recorded corpus, traced their rows, and honestly concluded the three-entry set (one supporting, two contradicting, all moderate-strength articles) cannot establish the claim. D edges ahead on export and reproducibility hygiene, while A was sharper on anomalies such as the by_tier totals and the off-topic rows. B gave a useful but unverified memory-based answer with internal metadata mismatches. C invented DOIs, which disqualifies it for a citation request.

**GPT judge:** A is the strongest decision aid because it provides a replayable, traceable citation export and distinguishes Prism’s stance labels from verified study findings. C is similarly cautious but misreads the source-ranking record; B and D offer stronger-sounding conclusions that depend on unsupported or fabricated specifics.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/citations-sugar-tax/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/citations-sugar-tax.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Give me APA citations for the claim that sugar taxes reduce sugary drink consumption, ranked by weight.
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.citations" \
  -H 'content-type: application/json' \
  -d '{"claim": "Sugar taxes reduce sugary drink consumption", "style": "apa", "limit": 8}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['get_citations']["fn"](**{'claim': 'Sugar taxes reduce sugary drink consumption', 'style': 'apa', 'limit': 8})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `get_citations` (24.6 s) → `rank_sources` (0.4 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
