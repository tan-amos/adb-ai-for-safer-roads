# Safe System Speed Safety Methodology

## Objective

The model screens road segments for speed-limit review and speed-management
intervention. It asks whether the posted limit and observed operating speed are
consistent with Safe System principles, especially where vulnerable road users
may be exposed.

The output is a segment-level Speed Safety Score from 0 to 100. Higher scores
mean stronger need for agency review, field validation, or intervention.

## Why a Transparent Score

The competition requires a score that is reproducible and interpretable by
non-technical decision makers. For that reason, the primary model is rule-based
rather than a black-box machine-learning model. Every point can be traced to an
input field and a documented threshold.

## Required Fields

The current implementation uses:

- `SpeedLimit`
- `MedianSpeed`
- `F85thPercentileSpeed`
- `PercentOverLimit`
- `SampleSizeTotal` or `Sample_Size_Total`
- `RoadLength`
- `RoadClass`
- `LandUse`
- GeoJSON line geometry

Crash records, pedestrian volumes, cyclist volumes, motorcycle volumes, traffic
volumes, and time-of-day speed records are not present in the supplied GeoJSON.
They are therefore treated as validation and future enhancement layers.

## Score Formula

The Speed Safety Score is the sum of six components.

| Component | Maximum points | Purpose |
| --- | ---: | --- |
| Posted limit alignment | 30 | Penalizes high posted speeds in urban or vulnerable-user contexts. |
| Operating speed behavior | 25 | Captures share over limit and F85/median speed gaps. |
| Exposure proxy | 15 | Prioritizes segments with larger speed-observation samples and longer lengths. |
| Vulnerable-user context | 15 | Adds concern for urban roads and major non-motorway roads where pedestrians, cyclists, and powered two-wheelers may be exposed. |
| Geometry | 10 | Adds concern for curvy or highly curvy roads with high operating speeds. |
| Data-quality review | 5 | Flags records that may need speed-limit inventory QA or field validation. |

### 1. Posted Limit Alignment, 0-30 Points

Urban segments:

| Posted speed limit | Points |
| ---: | ---: |
| <= 30 km/h | 0 |
| 31-50 km/h | 10 |
| 51-60 km/h | 20 |
| > 60 km/h | 30 |

Rural segments:

| Posted speed limit | Points |
| ---: | ---: |
| <= 50 km/h | 5 |
| 51-60 km/h | 10 |
| 61-80 km/h | 18 |
| > 80 km/h | 24 |

Major roads with posted limits of at least 80 km/h receive up to 4 additional
points, capped at 30. This reflects the Safe System concern that high-speed
major roads require access control, forgiving roadsides, and separation from
vulnerable users.

### 2. Operating Speed Behavior, 0-25 Points

Percent-over-limit points:

| Percent over limit | Points |
| ---: | ---: |
| >= 60% | 12 |
| >= 35% | 8 |
| >= 15% | 4 |
| < 15% | 0 |

Speed-gap points:

| Condition | Points |
| --- | ---: |
| F85 gap >= 25 km/h or median gap >= 15 km/h | 13 |
| F85 gap >= 15 km/h or median gap >= 10 km/h | 9 |
| F85 gap >= 5 km/h | 5 |
| Otherwise | 0 |

The component is capped at 25 points.

### 3. Exposure Proxy, 0-15 Points

Sample-count points:

| Segment observations | Points |
| ---: | ---: |
| >= 10,000,000 | 12 |
| >= 1,000,000 | 9 |
| >= 100,000 | 6 |
| >= 10,000 | 3 |
| < 10,000 | 0 |

Road-length points:

| Segment length | Points |
| ---: | ---: |
| >= 10 km | 3 |
| >= 3 km | 2 |
| < 3 km | 0 |

The component is capped at 15 points. The sample count is not a traffic volume;
it is an exposure proxy until official traffic counts are joined.

### 4. Vulnerable-User Context, 0-15 Points

| Context | Points |
| --- | ---: |
| Urban land use | 8 |
| Rural or unknown land use | 3 |
| Trunk or primary road | +5 |
| Secondary road | +4 |
| Motorway | +1 |

The component is capped at 15 points. This is a proxy for vulnerable-road-user
risk, not a substitute for pedestrian, cyclist, or motorcycle exposure data.

### 5. Geometry, 0-10 Points

Geometry is calculated from the GeoJSON line:

- Sinuosity: line length divided by straight-line endpoint distance.
- Bearing change per km: total direction change divided by line length.

| Geometry and speed condition | Points |
| --- | ---: |
| Highly curvy and F85 >= 70 km/h | 10 |
| Curvy and F85 >= 60 km/h | 7 |
| Curvy at lower speed | 4 |
| Otherwise | 0 |

Curvy means sinuosity >= 1.08 or bearing change >= 45 degrees/km. Highly curvy
means sinuosity >= 1.15 or bearing change >= 90 degrees/km.

### 6. Data-Quality Review, 0-5 Points

| Condition | Points |
| --- | ---: |
| Fewer than 10,000 observations | 3 |
| Posted limit <= 40 km/h, median gap >= 40 km/h, and F85 gap >= 50 km/h | 5 |
| Otherwise | 0 |

This component prevents suspicious records from disappearing. These segments
should be checked against official speed-limit inventories and field context
before final policy action.

