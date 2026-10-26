"""The showcase catalog: one entry per demonstration page.

Each scenario is a question a real analyst would put to Claude or ChatGPT, the
intelligence requirement behind it, the special case that makes it hard, and the
Prism tool plan that answers it. `capture.py` runs the plan against the live
corpora; `compare.py` asks Claude and ChatGPT the same question with and without
those results; `build_pages.py` turns both into a page.

Patterns (the tool plan a scenario uses):
  pulse      news.overview                         - volume, tone, themes, entities, places, critical headlines
  evidence   research.evidence + counter_evidence + statistics
  stance     research.stance_trends + research.browse(promising)
  brief      research.brief + news.trends
  compare    news.compare (2-4 terms)
  claims     research.compare (two claims)
  radar      research.radar
  table      research.table                        - one question across many rows (spreadsheet/export)
  audit      research.audit                        - whole-draft fact check
  geo        research.geography + news.geography
  trending   news.trending
  history    historical_analysis + trend_scenarios - multi-year series and forward ranges
  citations  research.citations + research.source_ranking
  improve    research.improve + research.evidence_card
"""

CATEGORIES = [
    ("entities", "Companies, people & places", "Any company, person, place or phrase as a measured news entity: attention, tone, themes, the people and places around it, and how it compares with its rivals."),
    ("medical", "Medical & clinical evidence", "Drug, therapy and risk-factor questions answered from 41M PubMed records and 55M extracted disease-factor claims, tiered by study design."),
    ("public-health", "Public health & epidemiology", "Outbreak coverage, health-system pressure and population risk, read from news and research together."),
    ("finance", "Finance & markets", "Market narratives, macro signals and sector sentiment measured over 255M news articles, not recalled from training data."),
    ("company", "Company & competitive intelligence", "What the world is saying about a company or a rival set: attention, tone, themes, the people and places around it."),
    ("policy", "Policy & regulation", "How a policy is covered, contested and studied, with the evidence base behind each side."),
    ("crime", "Crime & public safety", "Crime and safety narratives by geography and over time, with the critical stories separated from the noise."),
    ("defence", "Defence & geopolitics", "Conflict, deterrence and defence-industrial signals across news, research and patents."),
    ("energy-climate", "Energy & climate", "Transition technologies, climate risk and energy security, measured across all four corpora."),
    ("technology", "Technology & AI", "Where a technology is in its hype cycle: research momentum, patent activity, news framing."),
    ("agriculture", "Agriculture & food security", "Crops, prices, food safety and farm technology, from the field trials to the headlines."),
    ("education-labour", "Education & labour", "Skills, jobs and learning outcomes, with the research stance separated from the news noise."),
    ("legal", "Legal & compliance", "Litigation, enforcement and regulatory exposure, tracked as coverage and as literature."),
    ("supply-chain", "Supply chain & trade", "Shortages, tariffs and chokepoints, with the geography of coverage made explicit."),
    ("journalism", "Journalism & fact-checking", "Draft audits, claim checks and better-supported rewrites, with every number traced to a source."),
    ("academic", "Academic research & literature review", "Literature mapping by stance, citation-ready sources and library gaps for systematic work."),
    ("environment", "Environment & disasters", "Hazards, pollution and ecosystems, with the coverage window and enrichment lag stated."),
    ("consumer-media", "Consumer, brands & media", "Brand attention, consumer health claims and media narratives, measured rather than guessed."),
]

S = []


def add(cat, slug, title, question, requirement, special, pattern, **args):
    # A question that refers to material ("this draft", "my reading list") must
    # carry it, or the model (and the live MCP session) has nothing to check.
    if pattern == "audit":
        question = f"{question}\n\n{args['text']}"
    if pattern == "library":
        question = f"{question}\n\n" + "\n".join(f"- {x}" for x in args["items"])
    S.append(dict(category=cat, slug=slug, title=title, question=question,
                  requirement=requirement, special=special, pattern=pattern, args=args))


# ── medical ─────────────────────────────────────────────────────────────────
add("medical", "metformin-cancer-risk", "Does metformin lower cancer risk?",
    "Does metformin reduce cancer risk in people with type 2 diabetes? How strong is the evidence and what disagrees?",
    "A clinician-grade answer: the meta-analyses, the contrary trials, and the size of the effect.",
    "Observational meta-analyses say yes; randomised trials are weaker. A good answer has to separate the two tiers.",
    "evidence", claim="Metformin reduces cancer risk in diabetic patients")
add("medical", "glp1-weight-loss-muscle", "GLP-1 drugs and muscle loss",
    "Do GLP-1 weight-loss drugs like semaglutide cause significant lean muscle loss?",
    "Quantified evidence on lean-mass loss, with study design and population for each figure.",
    "A fast-moving 2023-2026 literature; model training data ends before most of it.",
    "evidence", claim="Semaglutide causes loss of lean muscle mass")
add("medical", "vitamin-d-depression", "Vitamin D and depression",
    "Is vitamin D supplementation effective for depression?",
    "Separate the trials from the association studies and state the mix of findings.",
    "Hundreds of association papers drown a handful of RCTs; counting them equally gives the wrong answer.",
    "evidence", claim="Vitamin D supplementation reduces depression symptoms")
add("medical", "statins-dementia", "Statins and dementia risk",
    "Do statins protect against dementia, or increase cognitive risk?",
    "Both directions of the claim, weighted by tier.",
    "The literature points both ways; the useful output is the tier-weighted balance, not a yes/no.",
    "claims", claim_a="Statins reduce dementia risk", claim_b="Statins impair cognitive function")
add("medical", "intermittent-fasting-stance", "How intermittent-fasting research is framed",
    "How has research on intermittent fasting shifted in tone over the past years? Is it getting more promising or more cautious?",
    "Year-by-year framing of the literature, plus the most promising recent studies.",
    "Framing is a property of thousands of abstracts, not something a model can recall.",
    "stance", term="intermittent fasting")
