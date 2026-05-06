#!/usr/bin/env python3
"""Fetch one current Embabel AsciiDoc file by repository-relative docs path."""

from __future__ import annotations

import argparse
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = "https://raw.githubusercontent.com/embabel/embabel-agent/main/embabel-agent-docs/src/main/asciidoc"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Docs path, for example reference/annotations/page.adoc")
    parser.add_argument("--out", help="Optional output file. Prints to stdout when omitted.")
    args = parser.parse_args()

    doc_path = args.path.lstrip("/")
    if ".." in Path(doc_path).parts:
        print("Refusing path containing '..'", file=sys.stderr)
        return 2
    if not doc_path.endswith((".adoc", ".md", ".html", ".js")):
        print("Expected a docs file path ending in .adoc, .md, .html, or .js", file=sys.stderr)
        return 2

    url = f"{ROOT}/{doc_path}"
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            content = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        print(f"Failed to fetch {url}: HTTP {exc.code}", file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        print(f"Failed to fetch {url}: {exc.reason}", file=sys.stderr)
        return 1

    if args.out:
        Path(args.out).write_text(content, encoding="utf-8")
    else:
        print(content, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
