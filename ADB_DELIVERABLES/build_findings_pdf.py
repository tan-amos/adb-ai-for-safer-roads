#!/usr/bin/env python3
"""Build an attachment-ready PDF findings summary with static charts."""

from __future__ import annotations

import csv
import html
import shutil
import subprocess
from collections import Counter, defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUTPUT_DIR = HERE / "outputs"
SCORES_CSV = OUTPUT_DIR / "safe_system_segment_scores.csv"
TIME_CSV = OUTPUT_DIR / "time_based_speed_management_candidates.csv"
HTML_OUTPUT = OUTPUT_DIR / "SaiFE_findings_summary.html"
PDF_OUTPUT = OUTPUT_DIR / "SaiFE_findings_summary.pdf"


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


def fmt_int(value: float) -> str:
    return f"{int(round(value)):,}"


def grouped_bar_chart(data: dict[str, dict[str, int]], title: str) -> str:
    countries = list(data)
    width, height = 860, 360
    margin_l, margin_r, margin_t, margin_b = 80, 30, 54, 70
    plot_w = width - margin_l - margin_r
    plot_h = height - margin_t - margin_b
    max_v = max(max(country_data.values()) for country_data in data.values()) or 1
    group_w = plot_w / len(countries)
    bar_w = group_w / (len(PRIORITY_ORDER) + 1)
    parts = [
        f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{html.escape(title)}">',
        f'<text x="{margin_l}" y="28" class="chart-title">{html.escape(title)}</text>',
        f'<line x1="{margin_l}" y1="{margin_t + plot_h}" x2="{width - margin_r}" y2="{margin_t + plot_h}" stroke="#94a3b8"/>',
        f'<line x1="{margin_l}" y1="{margin_t}" x2="{margin_l}" y2="{margin_t + plot_h}" stroke="#94a3b8"/>',
    ]
    for tick in range(5):
        value = max_v * tick / 4
        y = margin_t + plot_h - (value / max_v) * plot_h
        parts.append(f'<line x1="{margin_l}" y1="{y:.1f}" x2="{width - margin_r}" y2="{y:.1f}" stroke="#e2e8f0"/>')
        parts.append(f'<text x="{margin_l - 8}" y="{y + 4:.1f}" text-anchor="end" class="axis">{fmt_int(value)}</text>')

    for i, country in enumerate(countries):
        x0 = margin_l + i * group_w + bar_w * 0.5
        for j, label in enumerate(PRIORITY_ORDER):
            value = data[country].get(label, 0)
            bar_h = (value / max_v) * plot_h
            x = x0 + j * bar_w
            y = margin_t + plot_h - bar_h
            parts.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w * 0.78:.1f}" height="{bar_h:.1f}" '
                f'fill="{PRIORITY_COLORS[label]}"><title>{html.escape(country)} {html.escape(label)}: {value:,}</title></rect>'
            )
        parts.append(
            f'<text x="{margin_l + i * group_w + group_w / 2:.1f}" y="{height - 28}" '
            f'text-anchor="middle" class="axis-label">{html.escape(country)}</text>'
        )

    legend_x = margin_l
    for label in PRIORITY_ORDER:
        parts.append(f'<rect x="{legend_x}" y="{height - 18}" width="11" height="11" fill="{PRIORITY_COLORS[label]}"/>')
        parts.append(f'<text x="{legend_x + 16}" y="{height - 8}" class="legend">{html.escape(label)}</text>')
        legend_x += 155
    parts.append("</svg>")
    return "\n".join(parts)