add("medical", "antimicrobial-resistance-brief", "Antimicrobial resistance brief",
    "Give me a research brief on antimicrobial resistance: what is established, what is contested, key numbers and trend.",
    "A structured one-page brief built from measurements, ready for a policy memo.",
    "Volumes differ by orders of magnitude between corpora; the brief must say which lane each number is from.",
    "brief", topic="antimicrobial resistance", term="antimicrobial resistance")
add("medical", "long-covid-statistics", "Long COVID statistics",
    "What are the most cited statistics on long COVID prevalence, and where do they come from?",
    "Verbatim figures with the sentence and source each came from.",
    "Prevalence figures range from 5% to 50% depending on definition; a figure without its population is useless.",
    "evidence", claim="Long COVID affects a significant share of people after infection")
add("medical", "alzheimers-drugs-radar", "Alzheimer's drug research radar",
    "What has changed recently in Alzheimer's disease drug research?",
    "New work, momentum and framing shift since 2022.",
    "Lecanemab and donanemab approvals moved the field in 2023-2025, after most models' training data.",
    "radar", topic="alzheimer disease treatment", since_year=2022)
add("medical", "ozempic-news-pulse", "Ozempic in the news",
    "What is the news saying about Ozempic: volume, tone, themes and the critical stories?",
    "A media-intelligence pulse on a blockbuster drug.",
    "Brand, generic and class names (Ozempic, semaglutide, GLP-1) are covered differently.",
    "pulse", term="ozempic")
add("medical", "cancer-immunotherapy-table", "Immunotherapy evidence table",
    "Build me a table: for each cancer type, what does the research say about immunotherapy response rates?",
    "One research question answered across many rows: a spreadsheet you can export.",
    "Each row needs its own source; a single answer pasted into ten rows is a fabrication.",
    "table", rows=["melanoma", "non-small cell lung cancer", "renal cell carcinoma", "bladder cancer", "colorectal cancer", "breast cancer"],
    table_question="immune checkpoint inhibitor response rate")

# ── public health ───────────────────────────────────────────────────────────
add("public-health", "measles-outbreak-pulse", "Measles resurgence coverage",
    "How much measles outbreak coverage has there been, where, and how has it trended?",
    "Outbreak monitoring: volume, geography, critical stories.",
    "The 2025 US and Canadian outbreaks dominate; a global picture needs the geography split.",
    "pulse", term="measles")
add("public-health", "dengue-geography", "Where dengue is studied vs reported",
    "Which countries research dengue most, and which ones does the news cover?",
    "The gap between where a disease is studied and where it is reported.",
    "Research comes from the rich world; outbreaks happen elsewhere. The interesting signal is the mismatch.",
    "geo", claim="Dengue fever outbreaks", term="dengue")
add("public-health", "bird-flu-h5n1", "H5N1 bird flu coverage",
    "What does the news say about H5N1 bird flu in dairy cattle and humans? Is coverage rising?",
    "An early-warning read of a zoonotic threat.",
    "Coverage spikes are driven by single events; the critical-share trend matters more than raw volume.",
    "pulse", term="bird flu")
add("public-health", "air-pollution-mortality", "Air pollution and mortality",
    "How strong is the evidence that PM2.5 air pollution increases mortality? Give numbers.",
    "Effect sizes with sources, for a public-health briefing.",
    "The corpus files this under 'Air Quality and Health Impacts', not 'air pollution'; term discovery matters.",
    "evidence", claim="PM2.5 air pollution increases mortality")
add("public-health", "obesity-children-india", "Childhood obesity in India",
    "Give me a research brief on childhood obesity in India.",
    "A geo-scoped brief: what is studied about India specifically.",
    "A geo scope must be a scope (papers about India), not a keyword (papers mentioning India).",
    "brief", topic="childhood obesity", geo="india", term="childhood obesity")
add("public-health", "mental-health-teens-social-media", "Social media and teen mental health",
    "Does social media use harm adolescent mental health? What does the evidence say, and what disagrees?",
    "Both sides of one of the most contested questions in public health.",
    "Effect sizes are small and contested; an honest answer reports the disagreement.",
    "evidence", claim="Social media use harms adolescent mental health")
add("public-health", "vaccine-hesitancy-trend", "Vaccine hesitancy research trend",
    "How has research on vaccine hesitancy grown, and what range does it project for the next three years?",
    "A measured multi-year series with a forward range.",
    "Post-COVID research spike; a naive extrapolation overstates the trend.",
    "history", subject_phrases=["vaccine hesitancy"], outcome_phrases=None)

# ── finance ─────────────────────────────────────────────────────────────────
add("finance", "gold-price-pulse", "Gold price narrative",
    "What is the news narrative around gold prices: volume, tone, and the critical stories?",
    "Market-narrative intelligence for a commodities desk.",
    "Gold hit records through 2025-2026; tone and criticality move differently from volume.",
    "pulse", term="gold price")
add("finance", "inflation-vs-recession", "Inflation vs recession in the news",
    "Compare news coverage of inflation, recession and interest rates over the last two years.",
    "Which macro fear dominated, and when the narrative turned.",
    "Overlapping terms; the comparison must be on one scale and one window.",
    "compare", terms=["inflation", "recession", "interest rates"])
add("finance", "crypto-etf-pulse", "Bitcoin ETF coverage",
    "How has news coverage of Bitcoin ETFs evolved, and what is the tone?",
    "Product-level narrative tracking for a crypto analyst.",
    "Coverage is concentrated in a few publishers; the source concentration is part of the answer.",
    "pulse", term="bitcoin etf")
add("finance", "rbi-repo-rate", "RBI repo rate coverage",
    "What has the news said about RBI repo rate decisions over the last two years?",
    "Central-bank decision tracking for India.",
    "An acronym-heavy term; the resolver must route it as a topic, not a place.",
    "pulse", term="repo rate")
