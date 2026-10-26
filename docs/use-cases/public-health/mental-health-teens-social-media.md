# Social media and teen mental health

[Public health & epidemiology](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Both sides of one of the most contested questions in public health.  
> **Why it is hard.** Effect sizes are small and contested; an honest answer reports the disagreement.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [mental-health-teens-social-media.json](../../examples/mental-health-teens-social-media.json).

**The question:**

> Does social media use harm adolescent mental health? What does the evidence say, and what disagrees?

## What Prism returned

### How much evidence exists

| Corpus | Records on both sides of the claim | Window |
| --- | ---: | --- |
| Typed research papers | 2,800 | 2017-2025 |
| Papers with abstracts | 4 | 1990-2025 |
| the health literature index records | 6 | 1990-2025 |
| News articles | 6 | 2019-01-01..2026-06-01 |
| Patents | 0 | 2005-2024 |
| arXiv preprints | 0 | 2005-2025 |

![Evidence volume by corpus](../img/mental-health-teens-social-media-volumes.svg)

![Framing of the literature](../img/mental-health-teens-social-media-sides.svg)

*orientation is a label on the paper's own framing, not a verdict on the claim; this corpus starts in 2017* Contested share: **20.2%**.

### The strongest evidence, read

Prism read 2 sources: **2 support, 0 contradict, 0 qualify** (tier-weighted {"supports": 9, "contradicts": 0, "qualifies": 0}). Each quote is copied from the abstract and verified against it; 0 candidate quotes failed that check and were dropped.

| Year | Study | Tier | Reads as | Verbatim finding |
| ---: | --- | --- | --- | --- |
| 2020 | [A meta-analysis of the association between adolescent social media use and depressive symptoms.](https://doi.org/10.1016/j.jad.2020.06.014)<br><sub>Journal of affective disorders</sub> | meta_analysis | supports | We found a small but significant positive correlation (k=12 studies, r=.11, p<.01) between adolescent social media use and depressive symptoms. |
| 2017 | [Adolescent social media use and mental health from adolescent and parent perspectives](https://doi.org/10.1016/j.adolescence.2017.08.005)<br><sub>Journal of Adolescence</sub> | article | supports | anxiety and depressive symptoms were highest among adolescents with a relatively high number of parent-reported social media accounts and relatively high FoMO. |
| 2020 | Adolescent social media use and well-being<br><sub></sub> | article | unread | Results show friendship contingent self-esteem to be significantly related to social media investment, and increased stress to significantly influence well-being change. |
| 2020 | [Longitudinal Associations Between Adolescent Social Media Use and Depressive Symptoms: The Roles of Appearance-Related S](http://d-scholarship.pitt.edu/38612/19/Maheux%20Final%20ETD.pdf)<br><sub>D-Scholarship@Pitt (University of Pittsburgh)</sub> | article | unread | it did not mediate or moderate the link between time on social media and depressive symptoms in the full sample. |
| 2025 | [The representation of adolescent social media use: a systematic review and content analysis of UK newspaper articles.](https://doi.org/10.1186/s12889-025-23897-5)<br><sub>BMC public health</sub> | review | unrelated | Most headlines (58%) were negatively framed, with tabloids generally adopting a more negative tone than broadsheets. |
| 2025 | [Neuroscientific approaches to adolescent social media use: a review of neural correlates and potential associations to s](https://doi.org/10.1152/jn.00282.2024)<br><sub>Journal of neurophysiology</sub> | review | unrelated | Adolescents' social lives are evolving rapidly, existing largely online. There are mixed findings on the effect of social media on adolescent mental health. |
| 2025 | [Social media are many things: Addressing the components and patterns of adolescent social media use.](https://doi.org/10.1111/nyas.15326)<br><sub>Annals of the New York Academy of Sciences</sub> | review | unrelated | We advocate for more work taking this nuanced approach and for the development of a comprehensive taxonomic framework that categorizes specific online experiences afforded by social media features and content. |
| 2024 | [The Effect of Moral Disengagement and Online Disinhibition Effect on Cyberbullying in Adolescent Social Media Users](https://doi.org/10.52155/ijpsat.v43.1.6005)<br><sub>International Journal of Progressive Sciences and Technologies (Medical University Varna)</sub> | article | unrelated | The results showed that there was a positive effect of moral disengagement on cyberbullying behavior in adolescent social media users with an effective contribution of 23.4%. |

![Study designs](../img/mental-health-teens-social-media-tiers.svg)

### What disagrees

| Year | Study | Tier | Reads as | Verbatim finding |
| ---: | --- | --- | --- | --- |
| 2025 | [Annual Research Review: Adolescent social media use is not a monolith: toward the study of specific social media compone](https://doi.org/10.1111/jcpp.14085)<br><sub>Journal of child psychology and psychiatry, and allied disciplines</sub> | review | contradicts | To date, the majority of research investigating the effects of these changes has measured time spent on social media, yielding inconclusive results |

> The documents read include both supporting and contradictory findings; explain their differences.

### Numbers you can quote

| Figure | Measures | Population | Source |
| --- | --- | --- | --- |
| **98%** | proportion of articles discussing potential risks | articles about adolescent social media use | [The representation of adolescent social media use: a systematic review and content analysis of UK newspaper articles.](https://doi.org/10.1186/s12889-025-23897-5) 2025 |
| **24%** | proportion of articles discussing suicidality | articles about adolescent social media use | [The representation of adolescent social media use: a systematic review and content analysis of UK newspaper articles.](https://doi.org/10.1186/s12889-025-23897-5) 2025 |
| **58%** | proportion of headlines negatively framed | headlines about adolescent social media use | [The representation of adolescent social media use: a systematic review and content analysis of UK newspaper articles.](https://doi.org/10.1186/s12889-025-23897-5) 2025 |
| **31%** | proportion of articles using evidence to support claims | articles about adolescent social media use | [The representation of adolescent social media use: a systematic review and content analysis of UK newspaper articles.](https://doi.org/10.1186/s12889-025-23897-5) 2025 |
| **23.4%** | effective contribution of moral disengagement on cyberbullying behavior | adolescent social media users | [The Effect of Moral Disengagement and Online Disinhibition Effect on Cyberbullying in Adolescent Social Media Users](https://doi.org/10.52155/ijpsat.v43.1.6005) 2024 |
| **8.4%** | effective contribution of online disinhibition effect on cyberbullying behavior | adolescent social media users | [The Effect of Moral Disengagement and Online Disinhibition Effect on Cyberbullying in Adolescent Social Media Users](https://doi.org/10.52155/ijpsat.v43.1.6005) 2024 |

![Research output per year](../img/mental-health-teens-social-media-research-series.svg)

**Extracted disease-factor claims** (2 claims; extracted claims, not papers — one paper can produce several, and the same finding restated in ten papers counts ten times): association/na (observational) ×2

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/mental-health-teens-social-media-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 3.5 | 3.0 | 1.0 | 0.5 |
| Measured comparison | 4.0 | 3.0 | 1.5 | 0.5 |
| Visualisation from counted data | 3.5 | 3.5 | 1.0 | 0.0 |
| Exploration and drill-down | 1.0 | 2.0 | 1.0 | 1.0 |
| Data export with provenance | 3.5 | 3.0 | 1.0 | 0.0 |
| Reproducibility | 4.0 | 4.0 | 1.0 | 1.0 |
| Traceable references | 4.5 | 4.5 | 1.0 | 1.0 |
| Accuracy against the corpus | 3.5 | 4.0 | 3.0 | 2.5 |
| Calibration and limits | 4.0 | 4.0 | 3.0 | 3.5 |
| Decision-grade verdict | 4.0 | 4.0 | 3.5 | 3.0 |
| Facet coverage | 4.5 | 3.5 | 1.5 | 1.5 |
| **Score /100** | **73.2** | 71.4 | 35.3 | 27.7 |

**Claude Opus judge:** C and D both grounded their answers in the recorded evidence: the r=.11 meta-analysis, the inconclusive 2025 review and the traced research series. C went further, quantifying growth, comparing stance counts exactly, contrasting media framing with evidence, and catching tool anomalies, and it set a calibrated low confidence. A and B gave sensible memory-based verdicts but no measurable or traceable data, and A also carried a mismatched DOI.

**GPT judge:** A best balances a decision-ready answer with traceable study evidence, a clearly defined small association, and an explicit account of contradictory versus qualifying evidence. B is the most complete corpus dashboard, but it overreads framing counts and mishandles the censored endpoint; C and D are candid about memory or missing data, yet provide much less grounded evidence.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/mental-health-teens-social-media/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/mental-health-teens-social-media.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Does social media use harm adolescent mental health? What does the evidence say, and what disagrees?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.evidence" \
  -H 'content-type: application/json' \
  -d '{"claim": "Social media use harms adolescent mental health", "limit": 10}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['find_evidence']["fn"](**{'claim': 'Social media use harms adolescent mental health', 'limit': 10})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `find_evidence` (133.1 s) → `find_counter_evidence` (15.9 s) → `find_statistics` (24.6 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
