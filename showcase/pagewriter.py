"""Write the text of an analysis page from its facts: Claude Sonnet first, the fast model as a fallback, and the number
gate on every sentence (a sentence with a number that is not in the facts is dropped).

    from pagewriter import write
    text = write(SYSTEM, facts_dict, keys=("summary", "risk", ...))
"""
import json
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

RULES = ("\n\nRules: use ONLY the facts below. Copy every number exactly as written in the facts (with its thousands "
         "separators); do not compute new numbers, percentages or ratios. Lists in the facts are already ranked, largest "
         "first; do not call anything the largest, fastest or most unless the ranking shows it. Write plain, specific "
         "British English for a decision-maker; no hype, no advice, no mention of how the data was collected. "
         "Return ONLY the JSON object.")


def _commas(o):
    if isinstance(o, bool) or o is None:
        return o
    if isinstance(o, int):
        return o if 1900 <= o <= 2100 else f"{o:,}"   # years stay years
    if isinstance(o, dict):
        return {k: _commas(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_commas(v) for v in o]
    return o


def _bad(sentence, src_numbers):
    """numbers in the sentence that are not in the facts (values only; '12.4%' matches a fact of 12.4)"""
    from prism import llm
    return [n for n in llm.numbers_in(sentence) if n not in src_numbers]


def write(system, facts, keys):
    from prism import llm
    blob = json.dumps(_commas(facts), ensure_ascii=False, default=str)
    prompt = system + RULES + "\n\nFACTS:\n" + blob
    out = None
    try:
        import compare
        raw = compare.run_claude(prompt, model="sonnet", timeout=600)["text"]
        out = json.loads(re.search(r"\{.*\}", raw, re.S).group(0))
    except Exception:
        out = llm.call_json(system + RULES, "FACTS:\n" + blob, max_tokens=3000)
    src = llm.numbers_in(blob)
    text = {}
    for k in keys:
        raw = (out or {}).get(k)
        if isinstance(raw, list):   # a list of short items: keep those that pass the gate
            items = [str(x).strip() for x in raw if str(x).strip() and not _bad(str(x), src)]
            if items:
                text[k] = items
            continue
        v = str(raw or "").strip()
        keep = [x for x in re.split(r"(?<=[.!?])\s+", v) if x and not _bad(x, src)]
        if keep:
            text[k] = " ".join(keep)
    return text


def clean(text):
    """field names the writer sometimes copies from the facts, rewritten as prose"""
    import re

    def one(s):
        s = re.sub(r"(?:a |the )?contested_pct(?: is| of|:)? (\d+(?:\.\d+)?)%?", r"a contested share of \1%", s)
        s = re.sub(r"(?:a |the )?positive_pct(?: is| of|:)? (\d+(?:\.\d+)?)%?", r"a positive share of \1%", s)
        s = s.replace("contested_pct", "contested share").replace("positive_pct", "positive share").replace("neg_per_pos", "negative per positive")
        return s
    return {k: ([one(str(x)) for x in v] if isinstance(v, list) else one(str(v))) for k, v in text.items()}
