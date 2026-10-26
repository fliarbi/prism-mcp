#!/usr/bin/env python3
"""cite — turning a retrieved document into the citation a publisher wants.

Nine output modes, all built from the metadata the corpus actually holds:
authors, year, title, venue, DOI, URL. Nothing is inferred. A missing field is
simply absent from the rendered citation — an invented volume number in an
otherwise real reference is the one failure a reader cannot catch.

Names. Author arrays give full names ("Jane Q. Smith", "Rianne van Geen"), so
the surname has to be found rather than assumed: only a LOWERCASE particle
binds to the surname, which is what separates "van Geen" from the given name in
"Di Long". And no honorific is ever added — these are real named researchers,
an author array says nothing about anyone's pronouns or title, and a published
page that guesses has misgendered someone in print.
"""
from __future__ import annotations

import html
import re

PARTICLES = {"van", "von", "de", "der", "den", "del", "della", "di", "da", "dos",
             "du", "la", "le", "bin", "ibn", "al", "ter", "ten"}

STYLES = ("apa", "vancouver", "harvard", "mla", "chicago", "bibtex",
          "inline_link", "footnote", "numbered", "source_card", "wordpress")


def surname(full: str, surname_first: bool = False) -> str:
    """The family name.

    `surname_first` because the two corpora store names in opposite orders:
    OpenAlex writes "Jane Q. Smith", PubMed writes "Doepker Candace". Guessing
    from the string is unreliable — "Cohen Sarah S" and "Sarah S Cohen" are the
    same person in the same shape — so the caller passes what the source does,
    and rendering a real researcher as "Candace, D." stops happening."""
    parts = [t for t in re.split(r"\s+", (full or "").strip()) if t]
    if not parts:
        return ""
    if surname_first:
        return parts[0]
    # Walk back over a RUN of lowercase particles: "de la Cruz", "van der Berg".
    i = len(parts) - 1
    while i > 1 and parts[i - 1].strip(".") in PARTICLES:
        i -= 1
    return " ".join(parts[i:])


def initials(full: str, surname_first: bool = False) -> str:
    parts = [t for t in re.split(r"\s+", (full or "").strip()) if t]
    if len(parts) < 2:
        return ""
    if surname_first:
        given = parts[1:]
        return " ".join(f"{g[0].upper()}." for g in given if g and g[0].isalpha())
    sn = surname(full)
    given = parts[:len(parts) - len(sn.split())]
    return " ".join(f"{g[0].upper()}." for g in given if g and g[0].isalpha())


def _sf(doc: dict) -> bool:
    """PubMed rows carry "Surname Given"; everything else "Given Surname"."""
    return (doc or {}).get("source") == "pubmed"


def label(doc: dict) -> str:
    """'Jain and colleagues (2021)' — an attribution built from OUR author array,
    so prose cannot invent one."""
    names = [a for a in (doc.get("authors") or []) if a]
    year = doc.get("year")
    if not names:
        return f"({year})" if year else ""
    sf = _sf(doc)
    s = surname(names[0], sf)
    if len(names) == 1:
        return f"{s} ({year})" if year else s
    if len(names) == 2:
        return f"{s} and {surname(names[1], sf)} ({year})" if year else \
               f"{s} and {surname(names[1], sf)}"
    return f"{s} and colleagues ({year})" if year else f"{s} and colleagues"


def _url(doc: dict) -> str | None:
    if doc.get("doi"):
        return f"https://doi.org/{doc['doi']}"
    return doc.get("url")


def _authors_apa(doc: dict, cap: int = 20) -> str:
    names = [a for a in (doc.get("authors") or []) if a][:cap]
    if not names:
        return ""
    sf = _sf(doc)
    out = [f"{surname(n, sf)}, {initials(n, sf)}".strip().rstrip(",") for n in names]
    if len(out) == 1:
        return out[0]
    return ", ".join(out[:-1]) + ", & " + out[-1]


def _authors_vancouver(doc: dict, cap: int = 6) -> str:
    names = [a for a in (doc.get("authors") or []) if a]
    sf = _sf(doc)
    out = [f"{surname(n, sf)} {initials(n, sf).replace('.', '').replace(' ', '')}".strip()
           for n in names[:cap]]
    return ", ".join(out) + (", et al" if len(names) > cap else "")


def _title(doc: dict) -> str:
    return (doc.get("title") or "").strip().rstrip(".")


