# Audit a health article draft

[Journalism & fact-checking](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Every checkable claim found, matched to evidence, with citation coverage.  
> **Why it is hard.** A draft mixes true, overstated and unsupported claims; the audit must tell them apart.  
> **Data.** Captured 2026-10-23 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [audit-coffee-draft.json](../../examples/audit-coffee-draft.json).

**The question:**

> Fact-check this draft before I publish it.
> 
> Coffee is one of the healthiest drinks in the world. Drinking three cups a day lowers the risk of heart disease by 50 percent. Coffee also prevents Parkinson's disease and cures type 2 diabetes. However, caffeine raises blood pressure in the short term.

## What Prism returned

**4 claims detected**, 4 checkable by research. Evidence coverage 82%: *share of the RESEARCH-CHECKABLE claims with a literature behind them, weighted by how directly it speaks to the claim. Claims only a record could settle are excluded rather than counted as failures. It is not a truth score: it says a body of work exists, not that the work agrees*

| # | Claim | Status | Papers on both sides | Searched as | What could be wrong |
| ---: | --- | --- | ---: | --- | --- |
| 1 | Coffee is one of the healthiest drinks in the world. | **claim_covered** | 1,303 | coffee consumption | subjective ranking and vague definition of "healthiest" |
| 2 | Drinking three cups a day lowers the risk of heart disease by 50 percent. | **claim_covered** | 140 | coffee consumption + heart disease | may overstate effect size and imply causality |
| 3 | Coffee also prevents Parkinson's disease and cures type 2 diabetes. | **claim_covered** | 156 | coffee consumption + parkinson's disease, type 2 diabetes | overly strong claim of prevention and cure |
| 4 | Caffeine raises blood pressure in the short term. | **thin_literature** | 3 | caffeine intake + blood pressure | short‑term effect may vary across individuals |

![Claim status](../img/audit-coffee-draft-status.svg)

<details><summary>What each status means</summary>

- **not_research**: only a record — a filing, a register or a news report — could settle this. Prism's research corpus has no opinion, and that is not the same as the claim being wrong
- **no_literature**: no paper title matches this claim's own wording. The field may still cover it under different words — run research.evidence on the claim to find out
- **thin_literature**: a handful of paper titles match this wording — too few to rest an assertion on without reading them
- **literature_exists**: research exists on this subject — which is not the same as research agreeing with the claim; research.evidence reads it
- **claim_covered**: papers cover BOTH sides of the claim, so the literature speaks to it directly
- **unchecked**: the corpus lane failed for this claim
</details>

### Deep reads of the weakest claims

**Caffeine raises blood pressure in the short term.**: 0 support, 0 contradict, 0 qualify

**Drinking three cups a day lowers the risk of heart disease by 50 percent.**: 0 support, 0 contradict, 0 qualify

**Coffee also prevents Parkinson's disease and cures type 2 diabetes.**: 0 support, 1 contradict, 0 qualify

| Year | Study | Tier | Reads as | Verbatim finding |
| ---: | --- | --- | --- | --- |
| 2025 | [Coffee Consumption Is Associated With Later Age‐at‐Onset of Parkinson's Disease](https://doi.org/10.1002/acn3.70076)<br><sub>Annals of Clinical and Translational Neurology</sub> | article | contradicts | no causal association or genetic correlation with PD risk or progression. |

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/audit-coffee-draft-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Visualisation from counted data | 0.0 | 0.0 | 0.0 | 0.0 |
| Exploration and drill-down | 3.5 | 1.0 | 1.0 | 1.0 |
| Data export with provenance | 2.5 | 4.0 | 1.0 | 1.0 |
| Reproducibility | 2.5 | 4.5 | 0.0 | 0.0 |
| Traceable references | 3.5 | 4.0 | 1.0 | 1.5 |
| Accuracy against the corpus | 3.5 | 3.5 | 1.5 | 3.0 |
| Calibration and limits | 3.0 | 4.5 | 3.5 | 3.0 |
| Decision-grade verdict | 4.0 | 4.5 | 0.0 | 3.5 |
| Facet coverage | 4.0 | 4.0 | 1.0 | 1.5 |
| **Score /100** | 58.0 | **67.7** | 18.1 | 33.3 |

**Claude Opus judge:** A and B both grounded the fact-check in the audit. B went further: it drilled into the documents behind every claim, separated verified from unverified quotes, and gave a decisive rewrite. A had cleaner replay provenance but misreported the reference's Parkinson's/diabetes tally. C and D answered from memory; C added fabricated-looking DOIs and D had too few identifiers to check.

**GPT judge:** D is the strongest decision aid: its figures, export, and citations trace to the supplied audit, and it explains what the retrieval counts do and do not establish. A offers more proposed next steps, but its unverified quotes and partly ungrounded interpretations weaken confidence; B and C rely on memory or estimates, and B adds unresolved identifiers and an untagged number.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/audit-coffee-draft/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/audit-coffee-draft.pdf)

## Live MCP session

Here each model was given only the question and a live connection to the Prism MCP server, and chose its own calls.

**Claude** (claude-sonnet, 905.2 s) called 2 Prism tools:

| # | Tool | Arguments | Result |
| ---: | --- | --- | --- |
| 1 | `research_audit` | `{"text": "Coffee is one of the healthiest drinks in the world. Drinking three cups a day lowers the risk of heart disease by 50 percent. Coffee also prevents Pa` | ok · 12,155 chars |
| 2 | `find_evidence` | `{"claim": "Drinking three cups of coffee a day lowers the risk of cardiovascular disease", "limit": 8}` | ok · 18,301 chars |

<details><summary>Claude's answer</summary>

**Verdict: don't publish as written.** Three of the four claims are overstated or unsupported. Only the blood-pressure line holds up.

**What the data shows**
- **"Lowers heart disease risk by 50%": wrong.** The BMJ umbrella review (Poole et al., 2017) found the largest reduction at 3–4 cups a day versus none. For cardiovascular disease the relative risk was 0.85 (95% CI 0.80–0.90), which is about 15%, not 50%. A 2021 dose-response meta-analysis (Di Maso et al., *Advances in Nutrition*) found the same pattern. It saw the largest reduction at 3–4 cups a day and none beyond that. A 2014 meta-analysis (Crippa et al., *Am J Epidemiol*) found a 21% lower CVD *mortality* at 3 cups a day (95% CI 16–26%).
- **"Prevents Parkinson's": overstated.** Ross et al. (JAMA, 2000) found that higher coffee and caffeine intake was associated with a significantly lower incidence of Parkinson's. That is an association in an observational study, not prevention.
- **"Cures type 2 diabetes": no support.** The audit found 53 papers covering coffee together with both Parkinson's and diabetes. I did not retrieve any that show a cure, and I don't know of any. Observational work can show lower risk, but nothing I retrieved shows coffee treating or reversing the disease.
- **"Raises blood pressure in the short term": supported.** Corti et al. (*Circulation*, 2002) found that coffee acutely raises sympathetic nerve activity and blood pressure. The effect was seen in non-habitual drinkers and also occurred with decaffeinated coffee. So "caffeine" is slightly too narrow; "coffee" is safer.
- **"One of the healthiest drinks in the world": not testable.** It is a ranking claim. The umbrella review's pooled estimates are favourable, but that is not a ranking.

**Interpretation (mine)**
- The favourable associations come mostly from observational cohorts, so causation isn't established.
- The benefit appears to plateau at 3–4 cups a day.

**Suggested rewrite:** "Moderate coffee drinking, about 3–4 cups a day, is associated with roughly 15% lower cardiovascular risk and with lower Parkinson's incidence in observational studies. Coffee can raise blood pressure temporarily."

**Limits:** The study windows run from 2000 to 2021. I read only a few abstracts. The audit's literal title matching returned zero papers for the heart-disease and blood-pressure claims as phrased, so those verdicts come from the separate evidence search.

</details>

**ChatGPT** (gpt-6-luna, 400.1 s) called 5 Prism tools:

| # | Tool | Arguments | Result |
| ---: | --- | --- | --- |
| 1 | `research_audit` | `{"text": "Coffee is one of the healthiest drinks in the world. Drinking three cups a day lowers the risk of heart disease by 50 percent. Coffee also prevents Pa` | ok · 46,100 chars |
| 2 | `evidence_card` | `{"claim": "Does coffee cure type 2 diabetes, or does caffeine affect glucose control?", "style": "source_card"}` | ok · 5,259 chars |
| 3 | `evidence_card` | `{"claim": "Does coffee prevent Parkinson's disease in humans? What risk estimate and study period are reported?", "style": "source_card"}` | ok · 5,269 chars |
| 4 | `evidence_card` | `{"claim": "Does caffeine cause a short-term rise in blood pressure, and by how much/how long?", "style": "source_card"}` | ok · 5,685 chars |
| 5 | `evidence_card` | `{"claim": "Does drinking three cups of coffee per day reduce risk of coronary heart disease by 50%, and over what follow-up period?", "style": "source_card"}` | ok · 5,839 chars |

<details><summary>ChatGPT's answer</summary>

**Direct answer: Don’t publish this as written.** The “50 percent” and “cures” claims are unsupported or overstated; the Parkinson’s claim needs to be framed as an association, and “healthiest” is an unsourced ranking.

**What Prism’s evidence shows**

- A 2023 meta-analysis of prospective cohort studies found no significant association between coffee consumption and coronary heart disease risk: RR 1.05 (95% CI 0.97–1.14). It does not support a 50% reduction from three cups a day. The source does not specify one follow-up window for that pooled estimate. [Park et al., 2023](https://doi.org/10.1016/j.amjcard.2022.10.010)
- A 2000 JAMA study reported lower Parkinson’s incidence among men drinking more coffee: 10.4 versus 1.9 cases per 10,000 person-years, comparing no coffee with at least 28 oz/day. That is an observational association, not proof coffee prevents the disease. [Ross, 2000](https://doi.org/10.1001/jama.283.20.2674)
- A 2014 meta-analysis found coffee consumption associated with lower *risk* of developing type 2 diabetes; that does not mean coffee cures diabetes. [Ding et al., 2014](https://doi.org/10.2337/dc13-1203)
- Prism found an acute blood-pressure signal in one 2025 controlled study: mean arterial pressure increased 30 minutes after 200 mg caffeine. That supports a short-term effect, but the retrieved result does not quantify its size or duration. [Vera et al., 2025](https://doi.org/10.1123/ijsnem.2024-0159)

**Interpretation:** Replace “prevents” with “has been associated with lower risk,” remove “cures,” and avoid calling coffee one of the world’s healthiest drinks without a defined comparison and strong supporting evidence.

</details>

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Fact-check this draft before I publish it.

Coffee is one of the healthiest drinks in the world. Drinking three cups a day lowers the risk of heart disease by 50 percent. Coffee also prevents Parkinson's disease and cures type 2 diabetes. However, caffeine raises blood pressure in the short term.
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.audit" \
  -H 'content-type: application/json' \
  -d '{"text": "Coffee is one of the healthiest drinks in the world. Drinking three cups a day lowers the risk of heart disease by 50 percent. Coffee also prevents Parkinson's disease and cures type 2 diabetes. However, caffeine raises blood pressure in the short term.", "deep": 3}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['research_audit']["fn"](**{'text': "Coffee is one of the healthiest drinks in the world. Drinking three cups a day lowers the risk of heart disease by 50 percent. Coffee also prevents Parkinson's disease and cures type 2 diabetes. However, caffeine raises blood pressure in the short term.", 'deep': 3})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
