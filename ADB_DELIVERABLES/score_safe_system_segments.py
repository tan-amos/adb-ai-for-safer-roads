#!/usr/bin/env python3
"""Create transparent Safe System speed-safety scores for each road segment.

The model is intentionally rule-based. A transport official should be able to
recalculate every score from the source fields without needing a black-box
model. The script produces:

- `outputs/safe_system_segment_scores.csv`
- `outputs/safe_system_priority_segments.geojson`
- `outputs/safe_system_priority_map.html`
"""

from __future__ import annotations

import csv
import html
import json
import math
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUTPUT_DIR = HERE / "outputs"

DATASETS = [
    {
        "country": "Thailand",
        "path": ROOT / "ADB_Innovation_Thailand.geojson",
        "sample_field": "SampleSizeTotal",
        "road_name_field": "english_ro",
    },
    {
        "country": "Maharashtra",
        "path": ROOT / "ADB_Innovation_Maharashtra.geojson",
        "sample_field": "Sample_Size_Total",
        "road_name_field": "names_primary",
    },
]


def as_float(value: Any) -> float | None:
    try:
        if value is None or value == "":
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def haversine_km(a: list[float], b: list[float]) -> float:
    lon1, lat1 = math.radians(a[0]), math.radians(a[1])
    lon2, lat2 = math.radians(b[0]), math.radians(b[1])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 6371.0088 * 2 * math.asin(min(1, math.sqrt(h)))


