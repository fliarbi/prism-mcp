# Deep meta-analytics on one topic, narrowed to one angle

A worked example of what Prism answers that a language model with a search box cannot: a
whole research literature measured from the corpus, then focused onto a single claim — with
every number measured from the data and every quote verified against its source.

**Topic:** intermittent fasting **Angle:** glycemic control in type 2 diabetes

**▶ View the rendered report:** <https://fliarbi.com/demo/prism-examples/intermittent-fasting/>
*(GitHub shows `index.html` as source, not as a rendered page — the link above renders it.)*

The rendered page (`index.html`) is a self-contained, theme-aware visualization built entirely
from the two API responses below — open it in any browser. Every figure on it traces to
`data.json` in this folder, which is the raw retrieved payload (volumes, stance, pooled
effects, the per-year series and geography), kept for audit.

---

## Reproduce it — two calls

Both calls go to the public Prism endpoint and need one Fliar API key
(`Authorization: Bearer rdr_…`, from <https://fliarbi.com/radar/dashboard?tab=radarapi>).

### 1 · The whole topic

```bash
curl -s https://radar-api.fliarbi.com/prism/v1/research.brief \
  -H "Authorization: Bearer rdr_…" \
  -H "Content-Type: application/json" \
  -d '{"topic":"intermittent fasting"}'
```

Returns the structured brief: corpus **volumes** per window, **what is established**
(reviews, meta-analyses, guidelines), **what is contested** (the orientation mix),
**key numbers** quoted verbatim with their source, **direction of travel**, **geography**,
and the institutions working on it ranked by lift.

### 2 · Narrow to one angle

```bash
curl -s https://radar-api.fliarbi.com/prism/v1/research.evidence \
  -H "Authorization: Bearer rdr_…" \
  -H "Content-Type: application/json" \
  -d '{"claim":"intermittent fasting improves glycemic control in type 2 diabetes"}'
```

Returns the **claim lane**: how many papers cover *both* poles of the claim (99) versus the
subject (62,557) and the outcome (85,592) alone; the **corpus stance** (orientation and
support/qualify/contradict split over those 99 papers); and the **documents themselves**,
each with a verified verbatim quote, its study-design tier, and whether that quote supports or
contradicts the claim.

### The same, over MCP

Any MCP client (Claude Desktop, ChatGPT connector, Cursor, n8n) calls the identical features
as tools — no HTTP plumbing:

```jsonc
research_brief  { "topic": "intermittent fasting" }
find_evidence   { "claim": "intermittent fasting improves glycemic control in type 2 diabetes" }
```

---

## Focus a different angle

The angle *is* the claim. Keep the subject, change what you ask about it, and the lens swings:

```bash
# cardiovascular, not glycemic
-d '{"claim":"intermittent fasting reduces cardiovascular mortality"}'

# head-to-head, not absolute
-d '{"claim":"intermittent fasting outperforms continuous calorie restriction for weight loss"}'

# the safety angle a clinician would ask about
-d '{"claim":"intermittent fasting raises the risk of hypoglycaemia in type 2 diabetes"}'

# a different organ system
-d '{"claim":"intermittent fasting improves non-alcoholic fatty liver disease"}'
```

Each returns its own claim lane, stance split and verified documents. Because the subject is
held constant, the lanes are comparable: you can watch support rise on one outcome and the
cautionary minority grow on another.

To compare two claims side by side in one call, use `compare_claims`
(`{ "claim_a": "…", "claim_b": "…" }`).

---

## How to read the numbers (the honesty model)

- **Lane.** A topic count and a claim count differ by orders of magnitude. The page always says
  which lane a number came from; a verdict is read from the claim lane, never from one pole.
- **Window.** Each corpus is counted over its own window (typed research 2017–2025, biomedical index
  1990–2025, patents to 2024). Counts across corpora are not comparable and are never added.
- **Coverage.** Every number is computed under the coverage check; if part of the data were unavailable the answer says so rather than returning a silent undercount.
- **Evidence vs interpretation.** Quoted findings are copied verbatim and verified against the
  source. Orientation and stance are labels on each paper's own framing — not a judgment that
  the claim is true.
- **Units.** Different measures (HbA1c %, fasting glucose mg/dL, HOMA-IR) are shown each on its
  own scale; the example never puts unlike units on one axis.
