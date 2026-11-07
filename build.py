#!/usr/bin/env python3
"""Build the combined print-ready packet for the Nurse Shift-Swap Pack.

Reads the individual print sheets in print/*.html, inlines the shared
stylesheet, adds a cover sheet, and writes one self-contained HTML file
to _build/nurse-shift-swap-packet.html ready for File > Print.

Education only - not medical advice.
Copyright (c) 2026 Asdale Dynamics, LLC. MIT License.
"""

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PRINT = ROOT / "print"
BUILD = ROOT / "_build"

SHEETS = [
    ("shift-swap-request-text.html", "Kind shift-swap request scripts (text)"),
    ("shift-swap-request-email.html", "Shift-swap request emails (colleague + manager)"),
    ("unit-approval-checklist.html", "Unit-approval checklist"),
    ("coverage-math-one-pager.html", "Coverage math one-pager"),
    ("swap-confirmation-tracker.html", "Swap-confirmation tracker cards"),
    ("thank-you-coupons.html", "Thank-you coupons"),
]

COVER = f"""<article class="sheet cover">
<header class="pack-head">
  <p class="brand">Nurse Shift-Swap Pack &middot; Asdale Dynamics, LLC</p>
  <h1>The Nurse Shift-Swap Pack</h1>
</header>
<p class="cover-tagline">Kind scripts, honest math, and paper trails for trading
shifts with grace. Made like a friend would: plain English, step by step, never
condescending.</p>
<h2>What's inside</h2>
<ul>
  <li>Kind shift-swap request scripts (text)</li>
  <li>Shift-swap request emails (colleague + manager)</li>
  <li>Unit-approval checklist</li>
  <li>Coverage math one-pager</li>
  <li>Swap-confirmation tracker cards</li>
  <li>Thank-you coupons for the colleague who bails you out</li>
</ul>
<h2>How to use this packet</h2>
<ul class="check">
    <li>Print the sheets you need (or all six) on Letter or A4 paper.</li>
    <li>Write right on the pages: these are posters, cards, and coupons, not homework.</li>
    <li>Check dates against your unit's own policy before every swap.</li>
</ul>
<p class="cover-credit">A free pack by <strong>Asdale Dynamics, LLC</strong> &mdash;
AI explained &ldquo;like a friend would&rdquo; by Dylan Asdale, RN.
Distributed under the MIT License.</p>
</article>"""


def extract_sheet(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8")
    title_match = re.search(r"<title>(.*?)</title>", text, re.DOTALL)
    sheet_match = re.search(
        r"(<article class=\"sheet\".*?</article>)", text, re.DOTALL
    )
    if not sheet_match:
        raise ValueError(f"No <article> sheet found in {path.name}")
    return (title_match.group(1) if title_match else path.stem, sheet_match.group(1))


def build() -> Path:
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    title_parts, sheet_parts = ["The Nurse Shift-Swap Pack"], [COVER]
    for filename, sheet_title in SHEETS:
        page_title, sheet_html = extract_sheet(PRINT / filename)
        title_parts.append(page_title)
        sheet_parts.append(sheet_html)

    document = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Free nurse shift-swap pack: kind request scripts, approval checklist, coverage math, tracker cards, and thank-you coupons. Education only, not medical advice.">
<title>{html.escape(" — ".join(title_parts))}</title>
<style>
{css}
</style>
</head>
<body>
{chr(10).join(sheet_parts)}
</body>
</html>
"""
    BUILD.mkdir(exist_ok=True)
    out = BUILD / "nurse-shift-swap-packet.html"
    out.write_text(document, encoding="utf-8")
    return out


if __name__ == "__main__":
    out = build()
    print(f"Wrote {out.relative_to(ROOT)} ({out.stat().st_size:,} bytes)")