add("finance", "esg-investing-stance", "ESG investing research framing",
    "Is academic research on ESG investing becoming more critical over time?",
    "The stance trend of a contested investment thesis.",
    "Backlash against ESG is a 2022+ story; the framing shift is the signal.",
    "stance", term="esg investing")
add("finance", "private-credit-radar", "Private credit research radar",
    "What is new in research on private credit markets since 2022?",
    "A radar for an emerging asset class.",
    "Small literature: the honest answer reports how thin it is.",
    "radar", topic="private credit", since_year=2022)
add("finance", "tariffs-markets", "Tariffs and stock markets",
    "Compare news coverage of tariffs vs trade war vs stock market crash.",
    "How tariff policy fed market fear in the news.",
    "2025 tariff announcements created sharp spikes; the comparison must show the timing.",
    "compare", terms=["tariffs", "trade war", "stock market crash"])
add("finance", "housing-prices-evidence", "Do interest rates drive house prices?",
    "How strong is the evidence that rising interest rates lower house prices?",
    "Effect sizes from economics literature.",
    "Economics papers, not medical: tiering has to fall back from RCT logic to study type.",
    "evidence", claim="Rising interest rates reduce house prices")
add("finance", "fintech-trending", "What is trending in business news",
    "What topics are rising fastest in business and finance news right now?",
    "A corpus-wide trend scan, not a single-topic query.",
    "Trending must run on curated subcategories; raw tags surface boilerplate.",
    "trending", days=60, category="business")

# ── company ─────────────────────────────────────────────────────────────────
add("company", "nvidia-pulse", "NVIDIA media intelligence",
    "What is the world saying about NVIDIA: coverage volume, tone, themes, related companies and places?",
    "A full company media profile for an equity analyst.",
    "Entity names are canonical ('nvidia corporation'); matching must be by entity, not word.",
    "pulse", term="nvidia")
add("company", "tesla-vs-byd", "Tesla vs BYD",
    "Compare news coverage of Tesla and BYD over the last two years.",
    "Competitive attention share and tone, one scale.",
    "BYD overtook Tesla in EV sales in 2024-2025; does attention follow sales?",
    "compare", terms=["tesla", "byd"])
add("company", "openai-anthropic-google", "OpenAI vs Anthropic vs Google DeepMind",
    "Compare news attention on OpenAI, Anthropic and Google DeepMind.",
    "AI-lab competitive landscape by coverage.",
    "OpenAI dominates volume; share and growth tell a different story.",
    "compare", terms=["openai", "anthropic", "deepmind"])
add("company", "boeing-crisis", "Boeing crisis coverage",
    "What is the news saying about Boeing, and how negative is it compared with normal news?",
    "Reputation-risk monitoring for a stakeholder.",
    "Tone must be read against the corpus baseline; aviation news is negative by default.",
    "pulse", term="boeing")
add("company", "reliance-jio", "Reliance Jio coverage",
    "What themes and people dominate news coverage of Reliance Jio?",
    "An Indian conglomerate profile: themes, people, places.",
    "Jio IPO speculation and telecom tariffs both drive coverage.",
    "pulse", term="reliance jio")
add("company", "zomato-swiggy", "Zomato vs Swiggy",
    "Compare Zomato and Swiggy in the news.",
    "Indian quick-commerce rivalry by attention.",
    "Zomato renamed its parent to Eternal in 2025; a model may not know.",
    "compare", terms=["zomato", "swiggy"])
add("company", "pfizer-pipeline-radar", "mRNA beyond COVID",
    "What is new in mRNA vaccine research beyond COVID?",
    "Pipeline intelligence for a pharma competitor.",
    "The COVID papers swamp the non-COVID ones; the radar must show the newest work.",
    "radar", topic="mrna vaccine", since_year=2023)
add("company", "apple-sentiment", "Apple tone vs the baseline",
    "Is coverage of Apple more positive or more negative than average news? How has it moved?",
    "A tone benchmark for investor relations.",
    "Product launches create positive spikes; regulation creates negative ones.",
    "pulse", term="apple inc")

# ── policy ──────────────────────────────────────────────────────────────────
add("policy", "ai-regulation-pulse", "AI regulation coverage",
    "How is AI regulation being covered globally? Which countries, which themes, which critical stories?",
    "A policy-landscape read for a public-affairs team.",
    "EU AI Act, US executive orders and India's approach are covered very differently by country.",
    "pulse", term="ai regulation")
add("policy", "ubi-evidence", "Universal basic income evidence",
    "Does universal basic income reduce poverty without reducing work? What does the evidence say?",
    "The trial evidence for a contested policy.",
    "Pilots are small and local; the counter-evidence on labour supply must be shown.",
    "evidence", claim="Universal basic income reduces poverty")
add("policy", "minimum-wage-employment", "Minimum wage and jobs",
    "Do minimum wage increases reduce employment? Compare with the claim that they raise wages without job loss.",
    "Both poles of the classic labour-economics debate.",
    "The literature is genuinely split; tier-weighting is the whole answer.",
    "claims", claim_a="Minimum wage increases reduce employment", claim_b="Minimum wage increases raise earnings without job losses")
add("policy", "carbon-tax-stance", "Carbon tax research framing",
    "Is research on carbon taxes becoming more favourable or more critical?",
    "Stance trend of a flagship climate policy.",
    "Distributional critiques grew after 2018; the trend shows it.",
    "stance", term="carbon tax")
add("policy", "gst-india-pulse", "GST in Indian news",
    "What has the news said about India's GST Council and GST rate changes over the last two years?",
    "Indian tax-policy media tracking.",
    "GST 2.0 rate rationalisation in 2025 changed the tone.",
    "pulse", term="gst council")
add("policy", "immigration-us-trend", "Immigration policy coverage",
    "Compare coverage of immigration, deportation and border security.",
    "The framing of US immigration debate in numbers.",
    "Terms overlap heavily; overlap must be stated.",
    "compare", terms=["immigration", "deportation", "border security"])