def horizontal_bar_chart(items: list[tuple[str, float]], title: str, color: str = "#2563eb", suffix: str = "") -> str:
    width, row_h = 860, 30
    margin_l, margin_r, margin_t, margin_b = 260, 56, 52, 32
    height = margin_t + margin_b + row_h * len(items)
    max_v = max((v for _, v in items), default=1) or 1
    plot_w = width - margin_l - margin_r
    parts = [
        f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{html.escape(title)}">',
        f'<text x="0" y="28" class="chart-title">{html.escape(title)}</text>',
    ]
    for i, (label, value) in enumerate(items):
        y = margin_t + i * row_h
        bar_w = (value / max_v) * plot_w
        parts.append(f'<text x="{margin_l - 10}" y="{y + 17}" text-anchor="end" class="axis-label">{html.escape(label[:42])}</text>')
        parts.append(f'<rect x="{margin_l}" y="{y}" width="{bar_w:.1f}" height="20" fill="{color}"/>')
        parts.append(f'<text x="{margin_l + bar_w + 8:.1f}" y="{y + 15}" class="axis">{value:,.0f}{suffix}</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def score_histogram(rows: list[dict[str, str]]) -> str:
    bins = [(0, 24), (25, 49), (50, 74), (75, 100)]
    counts = Counter()
    for row in rows:
        score = fnum(row["speed_safety_score"])
        for lo, hi in bins:
            if lo <= score <= hi:
                counts[f"{lo}-{hi}"] += 1
                break
    return horizontal_bar_chart(list(counts.items()), "Segments by Speed Safety Score band", "#0891b2")


def table(rows: list[dict[str, str]], columns: list[tuple[str, str]]) -> str:
    head = "".join(f"<th>{html.escape(label)}</th>" for _, label in columns)
    body_rows = []
    for row in rows:
        cells = "".join(f"<td>{html.escape(str(row.get(key, '')))}</td>" for key, _ in columns)
        body_rows.append(f"<tr>{cells}</tr>")
    return f"<table><thead><tr>{head}</tr></thead><tbody>{''.join(body_rows)}</tbody></table>"


def build_html() -> str:
    rows = read_rows(SCORES_CSV)
    time_rows = read_rows(TIME_CSV) if TIME_CSV.exists() else []

    by_country_priority: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for row in rows:
        by_country_priority[row["country"]][row["priority_class"]] += 1

    action_counts = Counter(row["recommended_action"] for row in rows if fnum(row["speed_safety_score"]) >= 50)
    top_actions = action_counts.most_common(8)

    top_segments = rows[:12]
    top_time = time_rows[:8]

    high_plus = sum(1 for row in rows if fnum(row["speed_safety_score"]) >= 50)
    critical = sum(1 for row in rows if row["priority_class"] == "Critical review")

    charts = [
        grouped_bar_chart(dict(by_country_priority), "Priority classes by country"),
        score_histogram(rows),
        horizontal_bar_chart(top_actions, "Recommended action categories for priority segments", "#7c3aed"),
        horizontal_bar_chart(
            [(f"{r['country']} - {r['road_name'][:32] or 'Unnamed road'}", fnum(r["speed_safety_score"])) for r in top_segments[:10]],
            "Top scored segments",
            "#dc2626",
        ),
    ]

    if top_time:
        time_counts = Counter(row["time_pilot_type"] for row in time_rows)
        charts.append(horizontal_bar_chart(time_counts.most_common(8), "Time-based pilot candidate types", "#0f766e"))

    html_text = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>SaiFE Findings Summary</title>
  <style>
    @page {{ size: A4; margin: 16mm; }}
    body {{ font-family: Arial, sans-serif; color: #172033; line-height: 1.42; }}
    h1 {{ font-size: 25px; margin: 0 0 4px; }}
    h2 {{ font-size: 17px; margin: 22px 0 8px; border-bottom: 1px solid #d1d5db; padding-bottom: 4px; }}
    h3 {{ font-size: 14px; margin: 14px 0 6px; }}
    p, li {{ font-size: 11px; }}
    .subtitle {{ color: #475569; margin-top: 0; }}
    .metric-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin: 14px 0; }}
    .metric {{ border: 1px solid #cbd5e1; padding: 9px; border-radius: 4px; }}
    .metric strong {{ display: block; font-size: 19px; }}
    .metric span {{ font-size: 10px; color: #475569; }}
    svg {{ width: 100%; height: auto; margin: 6px 0 12px; }}
    .chart-title {{ font-weight: 700; font-size: 16px; fill: #172033; }}
    .axis, .legend {{ font-size: 11px; fill: #475569; }}
    .axis-label {{ font-size: 11px; fill: #172033; }}
    table {{ border-collapse: collapse; width: 100%; margin: 8px 0 12px; font-size: 9.5px; }}
    th, td {{ border: 1px solid #cbd5e1; padding: 4px 5px; vertical-align: top; }}
    th {{ background: #f1f5f9; text-align: left; }}
    .page-break {{ break-before: page; }}
    .note {{ background: #f8fafc; border-left: 4px solid #64748b; padding: 8px 10px; }}
  </style>
</head>
<body>
  <h1>SaiFE Findings Summary</h1>
  <p class="subtitle">Safe AI Framework for Speed-Limit Evaluation</p>

  <div class="metric-grid">
    <div class="metric"><strong>{len(rows):,}</strong><span>usable segments scored</span></div>
    <div class="metric"><strong>{high_plus:,}</strong><span>priority segments scoring 50+</span></div>
    <div class="metric"><strong>{critical:,}</strong><span>critical-review segments</span></div>
    <div class="metric"><strong>{len(time_rows):,}</strong><span>time-based pilot candidates</span></div>
  </div>

  <h2>What Problem SaiFE Solves</h2>
  <p>SaiFE helps transport agencies identify road segments where posted speed limits, actual operating speeds, road context, and geometry may create elevated safety concerns, especially for pedestrians, cyclists, and powered two-wheeler users. It is a transparent screening tool for deciding where governments should investigate first.</p>

  <h2>Method in Brief</h2>
  <p>The model uses the supplied Thailand and Maharashtra GeoJSON datasets. Each valid segment receives a 0-100 Speed Safety Score from six components: posted limit alignment, operating speed behavior, exposure proxy, vulnerable-user context, geometry, and data-quality review. Segments scoring 50 or above are treated as priority speed-unsafe segments for review.</p>

  <h2>Core Findings</h2>
  <p>Thailand produced 131 Critical-review segments and 6,114 High-priority segments. Maharashtra produced 484 High-priority segments. The strongest signals occur where high observed speeds combine with urban or major-road context, geometry concerns, and exposure proxies.</p>

  {charts[0]}
  {charts[1]}

  <div class="page-break"></div>
  <h2>Policy-Relevant Outputs</h2>
  <p>SaiFE does not only rank locations. It assigns action categories that a ministry can use for speed-limit review, road-design review, corridor speed management, enforcement planning, QA, or monitoring.</p>
  {charts[2]}
  {charts[3]}

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
  <h2>Time-Based Speed Management</h2>
  <p>The provided GeoJSON files do not contain timestamp, hour, or day/night fields, so SaiFE does not claim to prove day/night speeding patterns. Instead, it identifies where segment-hour data should be collected first for variable speed limits, night enforcement, school-zone windows, or dynamic speed-management pilots.</p>
  {charts[4] if len(charts) > 4 else ""}

  <h3>First-Wave Time-Based Pilot Candidates</h3>
  {table(top_time, [
      ("country", "Country"),
      ("road_name", "Road"),
      ("road_class", "Class"),
      ("speed_safety_score", "Score"),
      ("time_pilot_type", "Pilot type"),
      ("time_pilot_selection_score", "Pilot score"),
  ]) if top_time else "<p>No time-based candidate output found.</p>"}

  <h2>How a Ministry Could Use This</h2>
  <ul>
    <li>Prioritize corridors for speed-limit review and Safe System alignment checks.</li>
    <li>Select locations for average-speed enforcement, fixed cameras, or speed feedback signs.</li>
    <li>Identify curved or high-speed roads where engineering treatment may be needed.</li>
    <li>Target field validation and speed-limit inventory QA.</li>
    <li>Choose first-wave corridors for segment-hour day/night speed analysis.</li>
  </ul>

  <h2>Validation and Limitations</h2>
  <p class="note">SaiFE is a screening and prioritization model, not a final crash-prediction model. The supplied data does not include crash outcomes, traffic volumes, vulnerable-user exposure, or time-of-day speed records. Final investment decisions should join the score with crash data, traffic counts, field audits, and local engineering review.</p>

  <h2>Replication</h2>
  <p>The method can be replicated in other countries using common road data: segment geometry, posted speed limit, road class, land use, observed speed statistics, and sample count. Countries with less data can start with posted limits, geometry, road class, and urban/rural context, then add speed observations and crash data as they become available.</p>

  <p><strong>Repository:</strong> https://github.com/tan-amos/adb-ai-for-safer-roads<br>
  <strong>Interactive map:</strong> https://tan-amos.github.io/adb-ai-for-safer-roads/</p>
</body>
</html>
"""
    return html_text


def chrome_path() -> str | None:
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return candidate
    return shutil.which("google-chrome") or shutil.which("chromium")


def main() -> None:
    html_text = build_html()
    HTML_OUTPUT.write_text(html_text, encoding="utf-8")
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
