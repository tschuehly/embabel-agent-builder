#!/usr/bin/env python3
"""Fetch one Embabel docs file by repository-relative docs path.

By default, resolve the Embabel docs ref from the target project's
`embabel-agent.version` Maven property and fetch docs from that release tag,
for example `v0.3.4`.
"""

from __future__ import annotations

import argparse
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

RAW_ROOT = "https://raw.githubusercontent.com/embabel/embabel-agent"
DOCS_ROOT = "embabel-agent-docs/src/main/asciidoc"


def resolve_embabel_version(project_dir: Path) -> str | None:
    pom = project_dir / "pom.xml"
    if not pom.exists():
        return None
    text = pom.read_text(encoding="utf-8")
    match = re.search(r"<embabel-agent\.version>\s*([^<\s]+)\s*</embabel-agent\.version>", text)
    if match:
        return match.group(1)
    return None


def ref_for_version(version: str) -> str:
    return version if version.startswith(("v", "refs/", "main")) else f"v{version}"


def fetch_url(url: str) -> str:
    with urllib.request.urlopen(url, timeout=30) as response:
        return response.read().decode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Docs path, for example reference/annotations/page.adoc")
    parser.add_argument(
        "--project-dir",
        default=".",
        help="Project directory containing pom.xml. Defaults to the current working directory.",
    )
    parser.add_argument(
        "--version",
        help="Embabel artifact version to use for docs, for example 0.3.4. Overrides --project-dir detection.",
    )
    parser.add_argument(
        "--ref",
        help="Exact embabel-agent git ref to use for docs, for example v0.3.4. Overrides version detection.",
    )
    parser.add_argument("--out", help="Optional output file. Prints to stdout when omitted.")
    args = parser.parse_args()

    doc_path = args.path.lstrip("/")
    if ".." in Path(doc_path).parts:
        print("Refusing path containing '..'", file=sys.stderr)
        return 2
    if not doc_path.endswith((".adoc", ".md", ".html", ".js")):
        print("Expected a docs file path ending in .adoc, .md, .html, or .js", file=sys.stderr)
        return 2

    project_dir = Path(args.project_dir).resolve()
    version = args.version or resolve_embabel_version(project_dir)
    ref = args.ref or (ref_for_version(version) if version else None)
    if not ref:
        print(
            "Could not determine Embabel docs ref. Pass --ref, --version, or run from a Maven project with "
            "<embabel-agent.version>.",
            file=sys.stderr,
        )
        return 2

    url = f"{RAW_ROOT}/{ref}/{DOCS_ROOT}/{doc_path}"
    try:
        content = fetch_url(url)
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
