# Prism MCP: research, news and evidence intelligence for AI

**Search engines return pages. Chatbots return prose. Prism returns measurements.**

```bash
curl -fsSL https://radar-api.fliarbi.com/prism/install.sh | bash      # installs the `prism` command, no sudo
prism login                                                          # paste your rdr_ key
prism compare "narendra modi" "donald trump"
```

Prism is an intelligence API and MCP server for Claude, ChatGPT, Codex, Cursor and any agent: news
intelligence, research evidence, health and clinical evidence, patents and innovation signals, geography,
trend history and forecasting, citations and grounded writing, in **more than 50 tools** over MCP, REST and a command-line client. It sits on
**more than a billion records**: global news, scientific journals and research papers, health literature,
patents and social signals, indexed so an assistant can *count, compare, trace and cite* instead of recalling.

Give it a **company, person, place or phrase** (*Tata Motors*, *Narendra Modi*, *Bengaluru*, *"air pollution"*,
*"GLP-1"*) and it measures attention, growth, tone, themes, the people, organisations and places around it, and how
it compares with rivals. Ask it a question (*"is the evidence that metformin prevents cancer getting stronger?"*)
and it reads the research for and against. The numbers are measured from the data, the quotes are copied from the source and
verified, and every answer says the window it was counted over and what it cannot tell you.

> **The one rule: the model never supplies a fact.** Every count, share and trend is measured by Prism.
> Quotes are verified verbatim against their source. Numbers written into generated prose are checked against
> the material the prose was given, and rejected when they are not there. When the data has nothing, the tool
> says `ok: false` and why. It never fills the gap with something plausible.

**Live.** Base URL `https://radar-api.fliarbi.com/prism` · MCP `https://radar-api.fliarbi.com/prism/mcp` ·
create a key in the [Fliar dashboard](https://fliarbi.com/radar/dashboard?tab=radarapi) (**API keys**). One key works
on Prism, the [Radar API](https://github.com/fliarbi/radar-api-mcp) and the Prism News APIs, and one prepaid wallet
pays for all of them.

## What Prism answers

| Capability | What you get | Typical question |
| --- | --- | --- |
| **News intelligence** | volume, tone against the all-news baseline, themes, people and organisations, the critical stories, source mix | *What is the world saying about NVIDIA, and which stories matter?* |
| **Competitive attention** | two to four subjects on one scale, month by month, with growth and tone | *Tesla vs BYD: who is gaining attention, and how is it framed?* |
| **Research evidence** | supporting and contradicting papers, read and labelled, weighted by study tier, with verbatim quotes and DOIs | *Does vitamin D help depression? Show the counter-evidence.* |
| **Health evidence** | clinical study designs, effect sizes with their populations, the direction of risk-factor claims | *GLP-1 drugs and muscle loss: how strong is the signal?* |
| **Literature mapping** | how a field frames its findings year by year: promising, cautionary, critical | *Is carbon-tax research becoming more favourable?* |
| **Geography** | the place coverage is about (country, state, city) with lift; where a subject is studied, published and patented, kept apart | *Where is dengue studied vs where is it reported?* |
| **Trend history and forecasting** | long measured series and backtested three-year scenarios with bounds | *Where is research on humanoid robots heading?* |
| **Innovation signals** | patent activity by assignee country and over time, next to research and news | *Is green hydrogen moving from papers to patents?* |
| **Fact-checking** | every checkable claim in a draft, with its status and a safer wording | *Audit this health article before it goes out.* |
| **Spreadsheet research** | one question across many rows, a value and a source per row, or an honest blank | *Energy density and cost for five battery chemistries.* |
| **Citations and reading lists** | APA, Vancouver, BibTeX and more from stored metadata; what a reading list is missing | *What is my AI-ethics reading list missing?* |
| **Reports and dashboards** | HTML reports and dashboards built by the assistant, checked by `check_report` | *Build me a geo dashboard on air pollution in India.* |

## Who uses it

* **Policy and government teams:** decision briefings with India-vs-world comparisons, forecasts, options and the evidence against them.
* **Researchers and evidence-synthesis groups:** literature maps, counter-evidence on purpose, reproducible counts and exports for a methods section.
* **Newsrooms and fact-checkers:** draft audits, the critical stories behind a trend, and citations that resolve.
* **Strategy, consulting and competitive intelligence:** attention and tone for a rival set, themes, places and the people around a company.
* **Investors and finance research:** market narratives and sector sentiment measured over time, not recalled from training data.
* **Health, pharma and nutrition:** study-design-weighted evidence, effect sizes and the direction of risk-factor claims.

## Why it holds up

* **Measured, not recalled.** Counts and shares come from queries; a model only reads and explains them.
* **Time-aware.** Every series states its window and marks an incomplete newest period instead of plotting it as a collapse.
* **Evidence-weighted.** Papers are read and labelled supports, contradicts or qualifies, and weighted by study design.
* **Geography kept honest.** Where a subject is reported, studied, published and patented are four different questions, never added together.
* **Checkable.** One JSON envelope for every tool, with the window and the coverage check, exportable to CSV, Excel, JSONL and BibTeX.
* **Honest about gaps.** An empty answer comes back as `ok: false` with a reason, so an assistant can say "not measured" rather than guess.

## Demonstrations

The gallery of live demonstrations, topic, disease and investor pages is being refreshed and will be back here shortly.

---

© Fliar BI. All rights reserved.
