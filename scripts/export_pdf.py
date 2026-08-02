"""Export report/index.html to a print-quality PDF via Playwright Chromium."""
from __future__ import annotations

import sys
from pathlib import Path

from build_html import main as build_html
from lib_common import ROOT

OUT = ROOT / "report" / "FStock_Opportunity_Report.pdf"


def main() -> int:
    html_path = build_html()
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright not installed. Run: pip install playwright && playwright install chromium")
        return 1

    url = html_path.resolve().as_uri()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        page.emulate_media(media="print")
        page.pdf(
            path=str(OUT),
            format="A4",
            print_background=True,
            display_header_footer=True,
            header_template=(
                '<div style="font-size:8px; width:100%; text-align:center; '
                'color:#6e6e73; font-family:-apple-system,BlinkMacSystemFont,sans-serif;">'
                "F Stock · 全 AI 无人公司商业机会报告 · v1.0.0"
                "</div>"
            ),
            footer_template=(
                '<div style="font-size:8px; width:100%; padding:0 14mm; '
                "color:#6e6e73; font-family:-apple-system,BlinkMacSystemFont,sans-serif; "
                'display:flex; justify-content:space-between;">'
                "<span>Confidential · Not investment advice</span>"
                '<span><span class="pageNumber"></span> / <span class="totalPages"></span></span>'
                "</div>"
            ),
            margin={"top": "18mm", "bottom": "18mm", "left": "12mm", "right": "12mm"},
        )
        browser.close()

    print("Wrote", OUT)
    print("Size bytes:", OUT.stat().st_size)
    return 0


if __name__ == "__main__":
    sys.exit(main())
