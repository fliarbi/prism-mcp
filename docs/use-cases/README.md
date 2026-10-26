# Prism MCP: use cases

[Prism MCP](../../README.md) · [How the benchmark works](../../benchmarks/README.md) · [Research analysis](../RESEARCH_ANALYSIS.md) · [Data export](../DATA_EXPORT.md)

121 demonstrations across 18 domains. Every page runs real Prism tools against the live corpora, saves the raw responses, draws its charts from them, and puts Claude and ChatGPT side by side with and without Prism.

## [Companies, people & places](entities/README.md)

Any company, person, place or phrase as a measured news entity: attention, tone, themes, the people and places around it, and how it compares with its rivals.

| Demonstration | Pattern | Best with Prism vs best alone (/100) |
| --- | --- | ---: |
| [Narendra Modi vs Donald Trump in the news](entities/modi-vs-trump.md) | news comparison | – |
| [Reliance Industries: media intelligence](entities/reliance-industries-pulse.md) | news pulse | – |
| [Infosys vs TCS vs Wipro](entities/infosys-tcs-wipro.md) | news comparison | – |
| [HDFC Bank: media intelligence](entities/hdfc-bank-pulse.md) | news pulse | – |
| [Tata Motors: media intelligence](entities/tata-motors-pulse.md) | news pulse | – |
| [Bengaluru as a news entity](entities/bengaluru-pulse.md) | news pulse | – |
| [Mumbai vs Delhi vs Bengaluru](entities/mumbai-delhi-bengaluru.md) | news comparison | – |
| [ISRO: media intelligence](entities/isro-pulse.md) | news pulse | – |

## [Medical & clinical evidence](medical/README.md)

Drug, therapy and risk-factor questions answered from 41M the health literature index records and 55M extracted disease-factor claims, tiered by study design.

