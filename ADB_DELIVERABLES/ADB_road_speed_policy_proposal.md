# Proposal: Data-Driven Road Speed Management Screening for Thailand and Maharashtra

Prepared from analysis of:

- `ADB_Innovation_Thailand.geojson`
- `ADB_Innovation_Maharashtra.geojson`

## Executive Summary

This proposal recommends that the Asian Development Bank support a data-driven road speed management screening program using observed speed behavior, road class, posted speed limits, road geometry, and exposure proxies.

The analysis found that the same technical screening method can be applied across Thailand and Maharashtra, but the policy interpretation must differ by geography.

Thailand presents a regional exposure-versus-compliance problem. Central/Bangkok/East/West has the largest observed speed sample exposure and better average compliance, while North, Northeast, and South show weaker speed compliance, especially on trunk roads.

Maharashtra presents a road-class, land-use, and speed-limit credibility problem. The dominant speed limit is much lower than Thailand's, and the strongest concern is not regional clustering but trunk-road and motorway operating speeds exceeding posted limits.

The proposed next phase is not to immediately raise or lower speed limits. It is to identify corridors for field validation, crash-data matching, enforcement planning, speed-limit credibility review, and road-design intervention.

## Dataset Scope

| Dataset | Total features | Valid speed rows | Usable rows | Action candidates | Dominant speed limit | Avg % over limit | Avg F85 gap | Trunk % over | Trunk F85 gap |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Thailand | 55,884 | 11,544 | 11,134 | 4,907 | 90 km/h | 22.6% | -2.4 km/h | 41.9% | +11.2 km/h |
| Maharashtra | 14,082 | 4,010 | 3,577 | 500 | 55 km/h | 27.8% | +3.6 km/h | 43.3% | +16.9 km/h |

Definitions:

- Valid speed rows are records marked valid for speed analysis.
- Usable rows are valid rows with speed limit, geometry, and supported road class.
- Action candidates are road segments that meet conservative screening rules for field review.
- F85 gap is `F85th percentile speed - posted speed limit`.
- `SampleSizeTotal` and `Sample_Size_Total` are observed speed sample counts, not traffic volume or crash counts.

## What We Found

### 1. The Screening Formula Transfers, But the Policy Story Does Not

The same action-audit logic can be applied to both datasets:

| Action bucket | Screening rule | Policy meaning |
| --- | --- | --- |
| Investigate possible increase / QA | Speed limit <= 60 km/h, median speed at least 15 km/h above limit, F85 at least 25 km/h above limit, at least 60% over limit, and sufficient sample size | Could indicate miscoded speed limit, map-matching issue, special local context, unrealistic low limit, or severe noncompliance. Not an automatic increase. |
| Investigate possible decrease | Speed limit >= 80 km/h, curved/highly curved road, F85 at least 5 km/h below limit, low share over the limit, and sufficient sample size | Drivers may already be behaving below the posted limit. Review design speed, roadside risk, and crash history. |
| Enforcement / speed management | Motorway, trunk, or primary road with at least 35% over the limit and F85 at least 5 km/h above limit | Operating speeds exceed the posted limit. Consider enforcement, average-speed cameras, gateway treatments, and corridor speed management. |
| Road design change | Curved/highly curved road with high operating speeds | Signs alone may not be enough. Review curve treatment, shoulder, delineation, access, roadside hazards, and self-explaining design. |

However, the outputs point to different programs:

- Thailand should be managed through regional corridor programs.
- Maharashtra should be managed through road-class, land-use, and speed-limit credibility audits.

### 2. Thailand: Regional Exposure and Trunk-Road Compliance Are the Main Story

Thailand has 4,907 candidate segments under the action audit.

| Action bucket | Candidate segments |
| --- | ---: |
| Enforcement / speed management | 1,870 |
| Investigate possible decrease | 1,808 |
| Road design change | 980 |
| Investigate possible increase / QA | 249 |

Regional speed-compliance pattern:

