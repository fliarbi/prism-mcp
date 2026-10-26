# Benchmark: what Prism adds to Claude and ChatGPT

Every one of the 113 showcase scenarios, four respondents each: Claude (Sonnet) and ChatGPT (gpt-6-luna), each answering from memory and again with Prism's recorded tool results. Every respondent got the same deliverable specification (a decision-grade report with a verdict, measured trend, comparison, charts, drill-down, exports and references) and the same right to draw charts and tables from memory, labelled as estimates. The scoring rubric was designed by Fable 5.1; a script scores every checkable parameter first (number tracing, chart and CSV tracing, DOI lookup against the research index, follow-up execution), then two blind judges (Claude Opus, GPT) score under those ceilings and may only lower them.

![scores](results/full/scoreboard.svg)

|  | Claude alone | Claude + Prism | ChatGPT alone | ChatGPT + Prism |
|---|---|---|---|---|
| Mean score /100 (strict) | 32.0 | 72.0 | 27.4 | 68.7 |
| Mean score /100 (no gates) | 32.0 | 72.5 | 27.4 | 68.7 |
| Best of the four, scenarios | 0 | 81 | 0 | 32 |
| Numbers traced to the corpus | 0/1,647 | 7,406/7,555 | 0/264 | 2,999/3,101 |
| DOIs that resolve | 93/95 | 336/337 | 64/95 | 199/215 |
| Invention gate tripped | 12% | 2% | 1% | 0% |
| Mean answer time, s | 22.9 | 32.3 | 16.3 | 27.0 |

**Same model, with and without Prism:**

| Model | Prism wins | Ties | Memory wins | Mean gain (points) |
|---|---|---|---|---|
| Claude | 113 | 0 | 0 | 40.0 |
| ChatGPT | 113 | 0 | 0 | 41.3 |

Judge agreement: mean absolute difference 0.5 points per parameter on the 0-5 scale. Both judges are of the same model families as the respondents; the script ceilings exist to limit that bias.

## By parameter

Mean score (0-5), and the capability matrix: share of scenarios where the setup produced something real (score ≥ 2) · mean quality when it did.

| Parameter | Weight | Scenarios | Claude alone | Claude + Prism | ChatGPT alone | ChatGPT + Prism |
|---|---|---|---|---|---|---|
| Measured trend | 10 | 94 | 0.9 (0% · —) | 4.1 (99% · 4.2) | 0.2 (1% · 2.0) | 3.7 (97% · 3.7) |
| Measured comparison | 7 | 106 | 1.3 (34% · 2.0) | 4.1 (97% · 4.1) | 0.5 (8% · 2.0) | 3.9 (95% · 4.0) |
| Visualisation from counted data | 10 | 109 | 0.8 (0% · —) | 3.3 (92% · 3.6) | 0.2 (0% · —) | 2.9 (84% · 3.4) |
| Exploration and drill-down | 7 | 109 | 1.3 (12% · 2.0) | 2.9 (90% · 3.1) | 1.1 (5% · 2.1) | 2.2 (71% · 2.6) |
| Data export with provenance | 8 | 111 | 1.0 (0% · —) | 3.0 (94% · 3.2) | 0.3 (0% · —) | 3.4 (97% · 3.5) |
| Reproducibility | 12 | 113 | 0.6 (0% · —) | 4.2 (100% · 4.2) | 0.8 (0% · —) | 4.0 (100% · 4.0) |
| Traceable references | 8 | 86 | 1.4 (23% · 2.9) | 2.6 (63% · 3.6) | 1.0 (17% · 3.1) | 2.4 (59% · 3.5) |
| Accuracy against the corpus | 12 | 113 | 2.8 (96% · 2.9) | 3.6 (99% · 3.6) | 3.1 (87% · 3.4) | 3.6 (99% · 3.6) |
| Calibration and limits | 8 | 113 | 3.2 (100% · 3.2) | 4.0 (100% · 4.0) | 3.0 (99% · 3.0) | 3.7 (100% · 3.7) |
| Decision-grade verdict | 12 | 113 | 2.5 (87% · 2.8) | 3.6 (98% · 3.7) | 2.6 (94% · 2.7) | 3.7 (100% · 3.7) |
| Facet coverage | 6 | 113 | 1.2 (6% · 2.0) | 4.2 (100% · 4.2) | 1.0 (7% · 2.0) | 3.7 (100% · 3.7) |