| Demonstration | Pattern | Best with Prism vs best alone (/100) |
| --- | --- | ---: |
| [Does metformin lower cancer risk?](medical/metformin-cancer-risk.md) | evidence + counter-evidence | 73.7 vs 39.3 |
| [GLP-1 drugs and muscle loss](medical/glp1-weight-loss-muscle.md) | evidence + counter-evidence | 67.7 vs 40.4 |
| [Vitamin D and depression](medical/vitamin-d-depression.md) | evidence + counter-evidence | 80.2 vs 26.3 |
| [Statins and dementia risk](medical/statins-dementia.md) | claim vs claim | 77.8 vs 33.1 |
| [How intermittent-fasting research is framed](medical/intermittent-fasting-stance.md) | stance trend | 85.8 vs 32.7 |
| [Antimicrobial resistance brief](medical/antimicrobial-resistance-brief.md) | research brief | 74.0 vs 38.1 |
| [Long COVID statistics](medical/long-covid-statistics.md) | evidence + counter-evidence | 68.9 vs 38.7 |
| [Alzheimer's drug research radar](medical/alzheimers-drugs-radar.md) | research radar | 74.0 vs 39.7 |
| [Ozempic in the news](medical/ozempic-news-pulse.md) | news pulse | 80.4 vs 32.3 |
| [Immunotherapy evidence table](medical/cancer-immunotherapy-table.md) | evidence table / export | 68.8 vs 27.4 |

## [Public health & epidemiology](public-health/README.md)

Outbreak coverage, health-system pressure and population risk, read from news and research together.

| Demonstration | Pattern | Best with Prism vs best alone (/100) |
| --- | --- | ---: |
| [Measles resurgence coverage](public-health/measles-outbreak-pulse.md) | news pulse | 77.1 vs 35.5 |
| [Where dengue is studied vs reported](public-health/dengue-geography.md) | geography | 80.2 vs 29.6 |
| [H5N1 bird flu coverage](public-health/bird-flu-h5n1.md) | news pulse | 73.7 vs 34.0 |
| [Air pollution and mortality](public-health/air-pollution-mortality.md) | evidence + counter-evidence | 79.1 vs 25.4 |
| [Childhood obesity in India](public-health/obesity-children-india.md) | research brief | 77.2 vs 39.8 |
| [Social media and teen mental health](public-health/mental-health-teens-social-media.md) | evidence + counter-evidence | 73.2 vs 35.3 |
| [Vaccine hesitancy research trend](public-health/vaccine-hesitancy-trend.md) | history + scenarios | 76.0 vs 26.4 |

## [Finance & markets](finance/README.md)

Market narratives, macro signals and sector sentiment measured over 255M news articles, not recalled from training data.

| Demonstration | Pattern | Best with Prism vs best alone (/100) |
| --- | --- | ---: |
| [Gold price narrative](finance/gold-price-pulse.md) | news pulse | 69.8 vs 32.2 |
| [Inflation vs recession in the news](finance/inflation-vs-recession.md) | news comparison | 82.4 vs 34.2 |
| [Bitcoin ETF coverage](finance/crypto-etf-pulse.md) | news pulse | 73.7 vs 31.1 |
| [RBI repo rate coverage](finance/rbi-repo-rate.md) | news pulse | 74.5 vs 35.9 |
| [ESG investing research framing](finance/esg-investing-stance.md) | stance trend | 84.6 vs 30.9 |
| [Private credit research radar](finance/private-credit-radar.md) | research radar | 71.5 vs 32.4 |
| [Tariffs and stock markets](finance/tariffs-markets.md) | news comparison | 75.7 vs 34.6 |
| [Do interest rates drive house prices?](finance/housing-prices-evidence.md) | evidence + counter-evidence | 68.5 vs 36.8 |
| [What is trending in business news](finance/fintech-trending.md) | trending scan | 80.2 vs 26.2 |

## [Company & competitive intelligence](company/README.md)

What the world is saying about a company or a rival set: attention, tone, themes, the people and places around it.

| Demonstration | Pattern | Best with Prism vs best alone (/100) |
| --- | --- | ---: |
| [NVIDIA media intelligence](company/nvidia-pulse.md) | news pulse | 75.2 vs 26.9 |
| [Tesla vs BYD](company/tesla-vs-byd.md) | news comparison | 78.6 vs 26.7 |
| [OpenAI vs Anthropic vs Google DeepMind](company/openai-anthropic-google.md) | news comparison | 73.8 vs 26.8 |
| [Boeing crisis coverage](company/boeing-crisis.md) | news pulse | 77.4 vs 27.4 |
| [Reliance Jio coverage](company/reliance-jio.md) | news pulse | 76.7 vs 29.0 |
| [Zomato vs Swiggy](company/zomato-swiggy.md) | news comparison | 76.0 vs 23.8 |
| [mRNA beyond COVID](company/pfizer-pipeline-radar.md) | research radar | 78.2 vs 36.0 |
| [Apple tone vs the baseline](company/apple-sentiment.md) | news pulse | 74.9 vs 33.9 |

## [Policy & regulation](policy/README.md)

How a policy is covered, contested and studied, with the evidence base behind each side.

| Demonstration | Pattern | Best with Prism vs best alone (/100) |
| --- | --- | ---: |
| [AI regulation coverage](policy/ai-regulation-pulse.md) | news pulse | 77.6 vs 28.8 |
| [Universal basic income evidence](policy/ubi-evidence.md) | evidence + counter-evidence | 71.9 vs 37.6 |
| [Minimum wage and jobs](policy/minimum-wage-employment.md) | claim vs claim | 69.3 vs 32.3 |
| [Carbon tax research framing](policy/carbon-tax-stance.md) | stance trend | 80.7 vs 33.7 |
| [GST in Indian news](policy/gst-india-pulse.md) | news pulse | 80.3 vs 31.2 |
| [Immigration policy coverage](policy/immigration-us-trend.md) | news comparison | 68.7 vs 30.8 |
| [Smart Cities Mission brief](policy/smart-cities-india-brief.md) | research brief | 71.4 vs 35.8 |
| [Data protection law geography](policy/data-protection-geo.md) | geography | 64.4 vs 27.9 |

## [Crime & public safety](crime/README.md)

Crime and safety narratives by geography and over time, with the critical stories separated from the noise.

| Demonstration | Pattern | Best with Prism vs best alone (/100) |
| --- | --- | ---: |
| [Cybercrime coverage](crime/cybercrime-pulse.md) | news pulse | 69.6 vs 28.7 |
| [Digital arrest scams in India](crime/digital-arrest-scam.md) | news pulse | 74.8 vs 28.6 |
| [Do body cameras reduce police use of force?](crime/policing-body-cameras.md) | evidence + counter-evidence | 82.3 vs 38.7 |
| [Drug trafficking geography](crime/drug-trafficking-geo.md) | geography | 75.2 vs 33.2 |
| [Fraud vs theft vs violence in the news](crime/crime-safety-compare.md) | news comparison | 56.5 vs 25.5 |
| [Deepfake fraud research radar](crime/deepfake-fraud-radar.md) | research radar | 77.4 vs 40.2 |

## [Defence & geopolitics](defence/README.md)

Conflict, deterrence and defence-industrial signals across news, research and patents.

| Demonstration | Pattern | Best with Prism vs best alone (/100) |
| --- | --- | ---: |
| [Drone warfare coverage](defence/drone-warfare-pulse.md) | news pulse | 69.3 vs 27.0 |
| [Hypersonic weapons research](defence/hypersonic-radar.md) | research radar | 76.4 vs 31.6 |
| [NATO vs Russia vs Ukraine attention](defence/nato-russia-ukraine.md) | news comparison | 70.8 vs 32.8 |
| [India defence exports](defence/india-defence-exports.md) | news pulse | 74.8 vs 22.0 |
| [South China Sea tensions](defence/south-china-sea.md) | news pulse | 77.9 vs 29.2 |
| [Military AI research framing](defence/military-ai-stance.md) | stance trend | 73.6 vs 33.0 |
| [Cyber warfare geography](defence/cyber-warfare-geo.md) | geography | 72.4 vs 29.4 |

## [Energy & climate](energy-climate/README.md)

Transition technologies, climate risk and energy security, measured across all four corpora.

| Demonstration | Pattern | Best with Prism vs best alone (/100) |
| --- | --- | ---: |
| [Solar power coverage](energy-climate/solar-power-pulse.md) | news pulse | 72.3 vs 27.2 |
| [Green hydrogen research radar](energy-climate/green-hydrogen-radar.md) | research radar | 66.0 vs 27.9 |
| [EV battery chemistries table](energy-climate/ev-battery-table.md) | evidence table / export | 55.8 vs 32.0 |
| [Small modular reactor framing](energy-climate/nuclear-smr-stance.md) | stance trend | 75.1 vs 30.6 |
| [Heatwaves and mortality](energy-climate/heatwave-mortality.md) | evidence + counter-evidence | 76.5 vs 36.1 |
| [Oil vs renewables in the news](energy-climate/oil-vs-renewables.md) | news comparison | 77.9 vs 33.3 |
| [Carbon capture brief](energy-climate/carbon-capture-brief.md) | research brief | 78.3 vs 36.5 |
| [Climate finance geography](energy-climate/climate-finance-geo.md) | geography | 78.4 vs 28.9 |

## [Technology & AI](technology/README.md)

Where a technology is in its hype cycle: research momentum, patent activity, news framing.

| Demonstration | Pattern | Best with Prism vs best alone (/100) |
| --- | --- | ---: |
| [Generative AI in education](technology/gen-ai-education-stance.md) | stance trend | 82.0 vs 36.7 |
| [Quantum computing research radar](technology/quantum-computing-radar.md) | research radar | 70.2 vs 37.5 |
| [AI agents in the news](technology/ai-agents-pulse.md) | news pulse | 79.3 vs 34.5 |
| [Do LLMs hallucinate citations?](technology/llm-hallucination-evidence.md) | evidence + counter-evidence | 68.9 vs 26.8 |
| [Chips race in the news](technology/semiconductors-compare.md) | news comparison | 74.2 vs 32.0 |
| [Humanoid robot research trend](technology/humanoid-robots-history.md) | history + scenarios | 72.9 vs 31.6 |
| [6G research geography](technology/6g-research-geo.md) | geography | 74.6 vs 35.4 |
| [Rising topics in tech news](technology/cybersecurity-trending.md) | trending scan | 75.3 vs 26.5 |

## [Agriculture & food security](agriculture/README.md)

Crops, prices, food safety and farm technology, from the field trials to the headlines.

| Demonstration | Pattern | Best with Prism vs best alone (/100) |
| --- | --- | ---: |
| [Millets in Indian news](agriculture/millets-india-pulse.md) | news pulse | 73.3 vs 37.3 |
| [Does glyphosate cause cancer?](agriculture/glyphosate-cancer.md) | evidence + counter-evidence | 72.3 vs 34.4 |
| [Precision agriculture research radar](agriculture/precision-farming-radar.md) | research radar | 70.8 vs 32.3 |
| [Food prices in the news](agriculture/food-inflation-compare.md) | news comparison | 70.0 vs 32.0 |
| [Climate impact on crop yields](agriculture/crop-yields-climate-table.md) | evidence table / export | 70.1 vs 41.1 |
| [Organic farming research framing](agriculture/organic-farming-stance.md) | stance trend | 78.8 vs 42.6 |

## [Education & labour](education-labour/README.md)

Skills, jobs and learning outcomes, with the research stance separated from the news noise.

| Demonstration | Pattern | Best with Prism vs best alone (/100) |
| --- | --- | ---: |
| [Does remote work hurt productivity?](education-labour/remote-work-productivity.md) | evidence + counter-evidence | 74.0 vs 32.2 |
| [Layoffs in the news](education-labour/layoffs-pulse.md) | news pulse | 80.7 vs 32.7 |
| [National Education Policy brief](education-labour/nep-2020-brief.md) | research brief | 73.0 vs 32.6 |
| [AI and jobs research framing](education-labour/ai-jobs-stance.md) | stance trend | 77.3 vs 38.5 |
| [Edtech in the news](education-labour/edtech-compare.md) | news comparison | 74.8 vs 34.3 |

## [Legal & compliance](legal/README.md)

Litigation, enforcement and regulatory exposure, tracked as coverage and as literature.

| Demonstration | Pattern | Best with Prism vs best alone (/100) |
| --- | --- | ---: |
| [Google antitrust coverage](legal/antitrust-big-tech.md) | news pulse | 70.5 vs 31.0 |
| [Supreme Court of India coverage](legal/supreme-court-india.md) | news pulse | 77.5 vs 31.8 |
| [GDPR enforcement research](legal/gdpr-fines-radar.md) | research radar | 68.9 vs 33.9 |
| [AI copyright lawsuits](legal/copyright-ai-pulse.md) | news pulse | 79.3 vs 30.9 |
| [Does the death penalty deter crime?](legal/death-penalty-deterrence.md) | evidence + counter-evidence | 77.7 vs 41.2 |

## [Supply chain & trade](supply-chain/README.md)

Shortages, tariffs and chokepoints, with the geography of coverage made explicit.

| Demonstration | Pattern | Best with Prism vs best alone (/100) |
| --- | --- | ---: |
| [Red Sea shipping disruption](supply-chain/red-sea-shipping.md) | news pulse | 72.4 vs 29.6 |
| [Rare earths vs lithium vs cobalt](supply-chain/rare-earths-compare.md) | news comparison | 65.8 vs 31.1 |
| [Nearshoring research radar](supply-chain/nearshoring-radar.md) | research radar | 79.6 vs 30.8 |
| [Chip shortage research trend](supply-chain/semiconductor-shortage-history.md) | history + scenarios | 86.0 vs 30.2 |
| [Container freight rates](supply-chain/container-freight-pulse.md) | news pulse | 79.2 vs 33.6 |

## [Journalism & fact-checking](journalism/README.md)

Draft audits, claim checks and better-supported rewrites, with every number traced to a source.

| Demonstration | Pattern | Best with Prism vs best alone (/100) |
| --- | --- | ---: |
| [Audit a health article draft](journalism/audit-coffee-draft.md) | draft audit | 67.7 vs 33.3 |
| [Audit an EV explainer](journalism/audit-ev-draft.md) | draft audit | 68.1 vs 35.9 |
| [Fix an overstated claim](journalism/improve-microplastics.md) | claim rewrite | 59.3 vs 49.7 |
| [Fix a screen-time claim](journalism/improve-screen-time.md) | claim rewrite | 62.8 vs 51.0 |
| [Citations for a sugar-tax story](journalism/citations-sugar-tax.md) | citations | 78.5 vs 39.4 |
| [Election misinformation coverage](journalism/election-misinformation-pulse.md) | news pulse | 69.3 vs 33.2 |

## [Academic research & literature review](academic/README.md)

Literature mapping by stance, citation-ready sources and library gaps for systematic work.

| Demonstration | Pattern | Best with Prism vs best alone (/100) |
| --- | --- | ---: |
| [Gut microbiome and depression literature](academic/microbiome-depression-stance.md) | stance trend | 81.5 vs 36.7 |
| [What is my AI-ethics reading list missing?](academic/library-gaps-ai-ethics.md) | library gaps | 69.2 vs 45.1 |
| [Vancouver citations for exercise and depression](academic/citations-exercise-depression.md) | citations | 73.0 vs 51.8 |
| [CRISPR research trend](academic/crispr-history.md) | history + scenarios | 80.9 vs 30.8 |
| [Microfinance: empowerment or debt trap?](academic/microfinance-claims.md) | claim vs claim | 64.8 vs 37.1 |
| [Mindfulness research framing](academic/mindfulness-stance.md) | stance trend | 78.2 vs 30.6 |

## [Environment & disasters](environment/README.md)

Hazards, pollution and ecosystems, with the coverage window and enrichment lag stated.

| Demonstration | Pattern | Best with Prism vs best alone (/100) |
| --- | --- | ---: |
| [Microplastics in the news](environment/microplastics-pulse.md) | news pulse | 73.4 vs 38.7 |
| [Groundwater depletion in India](environment/groundwater-india-brief.md) | research brief | 71.8 vs 30.7 |
| [Floods vs heatwaves vs wildfires](environment/floods-vs-heatwaves.md) | news comparison | 75.1 vs 28.0 |
| [PFAS and health](environment/pfas-evidence.md) | evidence + counter-evidence | 81.6 vs 41.4 |
| [Coral bleaching research radar](environment/coral-bleaching-radar.md) | research radar | 69.8 vs 36.1 |

## [Consumer, brands & media](consumer-media/README.md)

Brand attention, consumer health claims and media narratives, measured rather than guessed.

| Demonstration | Pattern | Best with Prism vs best alone (/100) |
| --- | --- | ---: |
| [Does ashwagandha reduce stress?](consumer-media/ashwagandha-evidence.md) | evidence + counter-evidence | 75.1 vs 27.2 |
| [Netflix vs Disney+ vs Prime Video](consumer-media/streaming-compare.md) | news comparison | 64.5 vs 28.3 |
| [Quick commerce in India](consumer-media/quick-commerce-pulse.md) | news pulse | 72.8 vs 34.6 |
| [Ultra-processed food and health](consumer-media/ultra-processed-food.md) | evidence + counter-evidence | 77.2 vs 35.2 |