add("policy", "smart-cities-india-brief", "Smart Cities Mission brief",
    "Give me a research brief on smart cities in India.",
    "A geo-scoped policy brief.",
    "Many papers mention smart cities generically; India scope must be enforced.",
    "brief", topic="smart cities", geo="india", term="smart cities mission")
add("policy", "data-protection-geo", "Data protection law geography",
    "Where is data protection law studied and reported most?",
    "The geography of a regulatory field.",
    "GDPR dominates research; DPDP Act dominates Indian news.",
    "geo", claim="Data protection regulation", term="data protection")

# ── crime ───────────────────────────────────────────────────────────────────
add("crime", "cybercrime-pulse", "Cybercrime coverage",
    "How much cybercrime coverage is there, where, and what are the critical stories?",
    "A threat-landscape media read.",
    "Ransomware, fraud and data breaches split the coverage; themes separate them.",
    "pulse", term="cybercrime")
add("crime", "digital-arrest-scam", "Digital arrest scams in India",
    "What is being reported about 'digital arrest' scams in India?",
    "An emerging fraud pattern, tracked from first appearance.",
    "A 2024+ phrase that most models have never seen in training.",
    "pulse", term="digital arrest")
add("crime", "policing-body-cameras", "Do body cameras reduce police use of force?",
    "Does police body-worn camera use reduce use of force and complaints?",
    "Trial evidence for a policing intervention.",
    "Early RCTs said yes; the large replication said no effect. Both must appear.",
    "evidence", claim="Police body-worn cameras reduce use of force")
add("crime", "drug-trafficking-geo", "Drug trafficking geography",
    "Where is drug trafficking studied and where is it reported?",
    "The research-vs-news geography of an organised-crime topic.",
    "Place resolution has acronym collisions; the caveat matters.",
    "geo", claim="Drug trafficking", term="drug trafficking")
add("crime", "crime-safety-compare", "Fraud vs theft vs violence in the news",
    "Compare coverage of fraud, robbery and murder over the last two years.",
    "Which crime type dominates attention.",
    "Violent crime dominates criticality even when fraud dominates volume.",
    "compare", terms=["fraud", "robbery", "murder"])
add("crime", "deepfake-fraud-radar", "Deepfake fraud research radar",
    "What has changed in research on deepfake detection and fraud since 2022?",
    "A radar on a fast-moving threat.",
    "Generative AI moved this field in 2023; recency is everything.",
    "radar", topic="deepfake detection", since_year=2022)

# ── defence ─────────────────────────────────────────────────────────────────
add("defence", "drone-warfare-pulse", "Drone warfare coverage",
    "How is drone warfare covered in the news: volume, places, themes and critical stories?",
    "A defence-intelligence media read.",
    "Ukraine, the Middle East and South Asia each carry a distinct drone story.",
    "pulse", term="drone warfare")
add("defence", "hypersonic-radar", "Hypersonic weapons research",
    "What is new in hypersonic missile research?",
    "Research momentum on a strategic technology.",
    "Much of it is in engineering venues, not defence journals.",
    "radar", topic="hypersonic", since_year=2021)
add("defence", "nato-russia-ukraine", "NATO vs Russia vs Ukraine attention",
    "Compare news coverage of NATO, Russia and Ukraine over two years.",
    "The attention balance of the war over time.",
    "Russia and Ukraine co-occur in most articles; overlap is the caveat.",
    "compare", terms=["nato", "russia", "ukraine"])
add("defence", "india-defence-exports", "India defence exports",
    "What is the news saying about India's defence exports?",
    "An industrial-policy read for a defence analyst.",
    "BrahMos deals and record export figures drive positive tone.",
    "pulse", term="defence exports")
add("defence", "south-china-sea", "South China Sea tensions",
    "What is the coverage of the South China Sea: places, tone and the critical stories?",
    "A maritime flashpoint monitor.",
    "Philippine, Vietnamese and Chinese framing differ; geography splits it.",
    "pulse", term="south china sea")
add("defence", "military-ai-stance", "Military AI research framing",
    "Is research on military artificial intelligence becoming more cautionary?",
    "The ethical-framing trend in a sensitive field.",
    "Autonomy debates produce a large critical literature.",
    "stance", term="autonomous weapons")
add("defence", "cyber-warfare-geo", "Cyber warfare geography",
    "Where is cyber warfare studied and reported?",
    "Country-level view of a domain of conflict.",
    "Attribution is political; the geography of coverage is itself a signal.",
    "geo", claim="Cyber warfare", term="cyber warfare")

# ── energy & climate ────────────────────────────────────────────────────────
add("energy-climate", "solar-power-pulse", "Solar power coverage",
    "What does the news say about solar power: trend, tone, places, companies?",
    "A sector pulse for an energy investor.",
    "Product reviews mention 'solar' constantly; centrality matching keeps them out.",
    "pulse", term="solar power")
add("energy-climate", "green-hydrogen-radar", "Green hydrogen research radar",
    "What is new in green hydrogen research since 2022?",
    "Technology momentum for a transition fund.",
    "Electrolyser cost papers vs policy papers move differently.",
    "radar", topic="green hydrogen", since_year=2022)
add("energy-climate", "ev-battery-table", "EV battery chemistries table",
    "For each battery chemistry, what does research say about energy density?",
    "A spreadsheet of one question across chemistries, export-ready.",
    "Each row must carry its own figure and source; null means the corpus does not state one.",
    "table", rows=["lithium iron phosphate", "nickel manganese cobalt", "sodium-ion", "solid-state", "lithium-sulfur"],
    table_question="battery energy density Wh/kg")
add("energy-climate", "nuclear-smr-stance", "Small modular reactor framing",
    "Is research on small modular reactors getting more promising or more cautious?",
    "Framing trend for a nuclear policy team.",
    "SMR cost overruns (NuScale 2023) should show as a cautionary turn.",
    "stance", term="small modular reactor")
