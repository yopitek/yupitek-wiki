import json

import fix_toc_anchors as ft

DOC = """# Manual

## Table of Contents

- [**1. Product Overview & Hardware Architecture**](#1-product-overview-hardware-architecture)
  - [1.1 The Shark Jack by Hak5](#1-1-the-shark-jack-by-hak5)
  - [ok](#already-fine)
  - [nope](#totally-missing-heading)

## 1. Product Overview & Hardware Architecture

### 1.1 The Shark Jack by Hak5

## Already Fine

## Dup

## Dup

```
[code](#1-1-the-shark-jack-by-hak5)
```
"""


def self_lookup(doc):
    return lambda p: ft.headings(doc) if p == "" else None


def test_slugify_matches_github_slugger():
    assert ft.slugify("1. Product Overview & Hardware Architecture") == "1-product-overview--hardware-architecture"
    assert ft.slugify("1.1 The Shark Jack by Hak5") == "11-the-shark-jack-by-hak5"
    assert ft.slugify("Linux: Install GQRX (recommended)") == "linux-install-gqrx-recommended"
    assert ft.slugify("5.2 Configuring Cloud C\u00b2") == "52-configuring-cloud-c"
    assert ft.slugify("安裝 `GQRX` 步驟") == "安裝-gqrx-步驟"


def test_heading_ids_dedupe_skip_code_and_honor_explicit_ids():
    hs = ft.headings("## Dup\n\n## Dup\n\n```\n## no\n```\n## [Link](x) *em* {#custom}\n")
    assert [i for _, i in hs] == ["dup", "dup-1", "custom"]


def test_norm_key_ignores_punctuation_and_hyphens():
    assert ft.norm_key("1-1-the-shark-jack") == ft.norm_key("11-the-shark-jack")
    assert ft.norm_key("a--b") == ft.norm_key("a-b")


def test_fix_text_rewrites_unique_match_and_reports_the_rest():
    out, fixed, unmatched = ft.fix_text(DOC, self_lookup(DOC))
    assert "(#1-product-overview--hardware-architecture)" in out
    assert "(#11-the-shark-jack-by-hak5)" in out
    assert "[ok](#already-fine)" in out                      # valid id untouched
    assert "[code](#1-1-the-shark-jack-by-hak5)" in out      # fenced code untouched
    assert fixed == 2
    assert [u["anchor"] for u in unmatched] == ["totally-missing-heading"]


def test_ambiguous_match_is_not_guessed():
    doc = "[a](#dup)\n\n## D Up\n\n## D-Up\n"
    out, fixed, unmatched = ft.fix_text(doc, self_lookup(doc))
    assert out == doc and fixed == 0 and unmatched[0]["reason"] == "ambiguous"


def test_unknown_target_page_and_external_links_are_ignored():
    doc = "[a](/nope/#x) [b](https://e.com/#y)\n"
    out, fixed, unmatched = ft.fix_text(doc, lambda p: None)
    assert out == doc and fixed == 0 and unmatched == []


def test_cross_page_route_is_resolved_and_rewritten():
    seen = []

    def look(p):
        seen.append(p)
        return ft.headings("## Mayhem Firmware (v2)\n")

    out, fixed, _ = ft.fix_text("[x](/sdrlab/hardware/h4m/#mayhem-firmware--v2-)\n", look)
    assert seen == ["/sdrlab/hardware/h4m/"]
    assert fixed == 1 and "(/sdrlab/hardware/h4m/#mayhem-firmware-v2)" in out


def test_route_map_strips_numeric_prefixes(tmp_path):
    for rel in ["04-sdrlab/firmware.md", "04-sdrlab/hardware/h4m/index.md", "index.md"]:
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("# t\n")
    routes = ft.route_map(tmp_path)
    assert routes["/sdrlab/firmware"].name == "firmware.md"
    assert routes["/sdrlab/hardware/h4m"].name == "index.md"
    assert routes["/sdrlab/hardware/h4m/"] == routes["/sdrlab/hardware/h4m"]
    assert routes["/"].name == "index.md"


def test_run_applies_changes_and_writes_unmatched_json(tmp_path):
    root = tmp_path / "docs"
    (root / "01-a").mkdir(parents=True)
    f = root / "01-a" / "p.md"
    f.write_text(DOC)
    out_json = tmp_path / "out" / "toc_unmatched.json"
    stats = ft.run([root], out_json)
    assert stats["fixed"] == 2 and stats["unmatched"] == 1
    assert "(#11-the-shark-jack-by-hak5)" in f.read_text()
    data = json.loads(out_json.read_text())
    assert len(data) == 1 and data[0]["file"].endswith("p.md")
    assert ft.run([root], out_json)["fixed"] == 0            # idempotent


def test_run_preserves_crlf_and_lone_cr(tmp_path):
    root = tmp_path / "docs"
    root.mkdir()
    f = root / "p.md"
    raw = "## Abc Def\r\n[a](#abcdef)\r\nodd\rline\r\n".encode()
    f.write_bytes(raw)
    ft.run([root], tmp_path / "u.json")
    assert f.read_bytes() == raw.replace(b"#abcdef", b"#abc-def")
