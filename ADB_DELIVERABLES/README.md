# Safe System Speed Safety Screening

This repository contains a reproducible analytical model for identifying road
segments where posted speed limits and observed speeds may be misaligned with
Safe System principles, especially for vulnerable road users: pedestrians,
cyclists, and powered two-wheeler users.

The method is transparent by design. Each segment receives a 0-100 Speed Safety
Score built from posted speed, observed operating speed, exposure proxy, land-use
context, road class, geometry, and data-quality flags.

## Inputs

Place these source files in the repository root:

- `ADB_Innovation_Thailand.geojson`
- `ADB_Innovation_Maharashtra.geojson`

The current source files contain aggregate speed statistics by segment. They do
not contain hour-of-day, day/night, crash, pedestrian-count, cyclist-count, or
motorcycle-count fields.

## Setup

The scoring model uses only the Python standard library.

```bash
python3 ADB_DELIVERABLES/score_safe_system_segments.py
```

Optional: install Plotly if you want to regenerate the original narrative
proposal HTML.

```bash
python3 -m pip install -r requirements.txt
python3 ADB_DELIVERABLES/build_adb_interactive_proposal.py
```

## Outputs

Running the scoring script writes:

- `ADB_DELIVERABLES/outputs/safe_system_segment_scores.csv`
- `ADB_DELIVERABLES/outputs/safe_system_priority_segments.geojson`
- `ADB_DELIVERABLES/outputs/safe_system_priority_map.html`
- `ADB_DELIVERABLES/outputs/safe_system_scoring_summary.md`

Open `safe_system_priority_map.html` in a browser to inspect the highest-scoring
segments. The deployed GitHub Pages map is:

```text
https://tan-amos.github.io/adb-ai-for-safer-roads/
```

## Score Interpretation

| Score | Class | Meaning |
| ---: | --- | --- |
| 0-24 | Lower priority | No strong speed-safety signal in the available data. |
| 25-49 | Monitor / validate | Some concern; combine with crash and local exposure data. |
| 50-74 | High priority | Strong candidate for speed-limit review, enforcement, or design review. |
| 75-100 | Critical review | Highest-priority segment for agency validation and intervention planning. |

The score is not a crash prediction model. It is a screening model for deciding
where a transport agency should investigate first.

## Key Files

- `score_safe_system_segments.py`: reproducible segment scoring and map builder.
- `SAFE_SYSTEM_METHODOLOGY.md`: score formula, assumptions, and evaluation plan.
- `ADB_road_speed_policy_proposal.md`: policy narrative for Thailand and
  Maharashtra.
- `ADB_road_speed_policy_proposal_interactive.html`: existing interactive
  proposal report.

## Competition Positioning

This submission goes beyond a static speed-limit audit by separating four
decision questions:

1. Are posted limits aligned with Safe System speed principles?
2. Are actual operating speeds above posted limits?
3. Is the segment important enough, based on sample exposure, to prioritize?
4. Is the road context likely to elevate risk for vulnerable users?

The recommended next data upgrade is time-of-day scoring. The supplied files do
not include day/night speed observations, but the methodology document specifies
how to add them when hourly probe-speed records are available.