## Priority Classes

| Score | Class | Recommended use |
| ---: | --- | --- |
| 0-24 | Lower priority | Keep in dataset; no immediate signal from available speed data. |
| 25-49 | Monitor / validate | Combine with crash, traffic, and local context data. |
| 50-74 | High priority | Candidate for speed-limit review, enforcement, or design review. |
| 75-100 | Critical review | Highest-priority field validation and intervention planning. |

## Evaluation Methodology

The current dataset does not contain crash outcomes, so the model cannot be
validated as a crash-prediction model yet. The correct evaluation plan has two
tracks.

### Internal Evaluation

1. **Reproducibility test:** rerun the script and confirm the same segment scores
   and priority classes are produced.
2. **Sensitivity test:** vary major thresholds by plus/minus 10 percent and
   confirm that the highest-priority corridors remain broadly stable.
3. **Face-validity review:** inspect the top-ranked segments for obviously
   explainable high-risk patterns: high urban speed limits, large F85 gaps,
   high percent-over-limit values, high sample exposure, and challenging
   geometry.
4. **Data-quality audit:** manually review segments receiving QA points and
   check whether speed limits, land-use labels, or geometry segmentation are
   plausible.

### External Validation

When additional data becomes available, evaluate the model against:

- fatal and serious injury crashes by segment,
- pedestrian, cyclist, and powered two-wheeler crashes,
- traffic volume,
- pedestrian and cyclist activity,
- motorcycle exposure,
- school, market, transit, and settlement proximity,
- enforcement history,
- official speed-limit inventory records.

Useful metrics:

- crash concentration captured by the top 5, 10, and 20 percent of scored
  segments,
- fatal and serious injury rate per km by score band,
- vulnerable-user crash rate by score band,
- before-after change in F85 speed and percent over limit after intervention,
- false-positive review rate after field validation.

## AI-Based and Time-Based Speed Limiting Extension

The supplied GeoJSON has no hour, day/night, or timestamp field. Therefore the
current score cannot directly test whether night-time speeding differs from
daytime speeding. This is a high-value extension if raw probe-speed records or
hourly aggregates are available.

### Required Added Fields

At segment-hour level:

- segment ID,
- local timestamp or hour,
- day/night flag,
- observed speed distribution,
- sample count,
- weather if available,
- road lighting if available,
- enforcement or incident flags if available.

### Day/Night Features

For each segment, compute:

- daytime F85 speed,
- night-time F85 speed,
- daytime percent over limit,
- night-time percent over limit,
- night-minus-day F85 gap,
- night-minus-day percent-over gap,
- low-light vulnerable-user context flag.

Then add a time-risk component:

| Condition | Interpretation |
| --- | --- |
| Night F85 much higher than day F85 | Candidate for night enforcement, lighting review, or dynamic speed display. |
| Day F85 higher near schools/markets/transit | Candidate for time-window speed management. |
| Night speeding high but vulnerable-user exposure low | Lower priority than a comparable urban day/evening segment unless crash data says otherwise. |
| Night speeding plus motorcycle crash concentration | High-value candidate for targeted enforcement and lighting/visibility intervention. |

### Dynamic or AI-Assisted Speed Management

A practical competition-ready proposal is not "AI sets the speed limit by
itself." The defensible version is:

1. Use the transparent score to identify candidate corridors.
2. Use time-of-day speed profiles to find recurring unsafe periods.
3. Train a supervised model only after crash, exposure, weather, and enforcement
   data are joined.
4. Let the model recommend a risk state: normal, elevated, or critical.
5. Apply pre-approved speed-management responses:
   - variable message signs,
   - school-zone time windows,
   - night-time motorcycle enforcement,
   - average-speed enforcement,
   - temporary work-zone or weather speed limits.
6. Require agency approval and audit logs for any posted-limit change.

This keeps the AI role decision-support oriented, auditable, and compatible with
public-sector governance.

## Assumptions and Limitations

- The score identifies review priority, not proven crash risk.
- Sample count is an exposure proxy, not official traffic volume.
- Land-use labels are coarse and do not prove vulnerable-user presence.
- Safe System alignment cannot be finalized without road design, roadside risk,
  access control, and crash history.
- Very low posted limits with very high observed speeds may indicate severe
  noncompliance, an inventory error, or a map-matching issue.

## How This Can Win

The strongest competition narrative is:

1. Transparent enough for ministries to trust.
2. Reproducible enough for engineers to rerun.
3. Conservative enough not to overclaim crash risk.
4. Actionable enough to produce ranked corridors and intervention types.
5. Extensible enough to support AI-assisted, time-of-day speed management once
   richer temporal and crash data are joined.

## Reference Guidance

- FHWA describes variable speed limits as a proven safety countermeasure that
  uses roadway information such as traffic speed, volume, weather, and surface
  condition to display appropriate speeds and reduce speed variance.
- FHWA speed-limit guidance emphasizes setting appropriate speeds for all road
  users, especially vulnerable road users, within the Safe System Approach.
- The Global Road Safety Facility guide notes that 30 km/h or lower is generally
  needed where vulnerable road users are present and protective infrastructure is
  missing.
- WHO speed-management guidance connects impact speed directly to fatality risk
  for pedestrians and cyclists, with survivability falling sharply above about
  30 km/h.