## By category

| Category | Scenarios | Claude alone | Claude + Prism | ChatGPT alone | ChatGPT + Prism |
|---|---|---|---|---|---|
| Education & labour | 5 | 32.4 | 75.6 | 25.8 | 70.2 |
| Finance & markets | 9 | 32.1 | 75.3 | 28.6 | 68.2 |
| Environment & disasters | 5 | 34.1 | 74.3 | 27.8 | 68.9 |
| Public health & epidemiology | 7 | 29.7 | 74.1 | 27.3 | 69.4 |
| Supply chain & trade | 5 | 31.1 | 74.1 | 23.3 | 71.4 |
| Academic research & literature review | 6 | 33.2 | 73.0 | 35.5 | 66.1 |
| Medical & clinical evidence | 10 | 34.1 | 72.9 | 29.4 | 69.1 |
| Defence & geopolitics | 7 | 29.3 | 72.4 | 24.4 | 70.1 |
| Consumer, brands & media | 4 | 31.0 | 72.3 | 25.4 | 71.7 |
| Legal & compliance | 5 | 31.2 | 71.8 | 26.0 | 72.4 |
| Agriculture & food security | 6 | 36.3 | 71.4 | 26.6 | 68.8 |
| Energy & climate | 8 | 31.0 | 71.3 | 25.9 | 66.0 |
| Company & competitive intelligence | 8 | 28.5 | 71.2 | 25.1 | 68.8 |
| Policy & regulation | 8 | 31.3 | 71.1 | 27.9 | 68.6 |
| Crime & public safety | 6 | 31.9 | 70.4 | 26.4 | 67.9 |
| Technology & AI | 8 | 31.1 | 70.2 | 26.5 | 69.0 |
| Journalism & fact-checking | 6 | 37.4 | 62.9 | 32.0 | 64.2 |

## By pattern

| Pattern | Scenarios | Claude alone | Claude + Prism | ChatGPT alone | ChatGPT + Prism |
|---|---|---|---|---|---|
| `stance` | 10 | 34.6 | 79.8 | 23.1 | 71.6 |
| `trending` | 2 | 24.9 | 77.6 | 26.1 | 70.9 |
| `pulse` | 29 | 31.2 | 73.2 | 24.3 | 70.8 |
| `brief` | 6 | 31.2 | 73.0 | 33.2 | 69.4 |
| `geo` | 6 | 30.0 | 72.7 | 29.2 | 64.9 |
| `evidence` | 17 | 33.1 | 72.3 | 30.3 | 72.4 |
| `radar` | 11 | 34.4 | 71.8 | 26.1 | 68.9 |
| `history` | 4 | 28.6 | 70.7 | 25.9 | 70.2 |
| `citations` | 2 | 37.3 | 69.7 | 37.7 | 69.2 |
| `library` | 1 | 45.1 | 69.2 | 40.7 | 61.7 |
| `compare` | 15 | 29.6 | 69.1 | 25.6 | 65.2 |
| `claims` | 3 | 26.7 | 67.3 | 32.8 | 60.4 |
| `table` | 3 | 32.9 | 63.2 | 28.3 | 60.5 |
| `audit` | 2 | 25.4 | 63.0 | 34.6 | 62.4 |
| `improve` | 2 | 50.4 | 61.0 | 37.4 | 56.3 |

## Where memory beat Prism

In no scenario did a memory-only answer match the best Prism answer.

## Every scenario