| Region | Avg % over limit | Sample-weighted % over | Valid rows | Sample total |
| --- | ---: | ---: | ---: | ---: |
| Northeast | 24.3% | 32.8% | 2,844 | 967,714,524 |
| South | 23.2% | 30.7% | 1,919 | 661,509,722 |
| North | 22.4% | 33.1% | 2,668 | 889,805,565 |
| Central/Bangkok/East/West | 19.0% | 25.9% | 4,112 | 6,282,654,155 |

Key interpretation:

- Central/Bangkok/East/West is not the worst for average speed noncompliance, but it has by far the largest observed speed sample exposure.
- North, Northeast, and South show weaker compliance.
- Trunk roads are the clearest national speed-management class.

Thailand trunk-road pattern:

| Region | Trunk avg % over limit | Trunk sample-weighted % over |
| --- | ---: | ---: |
| North | 46.6% | 49.6% |
| South | 45.1% | 42.6% |
| Central/Bangkok/East/West | 35.9% | 34.4% |
| Northeast | 35.5% | 40.4% |

Thailand policy implication:

- Central/Bangkok/East/West should be treated as a high-exposure corridor validation track.
- North and South trunk corridors should be treated as priority speed-compliance tracks.
- Northeast should be treated as a broader trunk-and-primary speed management track.
- Extreme low-speed-limit cases, including 30 km/h rows with very high observed speeds, should be treated as QA and field-review candidates before any policy conclusion.

### 3. Maharashtra: Road Class, Land Use, and Speed-Limit Credibility Are the Main Story

Maharashtra has 500 candidate segments under the same action audit.

| Action bucket | Candidate segments |
| --- | ---: |
| Enforcement / speed management | 368 |
| Investigate possible increase / QA | 93 |
| Investigate possible decrease | 20 |
| Road design change | 19 |

By road class:

| Road class | Action bucket | Candidate segments |
| --- | --- | ---: |
| trunk | Enforcement / speed management | 260 |
| trunk | Investigate possible increase / QA | 84 |
| trunk | Road design change | 18 |
| trunk | Investigate possible decrease | 13 |
| primary | Enforcement / speed management | 91 |
| motorway | Enforcement / speed management | 17 |

By land use:

| Land use | Enforcement / speed management | Possible increase / QA | Possible decrease | Road design change |
| --- | ---: | ---: | ---: | ---: |
| RURAL | 246 | 82 | 7 | 18 |
| URBAN | 122 | 11 | 13 | 1 |

Key interpretation:

- The dominant candidate type is enforcement / speed management.
- Trunk roads are the largest concern, with 260 enforcement / speed-management candidates and 84 possible increase / QA candidates.
- Maharashtra's dominant speed limit is 55 km/h, so it should not be interpreted using the same assumptions as Thailand's 80-90 km/h road environment.
- Low posted limits with high observed speeds require credibility review, QA, and field validation before any recommendation to raise limits.

Maharashtra policy implication:

- Prioritize trunk-road speed management.
- Separate rural and urban reviews because the same operating speed can mean different safety problems in different land-use contexts.
- Audit whether some posted limits are credible, miscoded, locally justified, or undermined by road design.
- Avoid copying Thailand's regional-clustering approach unless additional administrative or crash data supports it.

## Proposed ADB Program

### Objective

Develop a replicable road-speed screening and intervention framework that helps governments identify where to investigate:

- speed enforcement,
- speed-limit increases or QA issues,
- speed-limit decreases,
- road-design changes,
- corridor-level safety investments.

### Phase 1: Data Validation and Corridor Screening

1. Confirm data definitions and metadata with source providers.
2. Validate speed-limit fields against official road authority inventories.
3. Check map matching and geometry quality for extreme outliers.
4. Produce candidate corridor lists by road class, action bucket, region or land use.
5. Select pilot corridors for field validation.

Expected output:

- validated candidate corridor list,
- QA log for suspicious speed-limit records,
- priority corridor maps,
- dashboard for agency review.

### Phase 2: Crash and Exposure Integration

Join speed-screening outputs with:

- fatal crashes,
- serious injuries,
- motorcycle exposure,
- pedestrian exposure,
- traffic volume,
- access density,
- junction density,
- land use,
- roadside hazards,
- enforcement history.

