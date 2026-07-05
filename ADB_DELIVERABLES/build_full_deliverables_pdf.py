#!/usr/bin/env python3
"""Build a full deliverables summary PDF from the original proposal plus SaiFE outputs."""

from __future__ import annotations

import csv
import html
import re
import shutil
import subprocess
from collections import Counter, defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUTPUT_DIR = HERE / "outputs"
PROPOSAL_MD = HERE / "ADB_road_speed_policy_proposal.md"
FINDINGS_MD = HERE / "FINDINGS_SUMMARY.md"
METHODOLOGY_MD = HERE / "SAFE_SYSTEM_METHODOLOGY.md"
TEMPORAL_MD = HERE / "TEMPORAL_DATA_AUDIT.md"
SCORES_CSV = OUTPUT_DIR / "safe_system_segment_scores.csv"
TIME_CSV = OUTPUT_DIR / "time_based_speed_management_candidates.csv"
HTML_OUTPUT = OUTPUT_DIR / "SaiFE_full_deliverables_summary.html"
PDF_OUTPUT = OUTPUT_DIR / "SaiFE_full_deliverables_summary.pdf"


PRIORITY_ORDER = ["Critical review", "High priority", "Monitor / validate", "Lower priority"]
PRIORITY_COLORS = {
    "Critical review": "#7f1d1d",
    "High priority": "#dc2626",
    "Monitor / validate": "#f59e0b",
    "Lower priority": "#16a34a",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def fnum(value: str | float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def markdown_excerpt(path: Path, start_heading: str, stop_heading: str | None = None) -> str:
    text = path.read_text(encoding="utf-8")
    start = text.find(start_heading)
    if start < 0:
        return ""
    if stop_heading:
        stop = text.find(stop_heading, start + len(start_heading))
        if stop >= 0:
            return text[start:stop].strip()
    return text[start:].strip()


def md_to_html(md: str) -> str:
    lines = md.splitlines()
    out = []
    in_ul = False
    in_ol = False
    in_table = False
    table_rows: list[str] = []

    def close_lists() -> None:
        nonlocal in_ul, in_ol
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if in_ol:
            out.append("</ol>")
            in_ol = False

    def flush_table() -> None:
        nonlocal in_table, table_rows
        if not in_table:
            return
        out.append("<table>")
        for idx, row in enumerate(table_rows):
            cells = [c.strip() for c in row.strip("|").split("|")]
            if idx == 1 and all(set(c) <= {"-", ":", " "} for c in cells):
                continue
            tag = "th" if idx == 0 else "td"
            out.append("<tr>" + "".join(f"<{tag}>{html.escape(c)}</{tag}>" for c in cells) + "</tr>")
        out.append("</table>")
        in_table = False
        table_rows = []

    for raw in lines:
        line = raw.rstrip()
        if line.startswith("|") and line.endswith("|"):
            close_lists()
            in_table = True
            table_rows.append(line)
            continue
        flush_table()

        if not line:
            close_lists()
            continue
        if line.startswith("### "):
            close_lists()
            out.append(f"<h3>{html.escape(line[4:])}</h3>")
        elif line.startswith("## "):
            close_lists()
            out.append(f"<h2>{html.escape(line[3:])}</h2>")
        elif line.startswith("# "):
            close_lists()
            out.append(f"<h1>{html.escape(line[2:])}</h1>")
        elif line.startswith("- "):
            if not in_ul:
                close_lists()
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{inline_md(line[2:])}</li>")
        elif re.match(r"^\d+\. ", line):
            if not in_ol:
                close_lists()
                out.append("<ol>")
                in_ol = True
            item_text = re.sub(r"^\d+\. ", "", line)
            out.append(f"<li>{inline_md(item_text)}</li>")
        else:
            close_lists()
            out.append(f"<p>{inline_md(line)}</p>")

    flush_table()
    close_lists()
    return "\n".join(out)


def inline_md(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"`(.+?)`", r"<code>\1</code>", escaped)
    return escaped


def grouped_bar_chart(data: dict[str, dict[str, int]], title: str) -> str:
    countries = list(data)
    width, height = 860, 350
    margin_l, margin_r, margin_t, margin_b = 78, 28, 52, 66
    plot_w = width - margin_l - margin_r
    plot_h = height - margin_t - margin_b
    max_v = max(max(country_data.values()) for country_data in data.values()) or 1
    group_w = plot_w / len(countries)
    bar_w = group_w / (len(PRIORITY_ORDER) + 1)
    parts = [
        f'<svg viewBox="0 0 {width} {height}">',
        f'<text x="{margin_l}" y="28" class="chart-title">{html.escape(title)}</text>',
    ]
    for tick in range(5):
        value = max_v * tick / 4
        y = margin_t + plot_h - (value / max_v) * plot_h
        parts.append(f'<line x1="{margin_l}" y1="{y:.1f}" x2="{width - margin_r}" y2="{y:.1f}" stroke="#e2e8f0"/>')
        parts.append(f'<text x="{margin_l - 8}" y="{y + 4:.1f}" text-anchor="end" class="axis">{value:,.0f}</text>')
    for i, country in enumerate(countries):
        x0 = margin_l + i * group_w + bar_w * 0.5
        for j, label in enumerate(PRIORITY_ORDER):
            value = data[country].get(label, 0)
            bar_h = (value / max_v) * plot_h
            x = x0 + j * bar_w
            y = margin_t + plot_h - bar_h
            parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w * 0.78:.1f}" height="{bar_h:.1f}" fill="{PRIORITY_COLORS[label]}"/>')
        parts.append(f'<text x="{margin_l + i * group_w + group_w / 2:.1f}" y="{height - 30}" text-anchor="middle" class="axis-label">{html.escape(country)}</text>')
    legend_x = margin_l
    for label in PRIORITY_ORDER:
        parts.append(f'<rect x="{legend_x}" y="{height - 18}" width="11" height="11" fill="{PRIORITY_COLORS[label]}"/>')
        parts.append(f'<text x="{legend_x + 16}" y="{height - 8}" class="legend">{html.escape(label)}</text>')
        legend_x += 155
    parts.append("</svg>")
    return "\n".join(parts)


def horizontal_bar_chart(items: list[tuple[str, float]], title: str, color: str) -> str:
    width, row_h = 860, 28
    margin_l, margin_r, margin_t, margin_b = 260, 58, 50, 24
    height = margin_t + margin_b + row_h * len(items)
    max_v = max((v for _, v in items), default=1) or 1
    plot_w = width - margin_l - margin_r
    parts = [
        f'<svg viewBox="0 0 {width} {height}">',
        f'<text x="0" y="28" class="chart-title">{html.escape(title)}</text>',
    ]
    for i, (label, value) in enumerate(items):
        y = margin_t + i * row_h
        bar_w = (value / max_v) * plot_w
        parts.append(f'<text x="{margin_l - 10}" y="{y + 16}" text-anchor="end" class="axis-label">{html.escape(label[:42])}</text>')
        parts.append(f'<rect x="{margin_l}" y="{y}" width="{bar_w:.1f}" height="18" fill="{color}"/>')
        parts.append(f'<text x="{margin_l + bar_w + 8:.1f}" y="{y + 14}" class="axis">{value:,.0f}</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def table(rows: list[dict[str, str]], columns: list[tuple[str, str]]) -> str:
    head = "".join(f"<th>{html.escape(label)}</th>" for _, label in columns)
    body_rows = []
    for row in rows:
        cells = "".join(f"<td>{html.escape(str(row.get(key, '')))}</td>" for key, _ in columns)
        body_rows.append(f"<tr>{cells}</tr>")
    return f"<table><thead><tr>{head}</tr></thead><tbody>{''.join(body_rows)}</tbody></table>"


def chrome_path() -> str | None:
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return candidate
    return shutil.which("google-chrome") or shutil.which("chromium")


def build_html() -> str:
    rows = read_rows(SCORES_CSV)
    time_rows = read_rows(TIME_CSV) if TIME_CSV.exists() else []
    by_country_priority: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for row in rows:
        by_country_priority[row["country"]][row["priority_class"]] += 1
    action_counts = Counter(row["recommended_action"] for row in rows if fnum(row["speed_safety_score"]) >= 50)

    proposal_intro = markdown_excerpt(PROPOSAL_MD, "## Executive Summary", "## Dataset Scope")

    top_segments = rows[:12]
    time_counts = Counter(row["time_pilot_type"] for row in time_rows)

    html_text = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>SaiFE Full Deliverables Summary</title>
  <style>
    @page {{ size: A4; margin: 15mm; }}
    body {{ font-family: Arial, sans-serif; color: #172033; line-height: 1.38; }}
    h1 {{ font-size: 24px; margin: 0 0 5px; }}
    h2 {{ font-size: 16px; margin: 18px 0 7px; border-bottom: 1px solid #cbd5e1; padding-bottom: 4px; }}
    h3 {{ font-size: 13px; margin: 12px 0 5px; }}
    p, li {{ font-size: 10.5px; }}
    code {{ background: #f1f5f9; padding: 1px 3px; }}
    .subtitle {{ color: #475569; margin-top: 0; }}
    .metric-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin: 12px 0; }}
    .metric {{ border: 1px solid #cbd5e1; padding: 8px; border-radius: 4px; }}
    .metric strong {{ display: block; font-size: 18px; }}
    .metric span {{ font-size: 9.5px; color: #475569; }}
    svg {{ width: 100%; height: auto; margin: 5px 0 10px; }}
    .chart-title {{ font-weight: 700; font-size: 15px; fill: #172033; }}
    .axis, .legend {{ font-size: 10px; fill: #475569; }}
    .axis-label {{ font-size: 10px; fill: #172033; }}
    table {{ border-collapse: collapse; width: 100%; margin: 7px 0 11px; font-size: 8.8px; }}
    th, td {{ border: 1px solid #cbd5e1; padding: 3.5px 4px; vertical-align: top; }}
    th {{ background: #f1f5f9; text-align: left; }}
    .page-break {{ break-before: page; }}
    .note {{ background: #f8fafc; border-left: 4px solid #64748b; padding: 8px 10px; }}
  </style>
</head>
<body>
  <h1>SaiFE Full Deliverables Summary</h1>
  <p class="subtitle">Safe AI Framework for Speed-Limit Evaluation | Original ADB proposal narrative plus segment-level SaiFE scoring outputs</p>
  <div class="metric-grid">
    <div class="metric"><strong>{len(rows):,}</strong><span>usable segments scored</span></div>
    <div class="metric"><strong>{sum(1 for r in rows if fnum(r['speed_safety_score']) >= 50):,}</strong><span>priority segments scoring 50+</span></div>
    <div class="metric"><strong>{sum(1 for r in rows if r['priority_class'] == 'Critical review'):,}</strong><span>critical-review segments</span></div>
    <div class="metric"><strong>{len(time_rows):,}</strong><span>time-pilot candidates</span></div>
  </div>

  {md_to_html(proposal_intro)}

  <h2>SaiFE Scoring Add-On</h2>
  <p>The original deliverables provided a cross-country speed-management proposal and interactive policy story. SaiFE adds a reproducible segment-level scoring layer, a public map, a findings summary, a temporal data audit, and a time-based speed-management candidate list.</p>
  <p>The Speed Safety Score is a transparent 0-100 score built from six components: posted limit alignment, operating speed behavior, exposure proxy, vulnerable-user context, geometry, and data-quality review. Segments scoring 50 or above are treated as priority speed-unsafe segments for review.</p>

  <div class="page-break"></div>
  <h2>What the Model Found</h2>
  <p>SaiFE scored 14,711 usable road segments. Thailand produced 131 Critical-review segments and 6,114 High-priority segments. Maharashtra produced 484 High-priority segments. The strongest signals occur where high posted limits, high observed speeds, urban or major-road context, exposure proxies, and geometry concerns combine.</p>
  <p>Thailand's highest-scoring segments are mainly urban expressways and major trunk or primary roads, including Prachim Ratthaya Expressway, Chalong Rat Expressway, Borommaratchachonnani Elevated Highway, Phahonyothin Road, Phetkasem Road, Sukhumvit Road, and Mittraphap Road. Maharashtra's highest-scoring segments include Yavatmal Bypass, JNPT Road, Amravati Bypass, urban trunk-road flyover segments, and rural trunk-road segments with high F85 speeds.</p>
  {grouped_bar_chart(dict(by_country_priority), "Priority classes by country")}

  <h3>Top Scored Segments</h3>
  {table(top_segments, [
      ("country", "Country"),
      ("road_name", "Road"),
      ("road_class", "Class"),
      ("land_use", "Land use"),
      ("speed_limit", "Limit"),
      ("f85_speed", "F85"),
      ("speed_safety_score", "Score"),
      ("recommended_action", "Recommended action"),
  ])}

  <div class="page-break"></div>
  <h2>How a Ministry Could Use SaiFE</h2>
  <p>A transport ministry or road safety agency could use SaiFE as a first-stage screening tool for speed management. It can inform national speed-limit review, corridor enforcement planning, average-speed camera pilots, road-design review, field validation, speed-limit inventory QA, and crash-data matching.</p>
  <p>The model is designed to support decisions about where to investigate first, not to make automatic final policy decisions. Each priority segment receives a recommended action so agencies can distinguish speed-limit review, road-design and speed-management review, enforcement, QA, and monitoring cases.</p>
  {horizontal_bar_chart(action_counts.most_common(8), "Recommended action categories for priority segments", "#7c3aed")}

  <h2>Temporal / Dynamic Speed Management</h2>
  <p>The supplied GeoJSON files do not contain timestamp, hour, day/night, weekday, month, or time-period fields. SaiFE therefore does not claim to prove day/night speeding patterns from the current data. Instead, it generates a first-wave candidate list for where segment-hour data should be collected first.</p>
  <p>These candidates can support future variable speed limits, night enforcement, school-zone windows, average-speed enforcement, and motorcycle safety programs once segment-hour speed data and crash records are available.</p>
  {horizontal_bar_chart(time_counts.most_common(8), "Time-based pilot candidate types", "#0f766e") if time_counts else ""}

  <div class="page-break"></div>
  <h2>Validation, Limitations, and Replication</h2>
  <p>SaiFE was validated through reproducibility checks, schema inspection, and face-validity review of the highest-scoring segments. The key limitation is that the supplied datasets do not include crash outcomes, traffic volumes, vulnerable-user exposure counts, or time-of-day speed records. Final investment decisions should combine SaiFE outputs with crash data, traffic counts, field audits, and local engineering review.</p>
  <p>The method can be replicated in other countries because it relies on common road-safety data elements: road-segment geometry, posted speed limit, road class, land use, observed speed statistics, and sample count. Countries with less data can start with posted limits, geometry, road class, and urban/rural context, then add speed observations, crash data, and segment-hour records as available.</p>

  <h2>Submission Links</h2>
  <p><strong>Repository:</strong> https://github.com/tan-amos/adb-ai-for-safer-roads<br>
  <strong>Interactive map:</strong> https://tan-amos.github.io/adb-ai-for-safer-roads/<br>
  <strong>Segment scores:</strong> ADB_DELIVERABLES/outputs/safe_system_segment_scores.csv<br>
  <strong>Methodology:</strong> ADB_DELIVERABLES/SAFE_SYSTEM_METHODOLOGY.md</p>
</body>
</html>
"""
    return html_text


def main() -> None:
    HTML_OUTPUT.write_text(build_html(), encoding="utf-8")
    chrome = chrome_path()
    if not chrome:
        print(f"Wrote {HTML_OUTPUT}")
        print("Chrome/Chromium was not found, so PDF export was skipped.")
        return
    subprocess.run(
        [
            chrome,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--no-pdf-header-footer",
            "--print-to-pdf-no-header",
            f"--print-to-pdf={PDF_OUTPUT}",
            f"file://{HTML_OUTPUT}",
        ],
        check=True,
    )
    print(f"Wrote {HTML_OUTPUT}")
    print(f"Wrote {PDF_OUTPUT}")


if __name__ == "__main__":
    main()