def render(doc: dict, style: str = "apa", index: int | None = None) -> str:
    """One document, one citation string (or HTML, for the display styles)."""
    style = (style or "apa").lower()
    t, venue, year = _title(doc), (doc.get("venue") or "").strip(), doc.get("year")
    url = _url(doc)

    if style == "apa":
        bits = [b for b in (_authors_apa(doc), f"({year})" if year else "",
                            f"{t}." if t else "", f"{venue}." if venue else "",
                            url or "") if b]
        return " ".join(bits).replace("  ", " ").strip()
    if style == "vancouver":
        bits = [b for b in (_authors_vancouver(doc) + "." if doc.get("authors") else "",
                            f"{t}." if t else "", f"{venue}." if venue else "",
                            f"{year}." if year else "", url or "") if b]
        return " ".join(bits).strip()
    if style == "harvard":
        names = [a for a in (doc.get("authors") or []) if a]
        sf = _sf(doc)
        who = (f"{surname(names[0], sf)}, {initials(names[0], sf)}" if len(names) == 1
               else f"{surname(names[0], sf)} et al." if names else "")
        return " ".join(b for b in (who, f"({year})" if year else "",
                                    f"'{t}',", f"{venue}." if venue else "",
                                    url or "") if b).strip()
    if style == "mla":
        names = [a for a in (doc.get("authors") or []) if a]
        sf = _sf(doc)
        who = (f"{surname(names[0], sf)}, {initials(names[0], sf)}"
               if len(names) == 1 else
               f"{surname(names[0], sf)}, et al" if names else "")
        return " ".join(b for b in (who + "." if who else "", f'"{t}."' if t else "",
                                    f"{venue}," if venue else "",
                                    f"{year}," if year else "", url or "") if b).strip()
    if style == "chicago":
        names = [a for a in (doc.get("authors") or []) if a]
        sf = _sf(doc)
        who = f"{surname(names[0], sf)}, {initials(names[0], sf)}" if names else ""
        return " ".join(b for b in (who + "." if who else "", f'"{t}."' if t else "",
                                    f"{venue}" if venue else "",
                                    f"({year})." if year else "", url or "") if b).strip()
    if style == "bibtex":
        names = [a for a in (doc.get("authors") or []) if a]
        key = re.sub(r"[^a-z0-9]", "",
                     (surname(names[0], _sf(doc)) if names else "prism").lower())
        key = f"{key}{year or ''}"
        rows = [f"  title = {{{t}}}"]
        if names:
            rows.append("  author = {" + " and ".join(names) + "}")
        if venue:
            rows.append(f"  journal = {{{venue}}}")
        if year:
            rows.append(f"  year = {{{year}}}")
        if doc.get("doi"):
            rows.append(f"  doi = {{{doc['doi']}}}")
        if url:
            rows.append(f"  url = {{{url}}}")
        return "@article{" + key + ",\n" + ",\n".join(rows) + "\n}"
    if style == "inline_link":
        anchor = html.escape(label(doc) or t[:60])
        return f'<a href="{html.escape(url or "#")}" rel="noopener">{anchor}</a>' \
               if url else anchor
    if style == "footnote":
        return render(doc, "vancouver")
    if style == "numbered":
        n = index if index is not None else 1
        return f"[{n}] " + render(doc, "vancouver")
    if style == "source_card":
        return _card(doc)
    if style == "wordpress":
        return _wp(doc)
    return render(doc, "apa")


def _card(doc: dict) -> str:
    """A self-contained evidence card. Inline styles, no classes and no script:
    it is pasted into somebody else's stylesheet and must survive it."""
    url, t = _url(doc), html.escape(_title(doc))
    head = f'<a href="{html.escape(url)}" rel="noopener" style="color:inherit">{t}</a>' \
        if url else t
    meta = " &middot; ".join(html.escape(str(x)) for x in (
        label(doc), doc.get("venue"), doc.get("year")) if x)
    strength = html.escape(str(doc.get("strength") or ""))
    why = html.escape(str(doc.get("why_tier") or ""))
    quote = doc.get("quote")
    q = (f'<blockquote style="margin:.6em 0 0;padding-left:.8em;border-left:3px '
         f'solid #d8d8d8;color:#444;font-style:italic">{html.escape(quote)}'
         f'</blockquote>') if quote else ""
    return (
        f'<div class="prism-evidence" style="border:1px solid #e3e3e3;border-radius:8px;'
        f'padding:.9em 1em;margin:1em 0;font-size:.95em;line-height:1.5">'
        f'<div style="font-weight:600;margin-bottom:.25em">{head}</div>'
        f'<div style="color:#666;font-size:.9em">{meta}</div>'
        f'<div style="margin-top:.4em"><span style="display:inline-block;'
        f'background:#f2f4f7;border-radius:4px;padding:.1em .5em;font-size:.85em">'
        f'{strength} evidence</span> <span style="color:#666;font-size:.85em">'
        f'{why}</span></div>{q}</div>')


def _wp(doc: dict) -> str:
    """A WordPress shortcode a plugin can expand server-side, keeping the post
    content portable if the plugin is later removed."""
    parts = [f'id="{doc.get("id", "")}"']
    for k in ("doi", "year", "tier", "strength"):
        if doc.get(k):
            parts.append(f'{k}="{html.escape(str(doc[k]))}"')
    if doc.get("title"):
        parts.append(f'title="{html.escape(doc["title"])}"')
    if _url(doc):
        parts.append(f'url="{html.escape(_url(doc))}"')
    return "[prism_evidence " + " ".join(parts) + "]"


def bibliography(docs: list, style: str = "apa") -> dict:
    """A whole reference list, plus the inline markers that point into it."""
    style = (style or "apa").lower()
    items, markers = [], []
    for i, d in enumerate(docs, 1):
        items.append({"n": i, "id": d.get("id"), "citation": render(d, style, index=i),
                      "url": _url(d), "tier": d.get("tier"),
                      "strength": d.get("strength")})
        markers.append({"n": i, "id": d.get("id"),
                        "inline": (f"[{i}]" if style in ("numbered", "footnote", "vancouver")
                                   else f"({label(d)})" if label(d) else f"[{i}]")})
    return {"style": style, "entries": items, "inline_markers": markers,
            "styles_available": list(STYLES)}
