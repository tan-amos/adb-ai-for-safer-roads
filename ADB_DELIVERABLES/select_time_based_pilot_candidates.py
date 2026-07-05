#!/usr/bin/env python3
"""Select candidates for future time-of-day or dynamic speed management pilots.

This script does not calculate day/night speeding because the source GeoJSON
files do not contain time fields. It uses the existing Speed Safety Score output
to identify where time-of-day probe-speed data would be most valuable.
"""

from __future__ import annotations

import csv
from pathlib import Path


HERE = Path(__file__).resolve().parent
INPUT = HERE / "outputs" / "safe_system_segment_scores.csv"
OUTPUT = HERE / "outputs" / "time_based_speed_management_candidates.csv"


def as_float(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def pilot_type(row: dict[str, str]) -> str:
    land_use = row["land_use"].upper()
    road_class = row["road_class"]
    f85_gap = as_float(row["f85_gap"])
    percent_over = as_float(row["percent_over"])
    geometry_points = as_float(row["geometry_points"])

    if land_use == "URBAN" and road_class in {"trunk", "primary"}:
        return "Urban time-window speed management"
    if geometry_points >= 7 and f85_gap >= 15:
        return "Night/low-visibility curve speed management"
    if percent_over >= 0.60 and f85_gap >= 20:
        return "Night enforcement or average-speed pilot"
    if road_class == "motorway":
        return "Variable speed limit feasibility review"
    return "Segment-hour data collection priority"


def selection_score(row: dict[str, str]) -> float:
    return (
        as_float(row["speed_safety_score"]) * 1.0
        + min(15.0, max(0.0, as_float(row["f85_gap"])) / 2.0)
        + min(10.0, as_float(row["percent_over"]) * 10.0)
        + min(5.0, as_float(row["sample_total"]) / 2_000_000.0)
    )


def main() -> None:
    with INPUT.open("r", encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))

    candidates = []
    for row in rows:
        score = as_float(row["speed_safety_score"])
        if score < 60:
            continue
        row = dict(row)
        row["time_pilot_type"] = pilot_type(row)
        row["time_pilot_selection_score"] = round(selection_score(row), 2)
        row["required_next_data"] = (
            "segment-hour median speed, F85 speed, percent over limit, sample count, "
            "day/night flag, crash records, and vulnerable-user exposure"
        )
        candidates.append(row)

    candidates.sort(key=lambda r: as_float(r["time_pilot_selection_score"]), reverse=True)
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
        "f85_gap",
        "sample_total",
        "speed_safety_score",
        "priority_class",
        "recommended_action",
        "time_pilot_type",
        "time_pilot_selection_score",
        "required_next_data",
    ]
    with OUTPUT.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(candidates[:250])

    print(f"Wrote {OUTPUT}")
    print(f"Candidate segments: {min(len(candidates), 250):,}")


if __name__ == "__main__":
    main()
