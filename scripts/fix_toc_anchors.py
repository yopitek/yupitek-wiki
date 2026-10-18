#!/usr/bin/env python3
"""Rewrite hand-written `#anchor` links to the github-slugger heading id.

A link is rewritten only when its target heading id does not exist AND exactly
one heading on the target page matches by normalized text. Everything else is
reported to out/toc_unmatched.json instead of being guessed.

Usage: uv run python scripts/fix_toc_anchors.py [--dry-run]
"""
import json
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
LINK = re.compile(r"\]\(([^)\s#]*)#([^)\s]+)\)")
HEADING = re.compile(r"^ {0,3}(#{1,6})\s+(.*?)\s*#*\s*$")
EXPLICIT = re.compile(r"\s*\{#([^}\s]+)\}\s*$")
CODE_SPAN = re.compile(r"(`[^`]*`)")
FENCE = re.compile(r"^\s*(```|~~~)")


def _keeps(c):
    """github-slugger keeps letters, digits (not No like superscripts), marks, _ - and space."""
    cat = unicodedata.category(c)
    return c in "_- " or cat[0] == "M" or (c.isalnum() and cat != "No")


def slugify(text):
    text = re.sub(r"[`*~\\]|<[^>]+>", "", text).strip().lower()
    keep = (c for c in text if _keeps(c))
    return "".join("-" if c == " " else c for c in keep)


def norm_key(s):
    return re.sub(r"[\W_]+", "", unquote(s).lower())


def _plain(text):
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", text)
    return re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)


def _body_lines(text):
    """Yield (index, line) for lines outside fenced code blocks."""
    fenced = False
    for i, line in enumerate(text.split("\n")):
        if FENCE.match(line):
            fenced = not fenced
        elif not fenced:
            yield i, line


def headings(md):
    """Return [(text_slug, id)] in document order, ids deduped like github-slugger."""
    out, seen = [], {}
    for _, line in _body_lines(md):
        m = HEADING.match(line)
        if not m:
            continue
        raw = m.group(2)
        ex = EXPLICIT.search(raw)
        base = slugify(_plain(EXPLICIT.sub("", raw)))
        if ex:
            out.append((base, ex.group(1)))
            continue
        n = seen.get(base, 0)
        seen[base] = n + 1
        out.append((base, base if n == 0 else f"{base}-{n}"))
    return out


def _fix_anchor(path, anchor, lookup):
    """Return (new_anchor|None, problem|None); None/None means leave alone."""
    hs = lookup(path)
    if hs is None:
        return None, None
    want = unquote(anchor)
    if any(want == i for _, i in hs):
        return None, None
    hits = [i for t, i in hs if norm_key(t) == norm_key(want)]
    if len(hits) == 1:
        return hits[0], None
    return None, "ambiguous" if hits else "no_heading_match"


def fix_text(text, lookup):
    """Return (new_text, fixed_count, unmatched[]). lookup(path)->headings|None."""
    lines, fixed, unmatched = text.split("\n"), 0, []
    for i, line in _body_lines(text):
        parts = CODE_SPAN.split(line)
        for k in range(0, len(parts), 2):          # even parts are outside code spans
            def sub(m, i=i):
                nonlocal fixed
                new, problem = _fix_anchor(m.group(1), m.group(2), lookup)
                if problem:
                    unmatched.append({"line": i + 1, "target": m.group(1) or "(self)",
                                      "anchor": m.group(2), "reason": problem})
                if new is None:
                    return m.group(0)
                fixed += 1
                return f"]({m.group(1)}#{new})"
            parts[k] = LINK.sub(sub, parts[k])
        lines[i] = "".join(parts)
    return "\n".join(lines), fixed, unmatched


def route_map(root):
    """Map doc routes ('/hak5/products/x' and with trailing '/') to files."""
    routes = {}
    for f in sorted(Path(root).rglob("*.md*")):
        rel = f.relative_to(root).with_suffix("")
        parts = [re.sub(r"^\d+-", "", p) for p in rel.parts]
        if parts[-1] == "index":
            parts = parts[:-1]
        route = "/" + "/".join(parts)
        routes[route] = f
        routes[route.rstrip("/") + "/"] = f
    return routes


def _read(path):
    """Read without newline translation so CRLF / lone CR survive the round trip."""
    return path.read_bytes().decode("utf-8")


def _make_lookup(f, routes):
    cache = {}

    def lookup(path):
        if re.match(r"^[a-z][a-z0-9+.-]*:", path):
            return None
        if path == "":
            target = f
        elif path.startswith("/"):
            target = routes.get(path)
        else:
            target = (f.parent / path).resolve() if path.endswith((".md", ".mdx")) else None
        if target is None or not Path(target).is_file():
            return None
        if target not in cache:
            cache[target] = headings(_read(Path(target)))
        return cache[target]

    return lookup


def run(roots, out_json, write=True):
    stats, report = {"files": 0, "fixed": 0, "unmatched": 0}, []
    for root in roots:
        root, routes = Path(root), route_map(root)
        for f in sorted(root.rglob("*.md*")):
            text = _read(f)
            new, fixed, unmatched = fix_text(text, _make_lookup(f, routes))
            if write and new != text:
                f.write_bytes(new.encode("utf-8"))
                stats["files"] += 1
            stats["fixed"] += fixed
            report += [{"file": str(f), **u} for u in unmatched]
    stats["unmatched"] = len(report)
    out_json = Path(out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return stats


def main(argv):
    roots = [ROOT / "docs", *sorted((ROOT / "i18n").glob("*/docusaurus-plugin-content-docs/current"))]
    stats = run(roots, ROOT / "out" / "toc_unmatched.json", write="--dry-run" not in argv)
    print(json.dumps(stats))


if __name__ == "__main__":
    main(sys.argv[1:])
