#!/usr/bin/env python3
"""Fail if a sitemap URL would be redirected by Cloudflare Pages instead of served directly.

Pages serves `/a/b/` from `a/b/index.html` and `/a/b` from `a/b.html`; a URL without the
trailing slash whose page was built as `a/b/index.html` gets a 308 to `/a/b/`.
Usage: python3 scripts/check_sitemap_urls.py build"""
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse


def served_directly(build: Path, url: str) -> bool:
    path = unquote(urlparse(url).path).lstrip("/")
    if path == "" or path.endswith("/"):
        return (build / path / "index.html").is_file()
    return (build / f"{path}.html").is_file()


def main() -> int:
    build = Path(sys.argv[1])
    urls = re.findall(r"<loc>([^<]+)</loc>", (build / "sitemap.xml").read_text())
    bad = [u for u in urls if not served_directly(build, u)]
    for u in bad[:20]:
        print("REDIRECTS", u)
    print(f"{len(urls)} sitemap URLs, {len(bad)} would redirect")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
