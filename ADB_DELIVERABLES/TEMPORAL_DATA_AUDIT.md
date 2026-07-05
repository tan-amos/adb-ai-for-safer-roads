# Temporal Data Audit for Day/Night Speed Analysis

## Purpose

This audit checks whether the supplied GeoJSON files contain the fields needed
to calculate day/night or time-of-day speeding patterns.

The short answer is: **they do not**.

The current files can support segment-level speed-safety screening from aggregate
speed statistics, but they cannot support a real day/night correlation test
because no timestamp, hour, day/night, or time-period fields are present.

## Files Audited

| File | Features | Property fields |
| --- | ---: | ---: |
| `ADB_Innovation_Thailand.geojson` | 55,884 | 26 |
| `ADB_Innovation_Maharashtra.geojson` | 14,082 | 27 |

## Thailand Schema

The Thailand file contains these property fields:

- `AnalysisStatus`
- `F85thPercentileSpeed`
- `ForAnalysis`
- `InvPercentile`
- `LandUse`
- `MedianSpeed`
- `NO_OF_Result_Segments`
- `NumberOverLimit`
- `OBJECTID`
- `OvertureID`
- `PercentOverLimit`
- `Percent_`
- `Percentile`
- `PercentileBand`
- `ProvinceID`
- `RankedPercentile`
- `RoadClass`
- `RoadLength`
- `SampleSizeTotal`
- `SampleSize_avg`
- `Shape_Length`
- `SpeedLimit`
- `SpeedLimitFloor`
- `StreetImageLink`
- `WeightedSample`
- `english_ro`

No field represents hour, timestamp, local time, day/night, weekday/weekend,
month, season, or observation period.

## Maharashtra Schema

The Maharashtra file contains these property fields:

- `AnalysisStatus`
- `DISSOLVE_ID`
- `ExcludeFromSpeedSPI`
- `F85thPercentileSpeed`
- `LandUse`
- `MedianSpeed`
- `NumberOverLimit`
- `OBJECTID`
- `Pass`
- `PercentOverLimit`
- `Percent_`
- `Percentile`
- `PercentileBand`
- `RankedPercentile`
- `RoadClass`
- `RoadLength`
- `SampleSize_avg`
- `Sample_Size_Total`
- `Shape_Length`
- `SpeedLimit`
- `SpeedLimitFloor`
- `StreetImageLink`
- `UrbanPC`
- `WeightedSample`
- `class`
- `names_primary`
- `subtype`

No field represents hour, timestamp, local time, day/night, weekday/weekend,
month, season, or observation period.

## Why Day/Night Cannot Be Calculated From These Files

A day/night speeding analysis requires at least one time dimension. For example:

- `hour`
- `timestamp`
- `local_time`
- `time_period`
- `day_night`
- `is_night`
- `weekday`
- `month`
- separate daytime and night-time speed summaries

The supplied files only contain aggregate segment-level speed summaries:

- median speed,
- F85 speed,
- percent over limit,
- number over limit,
- total sample size,
- weighted sample,
- road class,
- land use,
- geometry,
- speed limit.

Those fields tell us whether a segment has a speeding problem overall. They do
not tell us when the speeding occurred.

## What We Can Do Now

The current model can identify segments where a time-based or dynamic speed
management pilot would be worth testing. Good candidates are segments with:

- high Speed Safety Scores,
- high F85 speed gaps,
- high percent-over-limit values,
- urban land use,
- trunk or primary road class,
- high sample exposure,
- geometry concerns.

These candidates are suitable for the next data-collection stage:

1. request segment-hour probe-speed records,
2. calculate day/night F85 and percent-over-limit,
3. compare day versus night speed gaps,
4. join crash and vulnerable-user exposure data,
5. decide whether a time-window, night enforcement, school-zone, or variable
   speed-limit response is justified.

## Required Added Output for a True Day/Night Module

For each road segment, the input data should include:

| Field | Purpose |
| --- | --- |
| `segment_id` | Join to the current scored segment table |
| `local_hour` | Separate daytime, evening, and night periods |
| `sample_count` | Ensure each time bucket has enough observations |
| `median_speed` | Compare typical operating speed by time period |
| `f85_speed` | Compare high-end operating speed by time period |
| `percent_over_limit` | Compare noncompliance by time period |
| `day_night` | Simple analysis-ready day/night flag |
| `weather` | Optional control for wet-weather speed risk |
| `lighting` | Optional low-light risk modifier |

## Recommended Competition Framing

Do not claim that the current files prove a day/night speeding relationship.
That would not be technically sound.

The defensible claim is:

> The current model identifies where speed risk is concentrated. A time-of-day
> module is specified and ready to run when segment-hour speed data is available.
> This would allow agencies to distinguish all-day speeding problems from
> night-time, school-window, peak-period, or weather-sensitive speeding problems.

This keeps the submission rigorous while still showing the innovation pathway
for AI-assisted and time-based speed management.