add("energy-climate", "heatwave-mortality", "Heatwaves and mortality",
    "How strong is the evidence that heatwaves increase mortality? Give numbers.",
    "Effect sizes for a climate-adaptation plan.",
    "Effect sizes vary hugely by city; population must travel with each number.",
    "evidence", claim="Heatwaves increase mortality")
add("energy-climate", "oil-vs-renewables", "Oil vs renewables in the news",
    "Compare coverage of crude oil, renewable energy and natural gas.",
    "Energy-mix attention over two years.",
    "Oil-price spikes drive volume; renewables carry positive tone.",
    "compare", terms=["crude oil", "renewable energy", "natural gas"])
add("energy-climate", "carbon-capture-brief", "Carbon capture brief",
    "Give me a research brief on carbon capture and storage.",
    "A structured brief for a climate-tech memo.",
    "Patents and research tell different stories; the brief shows both.",
    "brief", topic="carbon capture", term="carbon capture")
add("energy-climate", "climate-finance-geo", "Climate finance geography",
    "Where is climate finance studied and where is it in the news?",
    "Research vs news geography of a negotiation topic.",
    "Global South coverage vs Global North research.",
    "geo", claim="Climate finance", term="climate finance")

# ── technology ──────────────────────────────────────────────────────────────
add("technology", "gen-ai-education-stance", "Generative AI in education",
    "How is research on generative AI in education framed: promising or cautionary? How has it moved?",
    "The framing trend of a fast-moving literature.",
    "A 2023+ literature: almost entirely after most training cut-offs.",
    "stance", term="generative ai in education")
add("technology", "quantum-computing-radar", "Quantum computing research radar",
    "What is new in quantum computing research since 2023?",
    "Momentum and framing shift for a deep-tech investor.",
    "Error-correction milestones in 2024-2025 shifted the framing.",
    "radar", topic="quantum computing", since_year=2023)
add("technology", "ai-agents-pulse", "AI agents in the news",
    "How much news coverage is there of AI agents, and how fast is it growing?",
    "Hype-cycle read on an emerging category.",
    "A 2024-2025 term: model knowledge is thin, the corpus is not.",
    "pulse", term="ai agents")
add("technology", "llm-hallucination-evidence", "Do LLMs hallucinate citations?",
    "How often do large language models fabricate references? Give numbers.",
    "Quantified failure rates for an AI-governance review.",
    "The meta-question: a model answering about its own failure mode.",
    "evidence", claim="Large language models fabricate citations")
add("technology", "semiconductors-compare", "Chips race in the news",
    "Compare news coverage of semiconductors, TSMC and chip export controls.",
    "Geopolitics of chips, measured as attention.",
    "Export-control coverage spikes on US announcements.",
    "compare", terms=["semiconductor", "tsmc", "export controls"])
add("technology", "humanoid-robots-history", "Humanoid robot research trend",
    "How has research on humanoid robots grown, and what range should we expect for the next three years?",
    "A measured series and a forward range.",
    "Media hype vs research output; the series is the reality check.",
    "history", subject_phrases=["humanoid robot"], outcome_phrases=None)
add("technology", "6g-research-geo", "6G research geography",
    "Which countries lead 6G research and patents?",
    "Country-level technology leadership.",
    "Patents publish ~18 months late; recent years are censored, not falling.",
    "geo", claim="6G wireless networks", term="6g")
add("technology", "cybersecurity-trending", "Rising topics in tech news",
    "What technology topics are rising fastest in the news?",
    "A tech-trend scan for a product strategist.",
    "Trending ranks by growth against the previous window, not by size.",
    "trending", days=60, category="technology")

# ── agriculture ─────────────────────────────────────────────────────────────
add("agriculture", "millets-india-pulse", "Millets in Indian news",
    "What is the news saying about millets in India?",
    "A food-policy and market narrative.",
    "International Year of Millets 2023 created a spike; what remains after?",
    "pulse", term="millets")
add("agriculture", "glyphosate-cancer", "Does glyphosate cause cancer?",
    "Does glyphosate exposure cause cancer? What does the evidence say and what disagrees?",
    "Both sides of a litigated scientific question.",
    "IARC classification vs regulators: the literature is polarised.",
    "evidence", claim="Glyphosate exposure causes cancer")
add("agriculture", "precision-farming-radar", "Precision agriculture research radar",
    "What is new in precision agriculture research?",
    "A technology radar for an agtech fund.",
    "Drones, AI and IoT sub-literatures move at different speeds.",
    "radar", topic="precision agriculture", since_year=2022)
add("agriculture", "food-inflation-compare", "Food prices in the news",
    "Compare coverage of food inflation, onion prices and wheat prices.",
    "Commodity narrative tracking for an Indian policy desk.",
    "Onion price coverage is seasonal and India-specific.",
    "compare", terms=["food inflation", "onion prices", "wheat prices"])
add("agriculture", "crop-yields-climate-table", "Climate impact on crop yields",
    "For each crop, what does research say about climate change impact on yield?",
    "A per-crop evidence table, export-ready.",
    "Each crop has a separate literature; one number cannot serve all rows.",
    "table", rows=["wheat", "rice", "maize", "soybean", "millet"],
    table_question="climate change impact on crop yield percent")
add("agriculture", "organic-farming-stance", "Organic farming research framing",
    "Is research on organic farming becoming more favourable?",
    "Stance trend for a sustainability review.",
    "Yield-gap critiques vs environmental-benefit findings.",
    "stance", term="organic farming")

# ── education & labour ──────────────────────────────────────────────────────
add("education-labour", "remote-work-productivity", "Does remote work hurt productivity?",
    "Does remote work reduce productivity? What does the evidence say?",
    "Evidence for a workplace policy decision.",
    "Pandemic-era studies and RCTs disagree; both appear.",
    "evidence", claim="Remote work reduces productivity")
