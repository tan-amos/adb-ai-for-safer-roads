# SaiFE Submission Index

Use this page as the main navigation guide for the submission.

## Primary Links

| Item | Link / file |
| --- | --- |
| Public repository | https://github.com/tan-amos/adb-ai-for-safer-roads |
| Interactive map | https://tan-amos.github.io/adb-ai-for-safer-roads/ |
| Full deliverables PDF | `ADB_DELIVERABLES/outputs/SaiFE_full_deliverables_summary.pdf` |
| Findings PDF, max 5 pages | `ADB_DELIVERABLES/outputs/SaiFE_findings_summary.pdf` |
| Findings summary markdown | `ADB_DELIVERABLES/FINDINGS_SUMMARY.md` |
| Methodology | `ADB_DELIVERABLES/SAFE_SYSTEM_METHODOLOGY.md` |
| Rubric alignment | `ADB_DELIVERABLES/RUBRIC_ALIGNMENT.md` |
| Temporal data audit | `ADB_DELIVERABLES/TEMPORAL_DATA_AUDIT.md` |

## Required Deliverables

### 1. Analytical Mode

Use:

- `ADB_DELIVERABLES/score_safe_system_segments.py`
- `ADB_DELIVERABLES/SAFE_SYSTEM_METHODOLOGY.md`
- `README.md`

These files document the code, setup, methodology, score calculation, validation
approach, assumptions, and limitations.

### 2. Speed Safety Score

Use:

- `ADB_DELIVERABLES/outputs/safe_system_segment_scores.csv`

Key columns:

- `speed_safety_score`
- `priority_class`
- `recommended_action`
- `confidence`
- `limit_alignment_points`
- `operating_speed_points`
- `exposure_points`
- `vulnerable_context_points`
- `geometry_points`
- `qa_points`

### 3. Geospatial Visualization

Use:

- Public map: https://tan-amos.github.io/adb-ai-for-safer-roads/
- Source HTML: `ADB_DELIVERABLES/outputs/safe_system_priority_map.html`
- Priority GeoJSON: `ADB_DELIVERABLES/outputs/safe_system_priority_segments.geojson`

## Attachment Recommendations

If the submission form allows only one PDF attachment, attach:

```text
ADB_DELIVERABLES/outputs/SaiFE_full_deliverables_summary.pdf
```

If the form specifically asks for a findings summary with a maximum of 5 pages,
attach:

```text
ADB_DELIVERABLES/outputs/SaiFE_findings_summary.pdf
```

Both PDFs are currently 4 pages.

## Reproducibility Commands

Run the core scoring model:

```bash
python3 ADB_DELIVERABLES/score_safe_system_segments.py
```

Build time-based speed-management candidates:

```bash
python3 ADB_DELIVERABLES/select_time_based_pilot_candidates.py
```

Build the PDF summaries:

```bash
python3 ADB_DELIVERABLES/build_findings_pdf.py
python3 ADB_DELIVERABLES/build_full_deliverables_pdf.py
```

## Submission Description

SaiFE is a transparent Safe System screening engine for speed-limit evaluation.
It scores each usable road segment from 0 to 100 using posted speed, observed
operating speed, exposure proxy, road class, land use, geometry, and data-quality
flags. The outputs identify priority segments for speed-limit review,
enforcement, road-design review, field validation, and future time-based speed
management pilots.