Expected output:

- investment-priority corridors,
- high-confidence enforcement corridors,
- speed-limit review corridors,
- road-design intervention corridors.

### Phase 3: Pilot Interventions

Recommended pilot packages:

| Pilot type | Where it fits | Example interventions |
| --- | --- | --- |
| Enforcement / speed management | Major roads with high F85 gap and high percent over limit | average-speed enforcement, fixed cameras, corridor enforcement, variable messaging |
| Speed-limit credibility review | Low limits with very high observed speeds | speed-limit inventory check, field review, local context validation, public communication |
| Speed-limit decrease review | High-limit curved roads where drivers already operate below limit | design-speed audit, sign review, roadside-risk review, possible posted-limit reduction |
| Road-design change | Curved/highly curved roads with high operating speeds | curve warning, delineation, shoulder treatment, rumble strips, access management, traffic calming |

### Phase 4: Monitoring and Evaluation

Measure before and after:

- F85 speed,
- median speed,
- percent over limit,
- crash frequency,
- fatal and serious injury crashes,
- motorcycle crashes,
- speed variance,
- public compliance,
- enforcement sustainability.

## Recommended Immediate Priorities

### Thailand

1. Build a high-exposure Central/Bangkok/East/West validation program.
2. Start trunk-road speed-management reviews in North and South.
3. Treat Northeast as a broader trunk-and-primary compliance program.
4. Field-check 30 km/h and other very low-limit rows with high observed speeds.
5. Use crash and motorcycle fatality data before final investment ranking.

### Maharashtra

1. Prioritize trunk-road enforcement and speed-management screening.
2. Separate rural and urban candidate interpretation.
3. Audit low posted speed limits where median and F85 speeds are far above the limit.
4. Review motorway and trunk segments where high operating speeds suggest corridor-level enforcement needs.
5. Add crash, traffic-volume, and land-use data before recommending speed-limit changes.

## Important Limitations

This analysis should not be presented as a final crash-risk ranking.

The GeoJSON files contain road-segment speed, geometry, road-class, and sample-count information. They do not contain the full set of variables needed for final safety investment decisions.

Before implementation, ADB and government counterparts should require:

- official crash and fatality records,
- serious-injury records,
- motorcycle and pedestrian exposure,
- traffic volumes,
- official posted speed-limit inventories,
- road authority classification,
- field inspection,
- engineering design-speed review,
- local context and land-use verification.

## Proposal Recommendation

ADB should support a two-country pilot that uses a shared road-speed screening method but allows each geography to produce its own policy pathway.

The practical value is not a universal score. The value is a repeatable decision workflow:

1. identify credible candidate corridors,
2. classify the type of review needed,
3. validate with crash and field data,
4. select enforcement, speed-limit review, or engineering interventions,
5. monitor before-and-after outcomes.

This gives ADB a defensible, scalable method for turning probe-speed and road-network data into targeted road-safety action while avoiding unsupported claims that a segment is dangerous based on speed data alone.

## Supporting Files

- Public-repository setup guide: `README.md`
- Segment-level Safe System scoring script: `score_safe_system_segments.py`
- Score formula and evaluation methodology: `SAFE_SYSTEM_METHODOLOGY.md`
- Segment-level scoring output: `outputs/safe_system_segment_scores.csv`
- Priority segment GeoJSON: `outputs/safe_system_priority_segments.geojson`
- Interactive priority map: `outputs/safe_system_priority_map.html`
- Thailand main storytelling report: `risk_diagnosis_v1/curve_speed_limit_regional_policy_story.html`
- Maharashtra audit report: `maharashtra_speed_limit_audit/maharashtra_speed_limit_action_audit_v2.html`
- Shared baseline comparison: `thailand_maharashtra_shared_baseline_comparison.html`
- Shared baseline markdown: `thailand_maharashtra_shared_baseline_comparison.md`
- Thailand project handoff: `risk_diagnosis_v1/project_accomplishments_and_policy_handoff.md`