add("education-labour", "layoffs-pulse", "Layoffs in the news",
    "How much layoff coverage has there been, which companies and places, and what is the tone?",
    "Labour-market sentiment monitoring.",
    "Tech layoffs dominate headlines out of proportion to labour data.",
    "pulse", term="layoffs")
add("education-labour", "nep-2020-brief", "National Education Policy brief",
    "Give me a research brief on India's National Education Policy 2020.",
    "A policy brief scoped to India.",
    "Small, recent literature; the brief must say how thin it is.",
    "brief", topic="national education policy", geo="india", term="national education policy")
add("education-labour", "ai-jobs-stance", "AI and jobs research framing",
    "Is research on AI and automation-driven job displacement becoming more pessimistic?",
    "Stance trend for a workforce strategy.",
    "Generative AI shifted the framing from automation to augmentation.",
    "stance", term="job displacement")
add("education-labour", "edtech-compare", "Edtech in the news",
    "Compare news coverage of edtech, online learning and Byju's.",
    "Sector attention and one company's crisis.",
    "Byju's collapse dominates Indian edtech coverage in 2024.",
    "compare", terms=["edtech", "online learning", "byju's"])

# ── legal ───────────────────────────────────────────────────────────────────
add("legal", "antitrust-big-tech", "Google antitrust coverage",
    "What is the news saying about the antitrust cases against Google: search, ad tech and the remedies?",
    "Litigation and enforcement monitoring.",
    "Google search ruling (2024) and remedies (2025) are post-training for many models.",
    "pulse", term="google antitrust")
add("legal", "supreme-court-india", "Supreme Court of India coverage",
    "What themes dominate coverage of India's Supreme Court?",
    "A judiciary media read for a legal team.",
    "'Supreme Court' is ambiguous across countries; geography disambiguates.",
    "pulse", term="supreme court of india")
add("legal", "gdpr-fines-radar", "GDPR enforcement research",
    "What is new in research on GDPR enforcement and fines?",
    "Regulatory-research radar for a compliance officer.",
    "Legal scholarship is slow; the radar shows how little is new.",
    "radar", topic="gdpr enforcement", since_year=2022)
add("legal", "copyright-ai-pulse", "AI copyright lawsuits",
    "What is the coverage of copyright lawsuits against AI companies?",
    "IP-litigation tracking for an AI company.",
    "NYT v OpenAI and the Anthropic authors settlement are recent; recency is the test.",
    "pulse", term="ai copyright")
add("legal", "death-penalty-deterrence", "Does the death penalty deter crime?",
    "Does the death penalty deter murder? What does the evidence say?",
    "Both sides of a long-running empirical debate.",
    "Econometric claims of deterrence are heavily contested.",
    "evidence", claim="The death penalty deters homicide")

# ── supply chain ────────────────────────────────────────────────────────────
add("supply-chain", "red-sea-shipping", "Red Sea shipping disruption",
    "What is the coverage of Red Sea shipping disruption: tone, places, critical stories?",
    "A chokepoint monitor for a logistics team.",
    "Houthi attacks since late 2023; coverage geography spans Asia and Europe.",
    "pulse", term="red sea shipping")
add("supply-chain", "rare-earths-compare", "Rare earths vs lithium vs cobalt",
    "Compare news coverage of rare earths, lithium and cobalt.",
    "Critical-minerals attention for a procurement team.",
    "China's 2025 rare-earth export controls spike one series.",
    "compare", terms=["rare earth", "lithium", "cobalt"])
add("supply-chain", "nearshoring-radar", "Nearshoring research radar",
    "What is new in research on supply chain reshoring and nearshoring?",
    "A strategy radar for manufacturing.",
    "Post-2020 literature; framing moved from cost to resilience.",
    "radar", topic="supply chain resilience", since_year=2021)
add("supply-chain", "semiconductor-shortage-history", "Chip shortage research trend",
    "How did research on semiconductor supply chains grow and what range follows?",
    "Measured series with a forward range.",
    "2021 shortage spike: a naive trend line overshoots.",
    "history", subject_phrases=["semiconductor supply chain"], outcome_phrases=None)
add("supply-chain", "container-freight-pulse", "Container freight rates",
    "What has the news said about container freight rates?",
    "Freight-market narrative for a shipper.",
    "Rates spiked in 2024 on Red Sea diversions.",
    "pulse", term="freight rates")

# ── journalism ──────────────────────────────────────────────────────────────
add("journalism", "audit-coffee-draft", "Audit a health article draft",
    "Fact-check this draft before I publish it.",
    "Every checkable claim found, matched to evidence, with citation coverage.",
    "A draft mixes true, overstated and unsupported claims; the audit must tell them apart.",
    "audit", text=("Coffee is one of the healthiest drinks in the world. Drinking three cups a day lowers the risk "
                   "of heart disease by 50 percent. Coffee also prevents Parkinson's disease and cures type 2 "
                   "diabetes. However, caffeine raises blood pressure in the short term."))
add("journalism", "audit-ev-draft", "Audit an EV explainer",
    "Fact-check this electric-vehicle explainer.",
    "Claim-by-claim evidence status for a tech explainer.",
    "Lifecycle-emissions claims need research, not news.",
    "audit", text=("Electric vehicles produce fewer lifetime emissions than petrol cars even on coal-heavy grids. "
                   "EV batteries lose most of their capacity within five years. Battery fires are more common in "
                   "electric vehicles than in petrol cars."))
add("journalism", "improve-microplastics", "Fix an overstated claim",
    "Rewrite this sentence so it says what the evidence supports: 'Microplastics cause cancer in humans.'",
    "A better-supported rewrite plus the evidence card behind it.",
    "The evidence is mostly animal and cell studies; the rewrite must say so.",
    "improve", claim="Microplastics cause cancer in humans")
add("journalism", "improve-screen-time", "Fix a screen-time claim",
    "Rewrite: 'Screen time causes ADHD in children.'",
    "A defensible rewrite and the strongest source.",
    "Association is not causation; the rewrite must downgrade the verb.",
    "improve", claim="Screen time causes ADHD in children")
