# Do LLMs hallucinate citations?

[Technology & AI](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Quantified failure rates for an AI-governance review.  
> **Why it is hard.** The meta-question: a model answering about its own failure mode.  
> **Data.** Captured 2026-10-23 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [llm-hallucination-evidence.json](../../examples/llm-hallucination-evidence.json).

**The question:**

> How often do large language models fabricate references? Give numbers.

## What Prism returned

### How much evidence exists

| Corpus | Records on both sides of the claim | Window |
| --- | ---: | --- |
| Typed research papers | 294,783 | 2017-2025 |
| Papers with abstracts | 188 | 1990-2025 |
| the health literature index records | 13 | 1990-2025 |
| News articles | 786 | 2019-01-01..2026-06-01 |
| Patents | 185 | 2005-2024 |
| arXiv preprints | 62 | 2005-2025 |

![Evidence volume by corpus](../img/llm-hallucination-evidence-volumes.svg)

![Framing of the literature](../img/llm-hallucination-evidence-sides.svg)

*orientation is a label on the paper's own framing, not a verdict on the claim; this corpus starts in 2017* Contested share: **12.2%**.

### The strongest evidence, read

Prism read 0 sources: **0 support, 0 contradict, 0 qualify** (tier-weighted {"supports": 0, "contradicts": 0, "qualifies": 0}). Each quote is copied from the abstract and verified against it; 0 candidate quotes failed that check and were dropped.

| Year | Study | Tier | Reads as | Verbatim finding |
| ---: | --- | --- | --- | --- |
| 2023 | [Applications of transformer-based language models in bioinformatics: a survey](https://doi.org/10.1093/bioadv/vbad001)<br><sub>Bioinformatics Advances</sub> | review | unrelated | The transformer-based language models, including vanilla transformer, BERT and GPT-3, have achieved revolutionary breakthroughs in the field of natural language processing (NLP). |
| 2024 | [Task-Specific Transformer-Based Language Models in Health Care: Scoping Review](https://doi.org/10.2196/49724)<br><sub>JMIR Medical Informatics</sub> | review | unrelated | BACKGROUND: Transformer-based language models have shown great potential to revolutionize health care by advancing clinical decision support, patient interaction, and disease prediction. |
| 2025 | [A review on the applications of Transformer-based language models for nucleotide sequence analysis](https://doi.org/10.1016/j.csbj.2025.03.024)<br><sub>Computational and Structural Biotechnology Journal</sub> | review | unrelated | Transformer-based language models are making an impact in the field of Natural Language Processing (NLP). |
| 2022 | [RadBERT: Adapting Transformer-based Language Models to Radiology](https://doi.org/10.1148/ryai.210258)<br><sub>Radiology Artificial Intelligence</sub> | article | unrelated | Purpose To investigate if tailoring a transformer-based language model to radiology is beneficial for radiology natural language processing (NLP) applications. |
| 2022 | [Transformer-Based Language Models for Software Vulnerability Detection](https://doi.org/10.1145/3564625.3567985)<br><sub></sub> | article | unrelated | The large transformer-based language models demonstrate excellent performance in natural language processing. |
| 2022 | [Classifying Drug Ratings Using User Reviews with Transformer-Based Language Models](https://doi.org/10.1109/ichi54592.2022.00035)<br><sub>2022 IEEE 10th International Conference on Healthcare Informatics (ICHI)</sub> | article | unrelated | Drug review websites such as Drugs.com provide users' textual reviews and numeric ratings of drugs. |
| 2025 | [Open-Domain Conversational Agents with Transformer-Based Language Models : Toward Multilingualism and Personality](https://theses.fr/2025AVIG0130/document)<br><sub>theses.fr (ABES)</sub> | article | unrelated | Les systèmes de dialogues à domaines ouverts (DDO) sont des agents conversationnels (CAI) conçus pour interagir avec les humains de manière naturelle et ouverte. |
| 2022 | [Affective Coherence Monitoring for Transformer-Based Language Models](https://doi.org/10.48550/arxiv.2212.08073)<br><sub>arXiv (Cornell University)</sub> | preprint | unrelated | As AI systems become more capable, we would like to enlist their help to supervise other AIs. |

![Study designs](../img/llm-hallucination-evidence-tiers.svg)

### What disagrees

Prism's counter-evidence pass found no source that directly contradicts the claim among those it read (tally {"supports": 0, "contradicts": 0, "qualifies": 0, "unrelated": 8, "unread": 0}).

> No verified document verdict supports a wording recommendation for this claim.

![Research output per year](../img/llm-hallucination-evidence-research-series.svg)

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/llm-hallucination-evidence-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 3.0 | 4.0 | 0.5 | 0.0 |
| Measured comparison | 1.5 | 0.5 | 2.0 | 0.0 |
| Visualisation from counted data | 3.5 | 3.5 | 1.0 | 0.0 |
| Exploration and drill-down | 1.5 | 1.0 | 1.0 | 1.0 |
| Data export with provenance | 2.5 | 3.5 | 1.0 | 0.5 |
| Reproducibility | 4.0 | 4.5 | 0.0 | 1.0 |
| Traceable references | 3.5 | 4.5 | 1.5 | 0.5 |
| Accuracy against the corpus | 3.5 | 4.0 | 2.0 | 4.0 |
| Calibration and limits | 4.0 | 3.0 | 3.0 | 2.5 |
| Decision-grade verdict | 4.0 | 4.0 | 0.0 | 2.5 |
| Facet coverage | 4.0 | 3.5 | 1.0 | 1.5 |
| **Score /100** | 65.6 | **68.9** | 22.0 | 26.8 |

**Claude Opus judge:** C separated measured from remembered: it traced every tool number and reported that the corpus held no fabrication-rate evidence. It still gave clearly labelled estimate ranges and a usable decision. A had the most useful real-world figures, and they appear correct, but none trace and its verdict rests on untagged numbers. D was rigorous but answered 'give numbers' with none, and B gave nothing.

**GPT judge:** A is the strongest decision-grade response because it refuses to turn broad subject-corpus counts into a fabrication rate, and it clearly states what evidence would be needed to answer the question. B adds memory-based rate estimates that are labelled honestly, but they remain unverified and its news-trend reading is inconsistent; C is cautious but offers little usable measurement. D appears most numerically decisive, yet its unsupported specifics make it the least reliable basis for a decision.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/llm-hallucination-evidence/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/llm-hallucination-evidence.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
How often do large language models fabricate references? Give numbers.
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.evidence" \
  -H 'content-type: application/json' \
  -d '{"claim": "Large language models fabricate citations", "limit": 10}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['find_evidence']["fn"](**{'claim': 'Large language models fabricate citations', 'limit': 10})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `find_evidence` (114.8 s) → `find_counter_evidence` (28.8 s) → `find_statistics` (25.0 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