def bearing_degrees(a: list[float], b: list[float]) -> float:
    lon1, lat1 = math.radians(a[0]), math.radians(a[1])
    lon2, lat2 = math.radians(b[0]), math.radians(b[1])
    dlon = lon2 - lon1
    x = math.sin(dlon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
    return (math.degrees(math.atan2(x, y)) + 360) % 360


def angle_delta(a: float, b: float) -> float:
    delta = abs(a - b) % 360
    return min(delta, 360 - delta)


def geometry_metrics(coords: list[list[float]]) -> dict[str, float]:
    if len(coords) < 2:
        return {"sinuosity": 1.0, "bearing_change_per_km": 0.0}

    lengths = [haversine_km(coords[i], coords[i + 1]) for i in range(len(coords) - 1)]
    line_length = sum(lengths)
    straight_distance = haversine_km(coords[0], coords[-1])
    sinuosity = line_length / straight_distance if straight_distance > 0.02 else 1.0
    bearings = [
        bearing_degrees(coords[i], coords[i + 1])
        for i, length in enumerate(lengths)
        if length > 0.005
    ]
    bearing_change = sum(angle_delta(bearings[i], bearings[i + 1]) for i in range(len(bearings) - 1))
    return {
        "sinuosity": sinuosity,
        "bearing_change_per_km": bearing_change / line_length if line_length else 0.0,
    }


def limit_alignment_points(speed_limit: float, land_use: str, road_class: str) -> int:
    """Points for posted-speed incompatibility with Safe System VRU principles."""
    is_urban = land_use.upper() == "URBAN"
    if is_urban:
        if speed_limit <= 30:
            points = 0
        elif speed_limit <= 50:
            points = 10
        elif speed_limit <= 60:
            points = 20
        else:
            points = 30
    else:
        if speed_limit <= 50:
            points = 5
        elif speed_limit <= 60:
            points = 10
        elif speed_limit <= 80:
            points = 18
        else:
            points = 24

    if road_class in {"motorway", "trunk", "primary"} and speed_limit >= 80:
        points = min(30, points + 4)
    return points


def operating_speed_points(percent_over: float, f85_gap: float, median_gap: float) -> int:
    over_points = 0
    if percent_over >= 0.60:
        over_points = 12
    elif percent_over >= 0.35:
        over_points = 8
    elif percent_over >= 0.15:
        over_points = 4

    gap_points = 0
    if f85_gap >= 25 or median_gap >= 15:
        gap_points = 13
    elif f85_gap >= 15 or median_gap >= 10:
        gap_points = 9
    elif f85_gap >= 5:
        gap_points = 5

    return min(25, over_points + gap_points)


def exposure_points(sample_total: float, road_length_km: float) -> int:
    sample_points = 0
    if sample_total >= 10_000_000:
        sample_points = 12
    elif sample_total >= 1_000_000:
        sample_points = 9
    elif sample_total >= 100_000:
        sample_points = 6
    elif sample_total >= 10_000:
        sample_points = 3

    length_points = 3 if road_length_km >= 10 else 2 if road_length_km >= 3 else 0
    return min(15, sample_points + length_points)


def vulnerable_context_points(land_use: str, road_class: str) -> int:
    points = 8 if land_use.upper() == "URBAN" else 3
    if road_class in {"trunk", "primary"}:
        points += 5
    elif road_class == "secondary":
        points += 4
    elif road_class == "motorway":
        points += 1
    return min(15, points)


def geometry_points(sinuosity: float, bearing_change_per_km: float, f85_speed: float) -> int:
    curvy = sinuosity >= 1.08 or bearing_change_per_km >= 45
    highly_curvy = sinuosity >= 1.15 or bearing_change_per_km >= 90
    if highly_curvy and f85_speed >= 70:
        return 10
    if curvy and f85_speed >= 60:
        return 7
    if curvy:
        return 4
    return 0


def data_quality_points(speed_limit: float, median_gap: float, f85_gap: float, sample_total: float) -> int:
    if sample_total < 10_000:
        return 3
    if speed_limit <= 40 and median_gap >= 40 and f85_gap >= 50:
        return 5
    return 0


def priority_class(score: int) -> str:
    if score >= 75:
        return "Critical review"
    if score >= 50:
        return "High priority"
    if score >= 25:
        return "Monitor / validate"
    return "Lower priority"


def recommended_action(row: dict[str, Any]) -> str:
    if row["qa_points"] >= 5:
        return "Speed-limit inventory QA and field validation"
    if row["geometry_points"] >= 7 and row["operating_speed_points"] >= 9:
        return "Road design and speed management review"
    if row["limit_alignment_points"] >= 20:
        return "Posted speed-limit review against Safe System principles"
    if row["operating_speed_points"] >= 13:
        return "Enforcement or corridor speed management"
    return "Monitor and combine with crash/exposure data"


def confidence(row: dict[str, Any]) -> str:
    if row["sample_total"] >= 100_000 and row["qa_points"] == 0:
        return "High"
    if row["sample_total"] >= 10_000:
        return "Medium"
    return "Low"


def score_feature(dataset: dict[str, Any], feature: dict[str, Any]) -> dict[str, Any] | None:
    p = feature["properties"]
    if p.get("AnalysisStatus") != "Valid":
        return None

    speed_limit = as_float(p.get("SpeedLimit"))
    median_speed = as_float(p.get("MedianSpeed"))
    f85_speed = as_float(p.get("F85thPercentileSpeed"))
    percent_over = as_float(p.get("PercentOverLimit"))
    sample_total = as_float(p.get(dataset["sample_field"])) or 0.0
    road_length = as_float(p.get("RoadLength")) or 0.0
    road_class = p.get("RoadClass") or p.get("class") or "unknown"
    land_use = p.get("LandUse") or "Unknown"
    coords = feature.get("geometry", {}).get("coordinates") or []

    if not coords or speed_limit is None or speed_limit <= 0:
        return None
    if median_speed is None or f85_speed is None or percent_over is None:
        return None
    if road_class not in {"motorway", "trunk", "primary", "secondary"}:
        return None

    geom = geometry_metrics(coords)
    median_gap = median_speed - speed_limit
    f85_gap = f85_speed - speed_limit

    row = {
        "country": dataset["country"],
        "segment_id": p.get("OBJECTID") or p.get("DISSOLVE_ID") or "",
        "road_name": p.get(dataset["road_name_field"]) or "Unnamed road",
        "road_class": road_class,
        "land_use": land_use,
        "speed_limit": speed_limit,
        "median_speed": median_speed,
        "f85_speed": f85_speed,
        "percent_over": percent_over,
        "median_gap": median_gap,
        "f85_gap": f85_gap,
        "sample_total": sample_total,
        "road_length_km": road_length,
        "sinuosity": geom["sinuosity"],
        "bearing_change_per_km": geom["bearing_change_per_km"],
    }
    row["limit_alignment_points"] = limit_alignment_points(speed_limit, land_use, road_class)
    row["operating_speed_points"] = operating_speed_points(percent_over, f85_gap, median_gap)
    row["exposure_points"] = exposure_points(sample_total, road_length)
    row["vulnerable_context_points"] = vulnerable_context_points(land_use, road_class)
    row["geometry_points"] = geometry_points(geom["sinuosity"], geom["bearing_change_per_km"], f85_speed)
    row["qa_points"] = data_quality_points(speed_limit, median_gap, f85_gap, sample_total)
    row["speed_safety_score"] = int(
        row["limit_alignment_points"]
        + row["operating_speed_points"]
        + row["exposure_points"]
        + row["vulnerable_context_points"]
        + row["geometry_points"]
        + row["qa_points"]
    )
    row["priority_class"] = priority_class(row["speed_safety_score"])
    row["recommended_action"] = recommended_action(row)
    row["confidence"] = confidence(row)
    row["geometry"] = feature["geometry"]
    return row


def load_scores() -> list[dict[str, Any]]:
    rows = []
    for dataset in DATASETS:
        with dataset["path"].open("r", encoding="utf-8") as file:
            data = json.load(file)
        for feature in data["features"]:
            row = score_feature(dataset, feature)
            if row:
                rows.append(row)
    return sorted(rows, key=lambda r: r["speed_safety_score"], reverse=True)


def write_csv_output(rows: list[dict[str, Any]]) -> None:
    fields = [
        "country",
        "segment_id",
        "road_name",
        "road_class",
        "land_use",
        "speed_limit",
        "median_speed",
        "f85_speed",
        "percent_over",
        "median_gap",
        "f85_gap",
        "sample_total",
        "road_length_km",
        "sinuosity",
        "bearing_change_per_km",
        "limit_alignment_points",
        "operating_speed_points",
        "exposure_points",
        "vulnerable_context_points",
        "geometry_points",
        "qa_points",
        "speed_safety_score",
        "priority_class",
        "recommended_action",
        "confidence",
    ]
    with (OUTPUT_DIR / "safe_system_segment_scores.csv").open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_geojson_output(rows: list[dict[str, Any]]) -> None:
    features = []
    for row in rows:
        if row["speed_safety_score"] < 50:
            continue
        props = {k: v for k, v in row.items() if k != "geometry"}
        features.append({"type": "Feature", "properties": props, "geometry": row["geometry"]})
    payload = {"type": "FeatureCollection", "features": features}
    (OUTPUT_DIR / "safe_system_priority_segments.geojson").write_text(
        json.dumps(payload, ensure_ascii=False), encoding="utf-8"
    )


def color_for_score(score: int) -> str:
    if score >= 75:
        return "#7f1d1d"
    if score >= 50:
        return "#dc2626"
    if score >= 25:
        return "#f59e0b"
    return "#16a34a"


def write_map_output(rows: list[dict[str, Any]]) -> None:
    map_rows = rows[:750]
    features = []
    for row in map_rows:
        props = {k: v for k, v in row.items() if k != "geometry"}
        props["color"] = color_for_score(row["speed_safety_score"])
        features.append({"type": "Feature", "properties": props, "geometry": row["geometry"]})

    payload = json.dumps({"type": "FeatureCollection", "features": features}, ensure_ascii=False)
    html_text = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Safe System Speed Safety Priority Map</title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
  <style>
    html, body, #map {{ height: 100%; margin: 0; font-family: Arial, sans-serif; }}
    .panel {{
      position: absolute; top: 12px; left: 54px; z-index: 500;
      max-width: 390px; background: white; padding: 12px 14px;
      border: 1px solid #d1d5db; border-radius: 6px; box-shadow: 0 3px 14px #0002;
    }}
    .panel h1 {{ font-size: 17px; margin: 0 0 6px; }}
    .panel p {{ font-size: 13px; margin: 4px 0; line-height: 1.35; }}
    .legend {{ margin-top: 8px; display: grid; gap: 4px; font-size: 12px; }}
    .swatch {{ display: inline-block; width: 14px; height: 4px; margin-right: 6px; vertical-align: middle; }}
  </style>
</head>
<body>
  <div id="map"></div>
  <div class="panel">
    <h1>Speed Safety Score priority map</h1>
    <p>Top 750 scored segments across Thailand and Maharashtra. Higher scores indicate stronger need for speed-limit review, speed management, or field validation.</p>
    <div class="legend">
      <div><span class="swatch" style="background:#7f1d1d"></span>75-100 Critical review</div>
      <div><span class="swatch" style="background:#dc2626"></span>50-74 High priority</div>
      <div><span class="swatch" style="background:#f59e0b"></span>25-49 Monitor / validate</div>
    </div>
  </div>
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <script>
    const data = {payload};
    const map = L.map('map').setView([17.8, 91.5], 5);
    L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
      maxZoom: 18,
      attribution: '&copy; OpenStreetMap contributors'
    }}).addTo(map);
    const layer = L.geoJSON(data, {{
      style: feature => ({{
        color: feature.properties.color,
        weight: Math.max(3, Math.min(8, feature.properties.speed_safety_score / 12)),
        opacity: 0.86
      }}),
      onEachFeature: (feature, layer) => {{
        const p = feature.properties;
        layer.bindPopup(`
          <strong>${{escapeHtml(p.road_name)}}</strong><br>
          ${{escapeHtml(p.country)}} | ${{escapeHtml(p.road_class)}} | ${{escapeHtml(p.land_use)}}<br>
          Score: <strong>${{p.speed_safety_score}}</strong> (${{escapeHtml(p.priority_class)}})<br>
          Limit: ${{p.speed_limit}} km/h; F85: ${{p.f85_speed}} km/h; over limit: ${{(p.percent_over * 100).toFixed(1)}}%<br>
          Action: ${{escapeHtml(p.recommended_action)}}<br>
          Confidence: ${{escapeHtml(p.confidence)}}
        `);
      }}
    }}).addTo(map);
    map.fitBounds(layer.getBounds(), {{padding: [25, 25]}});
    function escapeHtml(value) {{
      return String(value).replace(/[&<>"']/g, c => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}}[c]));
    }}
  </script>
</body>
</html>
"""
    (OUTPUT_DIR / "safe_system_priority_map.html").write_text(html_text, encoding="utf-8")


def write_summary(rows: list[dict[str, Any]]) -> None:
    counts: dict[tuple[str, str], int] = {}
    for row in rows:
        key = (row["country"], row["priority_class"])
        counts[key] = counts.get(key, 0) + 1

    lines = [
        "# Safe System Scoring Run Summary",
        "",
        f"Scored usable segments: {len(rows):,}",
        "",
        "| Country | Priority class | Segments |",
        "| --- | --- | ---: |",
    ]
    for key, count in sorted(counts.items()):
        lines.append(f"| {key[0]} | {key[1]} | {count:,} |")
    lines.extend(
        [
            "",
            "Top 20 priority segments are listed in `safe_system_segment_scores.csv`.",
            "The map file shows the top 750 segments so it remains responsive in a browser.",
        ]
    )
    (OUTPUT_DIR / "safe_system_scoring_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    rows = load_scores()
    write_csv_output(rows)
    write_geojson_output(rows)
    write_map_output(rows)
    write_summary(rows)
    print(f"Scored {len(rows):,} usable segments")
    print(f"Wrote {OUTPUT_DIR / 'safe_system_segment_scores.csv'}")
    print(f"Wrote {OUTPUT_DIR / 'safe_system_priority_map.html'}")


if __name__ == "__main__":
    main()