add("journalism", "citations-sugar-tax", "Citations for a sugar-tax story",
    "Give me APA citations for the claim that sugar taxes reduce sugary drink consumption, ranked by weight.",
    "Ready-to-paste citations, rendered from stored metadata, with source ranking.",
    "Models invent DOIs; every citation here comes from the corpus record.",
    "citations", claim="Sugar taxes reduce sugary drink consumption", style="apa")
add("journalism", "election-misinformation-pulse", "Election misinformation coverage",
    "How much coverage has election misinformation received, and where?",
    "A newsroom's beat monitor.",
    "2024 was a global election year; coverage is spread across dozens of countries.",
    "pulse", term="election misinformation")

# ── academic ────────────────────────────────────────────────────────────────
add("academic", "microbiome-depression-stance", "Gut microbiome and depression literature",
    "How is research on the gut microbiome and depression framed, and which recent studies are most promising?",
    "A literature map for a systematic review.",
    "Mouse studies and human cohorts share a vocabulary; stance labels separate the framings.",
    "stance", term="gut microbiome depression")
add("academic", "library-gaps-ai-ethics", "What is my AI-ethics reading list missing?",
    "Here is my reading list on AI ethics. What important topics is it missing?",
    "Library-gap analysis for a thesis.",
    "Coverage gaps are measured against the corpus, not suggested from memory.",
    "library", items=["Algorithmic bias in hiring", "Fairness in machine learning", "Explainable AI methods",
                      "Privacy-preserving machine learning"], subject="ai ethics")
add("academic", "citations-exercise-depression", "Vancouver citations for exercise and depression",
    "Give me Vancouver-style citations showing exercise reduces depression, ranked by evidence weight.",
    "Citation-ready references for a manuscript.",
    "Meta-analyses outrank single trials; the ranking shows why.",
    "citations", claim="Exercise reduces depression symptoms", style="vancouver")
add("academic", "crispr-history", "CRISPR research trend",
    "How has CRISPR research volume grown, and what range should we expect next?",
    "Bibliometric series and a forward range.",
    "A maturing field: growth is slowing; the range must reflect it.",
    "history", subject_phrases=["crispr"], outcome_phrases=None)
add("academic", "microfinance-claims", "Microfinance: empowerment or debt trap?",
    "Does microfinance empower women, or does it create debt traps? Compare the evidence.",
    "Two competing claims measured the same way.",
    "The 2015 RCT wave turned the consensus; both sides persist.",
    "claims", claim_a="Microfinance empowers women", claim_b="Microfinance causes over-indebtedness")
add("academic", "mindfulness-stance", "Mindfulness research framing",
    "Is research on mindfulness becoming more critical over time?",
    "Framing trend for a meta-research paper.",
    "Replication critiques after 2017 should show.",
    "stance", term="mindfulness")

# ── environment ─────────────────────────────────────────────────────────────
add("environment", "microplastics-pulse", "Microplastics in the news",
    "What does the news say about microplastics, and how has coverage moved?",
    "An environmental-risk media read.",
    "Human-tissue studies (brain, placenta) drove 2024-2025 spikes.",
    "pulse", term="microplastics")
add("environment", "groundwater-india-brief", "Groundwater depletion in India",
    "Give me a research brief on groundwater depletion in India.",
    "A geo-scoped environmental brief.",
    "Punjab and Haryana dominate; the brief should name the geography.",
    "brief", topic="groundwater depletion", geo="india", term="groundwater")
add("environment", "floods-vs-heatwaves", "Floods vs heatwaves vs wildfires",
    "Compare news coverage of floods, heatwaves and wildfires.",
    "Hazard attention for a disaster-risk team.",
    "Seasonality: each hazard peaks in a different month.",
    "compare", terms=["floods", "heatwave", "wildfire"])
add("environment", "pfas-evidence", "PFAS and health",
    "Do PFAS 'forever chemicals' harm human health? Give numbers and sources.",
    "Effect sizes for an environmental-health regulator.",
    "Many outcomes; one mechanism per claim keeps retrieval on target.",
    "evidence", claim="PFAS exposure increases cancer risk")
add("environment", "coral-bleaching-radar", "Coral bleaching research radar",
    "What has changed in coral bleaching research recently?",
    "A radar after the 2023-2024 global bleaching event.",
    "The fourth global bleaching event is post-training for many models.",
    "radar", topic="coral bleaching", since_year=2022)

# ── consumer & media ────────────────────────────────────────────────────────
add("consumer-media", "ashwagandha-evidence", "Does ashwagandha reduce stress?",
    "Does ashwagandha reduce stress and anxiety? What is the quality of evidence?",
    "Supplement-claim checking for a consumer-health brand.",
    "Small, industry-funded trials; tiering exposes it.",
    "evidence", claim="Ashwagandha reduces stress")
add("consumer-media", "streaming-compare", "Netflix vs Disney+ vs Prime Video",
    "Compare news coverage of Netflix, Disney+ and Amazon Prime Video.",
    "Media-brand attention share.",
    "Netflix dominates; growth tells the challenger story.",
    "compare", terms=["netflix", "disney+", "prime video"])
add("consumer-media", "quick-commerce-pulse", "Quick commerce in India",
    "What is the news saying about quick commerce in India?",
    "A sector narrative for a retail strategist.",
    "Blinkit, Zepto and Instamart; dark-store regulation stories.",
    "pulse", term="quick commerce")
add("consumer-media", "ultra-processed-food", "Ultra-processed food and health",
    "How strong is the evidence that ultra-processed food increases mortality?",
    "Effect sizes for a food-policy brief.",
    "A large 2019+ cohort literature with umbrella reviews in 2024.",
    "evidence", claim="Ultra-processed food consumption increases mortality")

