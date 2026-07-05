# AI for Safer Roads: Safe System Speed Safety Screening

This repository contains a reproducible analytical model for identifying road
segments where posted speed limits and observed speeds may be misaligned with
Safe System principles, especially for vulnerable road users: pedestrians,
cyclists, and powered two-wheeler users.

The core output is a transparent 0-100 **Speed Safety Score** for each usable
road segment in the supplied Thailand and Maharashtra GeoJSON datasets.

## Competition Deliverables

| Requirement | File |
| --- | --- |
| Analytical mode: documented code and methodology | `ADB_DELIVERABLES/score_safe_system_segments.py`, `ADB_DELIVERABLES/SAFE_SYSTEM_METHODOLOGY.md` |
| Clear setup and run instructions | `README.md`, `ADB_DELIVERABLES/README.md` |
| Speed Safety Score for each segment | `ADB_DELIVERABLES/outputs/safe_system_segment_scores.csv` |
| Transparent score calculation | `ADB_DELIVERABLES/SAFE_SYSTEM_METHODOLOGY.md` |
| Findings summary | `ADB_DELIVERABLES/FINDINGS_SUMMARY.md` |
| Geospatial visualization | `ADB_DELIVERABLES/outputs/safe_system_priority_map.html` |
| Priority segment GeoJSON | `ADB_DELIVERABLES/outputs/safe_system_priority_segments.geojson` |
| Rubric alignment | `ADB_DELIVERABLES/RUBRIC_ALIGNMENT.md` |
| Time-based speed management candidates | `ADB_DELIVERABLES/outputs/time_based_speed_management_candidates.csv` |

## Run the Model

The scoring pipeline uses only the Python standard library.

```bash
python3 ADB_DELIVERABLES/score_safe_system_segments.py
```

Expected outputs:

- `ADB_DELIVERABLES/outputs/safe_system_segment_scores.csv`
- `ADB_DELIVERABLES/outputs/safe_system_priority_segments.geojson`
- `ADB_DELIVERABLES/outputs/safe_system_priority_map.html`
- `ADB_DELIVERABLES/outputs/safe_system_scoring_summary.md`

## Score Meaning

| Score | Class | Meaning |
| ---: | --- | --- |
| 0-24 | Lower priority | No strong speed-safety signal in the available data. |
| 25-49 | Monitor / validate | Some concern; combine with crash and local exposure data. |
| 50-74 | High priority | Strong candidate for speed-limit review, enforcement, or design review. |
| 75-100 | Critical review | Highest-priority segment for agency validation and intervention planning. |

The score is a screening tool, not a final crash-risk prediction. Final
investment decisions should join crash, fatality, traffic-volume, pedestrian,
cyclist, motorcycle, enforcement, and field-audit data.

## Interactive Map

Public map URL:

```text
https://tan-amos.github.io/adb-ai-for-safer-roads/
```

Repository file:

```text
ADB_DELIVERABLES/outputs/safe_system_priority_map.html
```

The public map is served from the lightweight `docs/` folder so GitHub Pages can
publish quickly while the full analytical data and outputs remain in the
repository.

## Time-Based and AI-Assisted Speed Management

The supplied GeoJSON files contain aggregate speed summaries, but no hour,
timestamp, day/night, weather, or lighting fields. The methodology therefore
documents time-of-day scoring as an extension rather than making unsupported
claims from unavailable data.

The repo includes a full temporal data audit:

```text
ADB_DELIVERABLES/TEMPORAL_DATA_AUDIT.md
```

It also includes a current-data candidate list for where time-based or dynamic
speed-management pilots should be tested first:

```bash
python3 ADB_DELIVERABLES/select_time_based_pilot_candidates.py
```

Output:

```text
ADB_DELIVERABLES/outputs/time_based_speed_management_candidates.csv
```

The recommended next data step is to add segment-hour speed profiles and
calculate daytime versus night-time F85 speed, percent-over-limit, and speeding
deltas. Those features can support AI-assisted decision support for variable
speed limits, targeted enforcement, school-zone windows, and night-time
motorcycle safety programs.