| Scenario | Category | Claude alone | Claude + Prism | ChatGPT alone | ChatGPT + Prism | Details |
|---|---|---|---|---|---|---|
| Does metformin lower cancer risk? | Medical & clinical evidence | 39.3 | 71.8 | 29.1 | 73.7 | [page](results/full/metformin-cancer-risk/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/metformin-cancer-risk.pdf) |
| GLP-1 drugs and muscle loss | Medical & clinical evidence | 40.4 | 67.7 | 31.6 | 65.9 | [page](results/full/glp1-weight-loss-muscle/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/glp1-weight-loss-muscle.pdf) |
| Vitamin D and depression | Medical & clinical evidence | 21.5 | 71.4 | 26.3 | 80.2 | [page](results/full/vitamin-d-depression/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/vitamin-d-depression.pdf) |
| Statins and dementia risk | Medical & clinical evidence | 33.1 | 77.8 | 29.1 | 51.7 | [page](results/full/statins-dementia/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/statins-dementia.pdf) |
| How intermittent-fasting research is framed | Medical & clinical evidence | 32.7 | 85.8 | 25.1 | 74.5 | [page](results/full/intermittent-fasting-stance/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/intermittent-fasting-stance.pdf) |
| Antimicrobial resistance brief | Medical & clinical evidence | 38.1 | 74.0 | 36.0 | 67.2 | [page](results/full/antimicrobial-resistance-brief/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/antimicrobial-resistance-brief.pdf) |
| Long COVID statistics | Medical & clinical evidence | 38.7 | 61.4 | 23.5 | 68.9 | [page](results/full/long-covid-statistics/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/long-covid-statistics.pdf) |
| Alzheimer's drug research radar | Medical & clinical evidence | 39.7 | 70.2 | 37.2 | 74.0 | [page](results/full/alzheimers-drugs-radar/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/alzheimers-drugs-radar.pdf) |
| Ozempic in the news | Medical & clinical evidence | 32.3 | 80.4 | 28.7 | 71.9 | [page](results/full/ozempic-news-pulse/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/ozempic-news-pulse.pdf) |
| Immunotherapy evidence table | Medical & clinical evidence | 25.6 | 68.8 | 27.4 | 62.7 | [page](results/full/cancer-immunotherapy-table/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/cancer-immunotherapy-table.pdf) |
| Measles resurgence coverage | Public health & epidemiology | 35.5 | 73.0 | 23.2 | 77.1 | [page](results/full/measles-outbreak-pulse/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/measles-outbreak-pulse.pdf) |
| Where dengue is studied vs reported | Public health & epidemiology | 29.6 | 80.2 | 29.5 | 56.2 | [page](results/full/dengue-geography/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/dengue-geography.pdf) |
| H5N1 bird flu coverage | Public health & epidemiology | 34.0 | 73.7 | 21.2 | 63.2 | [page](results/full/bird-flu-h5n1/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/bird-flu-h5n1.pdf) |
| Air pollution and mortality | Public health & epidemiology | 25.4 | 65.2 | 24.1 | 79.1 | [page](results/full/air-pollution-mortality/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/air-pollution-mortality.pdf) |
| Childhood obesity in India | Public health & epidemiology | 22.0 | 77.2 | 39.8 | 69.1 | [page](results/full/obesity-children-india/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/obesity-children-india.pdf) |
| Social media and teen mental health | Public health & epidemiology | 35.3 | 73.2 | 27.7 | 71.4 | [page](results/full/mental-health-teens-social-media/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/mental-health-teens-social-media.pdf) |
| Vaccine hesitancy research trend | Public health & epidemiology | 26.4 | 76.0 | 25.7 | 69.9 | [page](results/full/vaccine-hesitancy-trend/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/vaccine-hesitancy-trend.pdf) |
| Gold price narrative | Finance & markets | 32.2 | 66.8 | 27.2 | 69.8 | [page](results/full/gold-price-pulse/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/gold-price-pulse.pdf) |
| Inflation vs recession in the news | Finance & markets | 31.1 | 82.4 | 34.2 | 58.0 | [page](results/full/inflation-vs-recession/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/inflation-vs-recession.pdf) |
| Bitcoin ETF coverage | Finance & markets | 29.1 | 73.7 | 31.1 | 64.3 | [page](results/full/crypto-etf-pulse/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/crypto-etf-pulse.pdf) |
| RBI repo rate coverage | Finance & markets | 35.9 | 74.5 | 24.4 | 73.8 | [page](results/full/rbi-repo-rate/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/rbi-repo-rate.pdf) |
| ESG investing research framing | Finance & markets | 30.9 | 84.6 | 26.2 | 68.0 | [page](results/full/esg-investing-stance/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/esg-investing-stance.pdf) |
| Private credit research radar | Finance & markets | 32.4 | 71.5 | 29.4 | 71.3 | [page](results/full/private-credit-radar/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/private-credit-radar.pdf) |
| Tariffs and stock markets | Finance & markets | 34.6 | 75.7 | 24.3 | 62.1 | [page](results/full/tariffs-markets/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/tariffs-markets.pdf) |
| Do interest rates drive house prices? | Finance & markets | 36.8 | 68.5 | 35.1 | 66.7 | [page](results/full/housing-prices-evidence/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/housing-prices-evidence.pdf) |
| What is trending in business news | Finance & markets | 26.2 | 79.9 | 25.7 | 80.2 | [page](results/full/fintech-trending/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/fintech-trending.pdf) |
| NVIDIA media intelligence | Company & competitive intelligence | 26.9 | 75.2 | 24.0 | 70.2 | [page](results/full/nvidia-pulse/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/nvidia-pulse.pdf) |
| Tesla vs BYD | Company & competitive intelligence | 26.7 | 40 | 25.8 | 78.6 | [page](results/full/tesla-vs-byd/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/tesla-vs-byd.pdf) |
| OpenAI vs Anthropic vs Google DeepMind | Company & competitive intelligence | 26.7 | 70.8 | 26.8 | 73.8 | [page](results/full/openai-anthropic-google/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/openai-anthropic-google.pdf) |
| Boeing crisis coverage | Company & competitive intelligence | 27.4 | 77.4 | 21.4 | 65.9 | [page](results/full/boeing-crisis/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/boeing-crisis.pdf) |
| Reliance Jio coverage | Company & competitive intelligence | 28.2 | 76.7 | 29.0 | 63.0 | [page](results/full/reliance-jio/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/reliance-jio.pdf) |
| Zomato vs Swiggy | Company & competitive intelligence | 22.1 | 76.0 | 23.8 | 58.3 | [page](results/full/zomato-swiggy/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/zomato-swiggy.pdf) |
| mRNA beyond COVID | Company & competitive intelligence | 36.0 | 78.2 | 25.2 | 68.8 | [page](results/full/pfizer-pipeline-radar/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/pfizer-pipeline-radar.pdf) |
| Apple tone vs the baseline | Company & competitive intelligence | 33.9 | 74.9 | 24.8 | 71.6 | [page](results/full/apple-sentiment/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/apple-sentiment.pdf) |
| AI regulation coverage | Policy & regulation | 28.8 | 77.6 | 21.9 | 70.0 | [page](results/full/ai-regulation-pulse/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/ai-regulation-pulse.pdf) |
| Universal basic income evidence | Policy & regulation | 37.6 | 71.9 | 34.9 | 67.2 | [page](results/full/ubi-evidence/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/ubi-evidence.pdf) |
| Minimum wage and jobs | Policy & regulation | 26.0 | 69.3 | 32.3 | 64.8 | [page](results/full/minimum-wage-employment/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/minimum-wage-employment.pdf) |
| Carbon tax research framing | Policy & regulation | 33.7 | 80.7 | 25.3 | 78.1 | [page](results/full/carbon-tax-stance/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/carbon-tax-stance.pdf) |
| GST in Indian news | Policy & regulation | 31.2 | 80.3 | 22.0 | 68.7 | [page](results/full/gst-india-pulse/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/gst-india-pulse.pdf) |
| Immigration policy coverage | Policy & regulation | 30.8 | 68.7 | 22.8 | 64.1 | [page](results/full/immigration-us-trend/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/immigration-us-trend.pdf) |
| Smart Cities Mission brief | Policy & regulation | 34.7 | 65.3 | 35.8 | 71.4 | [page](results/full/smart-cities-india-brief/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/smart-cities-india-brief.pdf) |
| Data protection law geography | Policy & regulation | 27.9 | 55.2 | 27.9 | 64.4 | [page](results/full/data-protection-geo/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/data-protection-geo.pdf) |
| Cybercrime coverage | Crime & public safety | 28.7 | 69.6 | 20.1 | 68.6 | [page](results/full/cybercrime-pulse/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/cybercrime-pulse.pdf) |
| Digital arrest scams in India | Crime & public safety | 28.6 | 61.5 | 23.8 | 74.8 | [page](results/full/digital-arrest-scam/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/digital-arrest-scam.pdf) |
| Do body cameras reduce police use of force? | Crime & public safety | 38.7 | 82.3 | 26.3 | 76.4 | [page](results/full/policing-body-cameras/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/policing-body-cameras.pdf) |
| Drug trafficking geography | Crime & public safety | 33.2 | 75.2 | 28.0 | 63.5 | [page](results/full/drug-trafficking-geo/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/drug-trafficking-geo.pdf) |
| Fraud vs theft vs violence in the news | Crime & public safety | 21.8 | 56.5 | 25.5 | 48.5 | [page](results/full/crime-safety-compare/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/crime-safety-compare.pdf) |
| Deepfake fraud research radar | Crime & public safety | 40.2 | 77.4 | 34.9 | 75.4 | [page](results/full/deepfake-fraud-radar/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/deepfake-fraud-radar.pdf) |
| Drone warfare coverage | Defence & geopolitics | 27.0 | 69.3 | 23.6 | 68.1 | [page](results/full/drone-warfare-pulse/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/drone-warfare-pulse.pdf) |
| Hypersonic weapons research | Defence & geopolitics | 31.6 | 76.4 | 26.6 | 72.1 | [page](results/full/hypersonic-radar/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/hypersonic-radar.pdf) |
| NATO vs Russia vs Ukraine attention | Defence & geopolitics | 32.8 | 70.8 | 27.0 | 61.0 | [page](results/full/nato-russia-ukraine/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/nato-russia-ukraine.pdf) |
| India defence exports | Defence & geopolitics | 22.0 | 74.8 | 21.3 | 74.2 | [page](results/full/india-defence-exports/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/india-defence-exports.pdf) |
| South China Sea tensions | Defence & geopolitics | 29.2 | 69.6 | 26.3 | 77.9 | [page](results/full/south-china-sea/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/south-china-sea.pdf) |
| Military AI research framing | Defence & geopolitics | 33.0 | 73.6 | 18.2 | 72.8 | [page](results/full/military-ai-stance/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/military-ai-stance.pdf) |
| Cyber warfare geography | Defence & geopolitics | 29.4 | 72.4 | 27.7 | 64.5 | [page](results/full/cyber-warfare-geo/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/cyber-warfare-geo.pdf) |
| Solar power coverage | Energy & climate | 27.2 | 67.6 | 23.8 | 72.3 | [page](results/full/solar-power-pulse/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/solar-power-pulse.pdf) |
| Green hydrogen research radar | Energy & climate | 27.9 | 66.0 | 22.2 | 63.8 | [page](results/full/green-hydrogen-radar/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/green-hydrogen-radar.pdf) |
| EV battery chemistries table | Energy & climate | 32.0 | 50.6 | 28.0 | 55.8 | [page](results/full/ev-battery-table/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/ev-battery-table.pdf) |
| Small modular reactor framing | Energy & climate | 30.6 | 75.1 | 24.4 | 61.0 | [page](results/full/nuclear-smr-stance/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/nuclear-smr-stance.pdf) |
| Heatwaves and mortality | Energy & climate | 36.1 | 76.5 | 25.8 | 65.0 | [page](results/full/heatwave-mortality/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/heatwave-mortality.pdf) |
| Oil vs renewables in the news | Energy & climate | 33.3 | 77.9 | 23.6 | 72.0 | [page](results/full/oil-vs-renewables/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/oil-vs-renewables.pdf) |
| Carbon capture brief | Energy & climate | 36.5 | 78.3 | 30.1 | 65.0 | [page](results/full/carbon-capture-brief/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/carbon-capture-brief.pdf) |
| Climate finance geography | Energy & climate | 24.5 | 78.4 | 28.9 | 72.7 | [page](results/full/climate-finance-geo/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/climate-finance-geo.pdf) |
| Generative AI in education | Technology & AI | 36.7 | 82.0 | 21.4 | 76.5 | [page](results/full/gen-ai-education-stance/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/gen-ai-education-stance.pdf) |
| Quantum computing research radar | Technology & AI | 37.5 | 70.2 | 21.4 | 59.5 | [page](results/full/quantum-computing-radar/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/quantum-computing-radar.pdf) |
| AI agents in the news | Technology & AI | 34.5 | 79.3 | 25.5 | 74.7 | [page](results/full/ai-agents-pulse/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/ai-agents-pulse.pdf) |
| Do LLMs hallucinate citations? | Technology & AI | 22.0 | 65.6 | 26.8 | 68.9 | [page](results/full/llm-hallucination-evidence/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/llm-hallucination-evidence.pdf) |
| Chips race in the news | Technology & AI | 32.0 | 74.2 | 25.7 | 70.0 | [page](results/full/semiconductors-compare/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/semiconductors-compare.pdf) |
| Humanoid robot research trend | Technology & AI | 26.8 | 40 | 31.6 | 72.9 | [page](results/full/humanoid-robots-history/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/humanoid-robots-history.pdf) |
| 6G research geography | Technology & AI | 35.4 | 74.6 | 33.0 | 68.0 | [page](results/full/6g-research-geo/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/6g-research-geo.pdf) |
| Rising topics in tech news | Technology & AI | 23.6 | 75.3 | 26.5 | 61.6 | [page](results/full/cybersecurity-trending/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/cybersecurity-trending.pdf) |
| Millets in Indian news | Agriculture & food security | 37.3 | 71.5 | 28.3 | 73.3 | [page](results/full/millets-india-pulse/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/millets-india-pulse.pdf) |
| Does glyphosate cause cancer? | Agriculture & food security | 32.6 | 72.3 | 34.4 | 67.6 | [page](results/full/glyphosate-cancer/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/glyphosate-cancer.pdf) |
| Precision agriculture research radar | Agriculture & food security | 32.3 | 70.8 | 24.7 | 64.6 | [page](results/full/precision-farming-radar/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/precision-farming-radar.pdf) |
| Food prices in the news | Agriculture & food security | 32.0 | 65.0 | 24.1 | 70.0 | [page](results/full/food-inflation-compare/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/food-inflation-compare.pdf) |
| Climate impact on crop yields | Agriculture & food security | 41.1 | 70.1 | 29.4 | 62.9 | [page](results/full/crop-yields-climate-table/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/crop-yields-climate-table.pdf) |
| Organic farming research framing | Agriculture & food security | 42.6 | 78.8 | 18.8 | 74.6 | [page](results/full/organic-farming-stance/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/organic-farming-stance.pdf) |
| Does remote work hurt productivity? | Education & labour | 31.5 | 73.4 | 32.2 | 74.0 | [page](results/full/remote-work-productivity/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/remote-work-productivity.pdf) |
| Layoffs in the news | Education & labour | 32.7 | 80.7 | 25.4 | 63.0 | [page](results/full/layoffs-pulse/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/layoffs-pulse.pdf) |
| National Education Policy brief | Education & labour | 24.9 | 71.6 | 32.6 | 73.0 | [page](results/full/nep-2020-brief/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/nep-2020-brief.pdf) |
| AI and jobs research framing | Education & labour | 38.5 | 77.3 | 11.3 | 67.4 | [page](results/full/ai-jobs-stance/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/ai-jobs-stance.pdf) |
| Edtech in the news | Education & labour | 34.3 | 74.8 | 27.4 | 73.4 | [page](results/full/edtech-compare/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/edtech-compare.pdf) |
| Google antitrust coverage | Legal & compliance | 31.0 | 68.3 | 22.7 | 70.5 | [page](results/full/antitrust-big-tech/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/antitrust-big-tech.pdf) |
| Supreme Court of India coverage | Legal & compliance | 31.8 | 77.5 | 23.6 | 72.6 | [page](results/full/supreme-court-india/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/supreme-court-india.pdf) |
| GDPR enforcement research | Legal & compliance | 33.9 | 60.0 | 24.5 | 68.9 | [page](results/full/gdpr-fines-radar/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/gdpr-fines-radar.pdf) |
| AI copyright lawsuits | Legal & compliance | 30.9 | 79.3 | 18.2 | 72.5 | [page](results/full/copyright-ai-pulse/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/copyright-ai-pulse.pdf) |
| Does the death penalty deter crime? | Legal & compliance | 28.3 | 73.8 | 41.2 | 77.7 | [page](results/full/death-penalty-deterrence/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/death-penalty-deterrence.pdf) |
| Red Sea shipping disruption | Supply chain & trade | 29.6 | 72.4 | 24.8 | 70.5 | [page](results/full/red-sea-shipping/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/red-sea-shipping.pdf) |
| Rare earths vs lithium vs cobalt | Supply chain & trade | 31.1 | 63.9 | 22.2 | 65.8 | [page](results/full/rare-earths-compare/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/rare-earths-compare.pdf) |
| Nearshoring research radar | Supply chain & trade | 30.8 | 79.6 | 20.6 | 71.1 | [page](results/full/nearshoring-radar/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/nearshoring-radar.pdf) |
| Chip shortage research trend | Supply chain & trade | 30.2 | 86.0 | 23.4 | 70.5 | [page](results/full/semiconductor-shortage-history/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/semiconductor-shortage-history.pdf) |
| Container freight rates | Supply chain & trade | 33.6 | 68.7 | 25.6 | 79.2 | [page](results/full/container-freight-pulse/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/container-freight-pulse.pdf) |
| Audit a health article draft | Journalism & fact-checking | 18.1 | 58.0 | 33.3 | 67.7 | [page](results/full/audit-coffee-draft/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/audit-coffee-draft.pdf) |
| Audit an EV explainer | Journalism & fact-checking | 32.7 | 68.1 | 35.9 | 57.1 | [page](results/full/audit-ev-draft/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/audit-ev-draft.pdf) |
| Fix an overstated claim | Journalism & fact-checking | 49.7 | 59.3 | 44.5 | 53.4 | [page](results/full/improve-microplastics/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/improve-microplastics.pdf) |
| Fix a screen-time claim | Journalism & fact-checking | 51.0 | 62.8 | 30.3 | 59.3 | [page](results/full/improve-screen-time/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/improve-screen-time.pdf) |
| Citations for a sugar-tax story | Journalism & fact-checking | 39.4 | 66.4 | 23.6 | 78.5 | [page](results/full/citations-sugar-tax/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/citations-sugar-tax.pdf) |
| Election misinformation coverage | Journalism & fact-checking | 33.2 | 62.9 | 24.4 | 69.3 | [page](results/full/election-misinformation-pulse/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/election-misinformation-pulse.pdf) |
| Gut microbiome and depression literature | Academic research & literature review | 36.7 | 81.5 | 35.5 | 72.9 | [page](results/full/microbiome-depression-stance/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/microbiome-depression-stance.pdf) |
| What is my AI-ethics reading list missing? | Academic research & literature review | 45.1 | 69.2 | 40.7 | 61.7 | [page](results/full/library-gaps-ai-ethics/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/library-gaps-ai-ethics.pdf) |
| Vancouver citations for exercise and depression | Academic research & literature review | 35.2 | 73.0 | 51.8 | 60.0 | [page](results/full/citations-exercise-depression/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/citations-exercise-depression.pdf) |
| CRISPR research trend | Academic research & literature review | 30.8 | 80.9 | 23.0 | 67.5 | [page](results/full/crispr-history/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/crispr-history.pdf) |
| Microfinance: empowerment or debt trap? | Academic research & literature review | 21.1 | 54.9 | 37.1 | 64.8 | [page](results/full/microfinance-claims/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/microfinance-claims.pdf) |
| Mindfulness research framing | Academic research & literature review | 30.6 | 78.2 | 24.8 | 69.8 | [page](results/full/mindfulness-stance/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/mindfulness-stance.pdf) |
| Microplastics in the news | Environment & disasters | 38.7 | 73.4 | 24.4 | 70.6 | [page](results/full/microplastics-pulse/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/microplastics-pulse.pdf) |
| Groundwater depletion in India | Environment & disasters | 30.7 | 71.8 | 25.1 | 70.5 | [page](results/full/groundwater-india-brief/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/groundwater-india-brief.pdf) |
| Floods vs heatwaves vs wildfires | Environment & disasters | 27.0 | 75.1 | 28.0 | 57.6 | [page](results/full/floods-vs-heatwaves/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/floods-vs-heatwaves.pdf) |
| PFAS and health | Environment & disasters | 38.1 | 81.6 | 41.4 | 77.5 | [page](results/full/pfas-evidence/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/pfas-evidence.pdf) |
| Coral bleaching research radar | Environment & disasters | 36.1 | 69.8 | 20.1 | 68.2 | [page](results/full/coral-bleaching-radar/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/coral-bleaching-radar.pdf) |
| Does ashwagandha reduce stress? | Consumer, brands & media | 25.8 | 75.1 | 27.2 | 74.4 | [page](results/full/ashwagandha-evidence/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/ashwagandha-evidence.pdf) |
| Netflix vs Disney+ vs Prime Video | Consumer, brands & media | 28.3 | 64.3 | 23.5 | 64.5 | [page](results/full/streaming-compare/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/streaming-compare.pdf) |
| Quick commerce in India | Consumer, brands & media | 34.6 | 72.8 | 23.5 | 71.0 | [page](results/full/quick-commerce-pulse/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/quick-commerce-pulse.pdf) |
| Ultra-processed food and health | Consumer, brands & media | 35.2 | 77.2 | 27.3 | 76.9 | [page](results/full/ultra-processed-food/README.md) · [PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/ultra-processed-food.pdf) |

## Method

- Rubric: `benchmarks/rubric/benchmark_rubric.json` (and `.md` for the reasoning), 11 parameters, weights per pattern.
- Harness: `benchmarks/bench.py` (prompts, ground pass, judges, renderer), `benchmarks/bench_full.py` (this run), `benchmarks/bench_summary.py` (this page).
- Prism setups received the scenario's recorded Prism calls in full (`docs/examples/<slug>.json`), so retrieval is held constant; deep live-MCP tiers are in `benchmarks/bench_deep.py`.
- Gates: an unsourced chart, table or verdict number caps a deliverable at 40; the 'no gates' row shows scores without it.

Summary PDF: [https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/summary.pdf](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/summary.pdf)