assert len({s["slug"] for s in S}) == len(S), "duplicate slug"
# ── entities: companies, people, places, phrases ────────────────────────────
add("entities", "modi-vs-trump", "Narendra Modi vs Donald Trump in the news",
    "How does world news coverage of Narendra Modi compare with Donald Trump: volume, growth, tone and critical stories?",
    "Two leaders on one scale, month by month, with tone against the all-news baseline.",
    "Trump dominates global volume; the useful reading is share, growth and tone, not raw counts.",
    "compare", terms=["narendra modi", "donald trump"])
add("entities", "reliance-industries-pulse", "Reliance Industries: media intelligence",
    "What is the world saying about Reliance Industries: volume, tone, themes, people and places?",
    "A listed conglomerate as an entity: Jio, retail, energy and the Ambanis around it.",
    "The company name collides with 'reliance' as a common word; matching must be by entity.",
    "pulse", term="reliance industries")
add("entities", "infosys-tcs-wipro", "Infosys vs TCS vs Wipro",
    "How does news attention compare across Infosys, TCS and Wipro, and whose tone is better?",
    "Three listed IT services rivals on one scale with growth and tone.",
    "Results seasons create quarterly spikes; growth must be read across them.",
    "compare", terms=["infosys", "tcs", "wipro"])
add("entities", "hdfc-bank-pulse", "HDFC Bank: media intelligence",
    "What is the world saying about HDFC Bank: coverage volume, tone, themes, related companies and places?",
    "A listed bank as an entity, with the merger and results cycle in its themes.",
    "HDFC Bank and HDFC (the merged parent) share a name; the reading must say which.",
    "pulse", term="hdfc bank")
add("entities", "tata-motors-pulse", "Tata Motors: media intelligence",
    "What is the world saying about Tata Motors: volume, tone, themes, people and places?",
    "A listed automaker as an entity: EVs, Jaguar Land Rover, demerger.",
    "Tata group coverage spills into Tata Motors; themes show which stories are about the company.",
    "pulse", term="tata motors")
add("entities", "bengaluru-pulse", "Bengaluru as a news entity",
    "What is the world saying about Bengaluru: coverage volume, tone, themes, people and organisations?",
    "A city as an entity: tech, traffic, water, politics.",
    "Bangalore and Bengaluru are one place; tone moves with civic crises.",
    "pulse", term="bengaluru")
add("entities", "mumbai-delhi-bengaluru", "Mumbai vs Delhi vs Bengaluru",
    "How does news attention compare across Mumbai, Delhi and Bengaluru, and how does tone differ?",
    "Three cities on one scale, with growth and tone.",
    "Delhi carries national-government news; the comparison has to say so.",
    "compare", terms=["mumbai", "delhi", "bengaluru"])
add("entities", "isro-pulse", "ISRO: media intelligence",
    "What is the world saying about ISRO: coverage volume, tone, themes, people and places?",
    "A public agency as an entity: launches, missions and the people around them.",
    "Mission spikes (Chandrayaan, Gaganyaan) dominate; tone is unusually positive.",
    "pulse", term="isro")


SCENARIOS = S

# Benchmark-only questions: generic finance and business research, no news time series. Kept out of
# SCENARIOS so the showcase pages do not change; bench.py draws one of these at random.
_n = len(S)
add("finance", "board-diversity-performance", "Does board gender diversity improve firm performance?",
    "Does board gender diversity improve firm financial performance? What does the evidence say?",
    "Effect sizes from corporate-finance studies, with the contrary findings.",
    "Endogeneity: diverse boards may follow good performance; quota natural experiments (Norway) disagree with correlational studies.",
    "evidence", claim="Board gender diversity improves firm financial performance")
add("finance", "esg-returns-evidence", "Does ESG investing deliver better risk-adjusted returns?",
    "Does ESG investing deliver better risk-adjusted returns than conventional investing? What does the evidence say?",
    "Meta-analytic and portfolio-level findings, with the null and negative results.",
    "Results depend on the ESG rating provider, period and asset class; outperformance claims often vanish after factor adjustment.",
    "evidence", claim="ESG investing delivers higher risk-adjusted returns")
add("finance", "buybacks-investment-evidence", "Do share buybacks crowd out corporate investment?",
    "Do share buybacks reduce long-term corporate investment? What does the evidence say?",
    "Firm-level evidence on buybacks, capex and R&D, with the contrary findings.",
    "Buybacks may follow a lack of investment opportunities rather than cause underinvestment.",
    "evidence", claim="Share buybacks reduce corporate investment")
add("finance", "microfinance-poverty-evidence", "Does microfinance reduce poverty?",
    "Does microfinance reduce household poverty? What does the evidence say?",
    "Randomised evaluations and their effect sizes, with the null results.",
    "Six RCTs found modest effects; earlier observational studies were far more positive.",
    "evidence", claim="Microfinance reduces household poverty")
add("finance", "ma-acquirer-returns-evidence", "Do acquisitions create value for acquirers?",
    "Do mergers and acquisitions create value for the acquiring firm's shareholders? What does the evidence say?",
    "Event-study and long-run return evidence, with the contrary findings.",
    "Short-window announcement returns and long-run performance often disagree; public vs private targets differ.",
    "evidence", claim="Acquisitions create value for acquiring firm shareholders")
add("finance", "minimum-capital-bank-lending-evidence", "Do higher bank capital requirements reduce lending?",
    "Do higher bank capital requirements reduce bank lending? What does the evidence say?",
    "Effect sizes from banking studies, with the contrary findings.",
    "Short-run lending cuts versus long-run stability; the effect depends on how banks raise capital.",
    "evidence", claim="Higher bank capital requirements reduce bank lending")
BENCH_EXTRA = S[_n:]
del S[_n:]
BY_SLUG = {s["slug"]: s for s in S + BENCH_EXTRA}

if __name__ == "__main__":
    from collections import Counter
    print(len(S), "scenarios")
    print(Counter(s["category"] for s in S))
    print(Counter(s["pattern"] for s in S))
