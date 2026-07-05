# Findings Summary

## What SaiFE Found

SaiFE scored **14,711 usable road segments** across the provided Thailand and
Maharashtra datasets. Each segment received a transparent 0-100 Speed Safety
Score based on posted speed, observed operating speed, share of vehicles over
the limit, exposure proxy, road class, land use, geometry, and data-quality
flags.

The model identified:

| Country | Critical review | High priority | Monitor / validate | Lower priority |
| --- | ---: | ---: | ---: | ---: |
| Thailand | 131 | 6,114 | 4,877 | 12 |
| Maharashtra | 0 | 484 | 2,800 | 293 |

The results show that speed risk is not just a question of whether drivers are
above the posted limit. The strongest signals occur where several concerns
combine: high posted limits, high observed speeds, high share of vehicles over
the limit, urban or vulnerable-user context, major road class, high sample
exposure, and challenging geometry.

## Key Findings

### 1. Thailand Has a Large Set of High-Priority Segments

Thailand produced the highest number of priority segments, including all 131
segments classified as **Critical review**. The top-ranked segments are mainly
urban expressways and major trunk or primary roads where observed speeds are
high relative to the posted limit and where urban context or geometry increases
the need for review.

Examples of high-scoring Thailand segments include:

- Prachim Ratthaya Expressway,
- Chalong Rat Expressway,
- Borommaratchachonnani Elevated Highway,
- Phahonyothin Road,
- Phetkasem Road,
- Sukhumvit Road,
- Mittraphap Road.

These should not automatically be treated as locations where speed limits must
be lowered or raised. They should be treated as priority locations for field
validation, speed-management review, design review, and crash-data matching.

### 2. Maharashtra Shows Fewer Extreme Cases but Clear High-Priority Corridors

Maharashtra did not produce Critical-review segments under the current scoring
thresholds, but it did produce **484 High-priority segments**. These are mainly
trunk, primary, and motorway segments where operating speeds, posted limits,
urban context, or road geometry indicate a need for government review.

Examples of high-scoring Maharashtra segments include:

- Yavatmal Bypass,
- JNPT Road,
- Amravati Bypass,
- urban trunk-road flyover segments,
- rural trunk-road segments with high F85 speeds.

The Maharashtra pattern suggests the need for trunk-road and primary-road speed
management, plus field validation of places where posted limits and observed
speeds appear poorly aligned.

### 3. The Model Separates Different Types of Action

SaiFE does not only rank segments. It assigns an action category that a transport
agency can use:

- **Road design and speed management review:** where geometry and high operating
  speeds combine.
- **Posted speed-limit review against Safe System principles:** where the posted
  limit may be high for the road context.
- **Enforcement or corridor speed management:** where operating speeds are well
  above posted limits.
- **Speed-limit inventory QA and field validation:** where the data suggest a
  possible coding, map-matching, or local-context issue.
- **Monitor and combine with crash/exposure data:** where the speed signal is
  present but not enough for immediate intervention.

This makes the output practical for ministries because the model does not simply
say "dangerous." It says what kind of review is needed next.

## How a Transport Ministry Could Use SaiFE

A transport ministry or road safety agency could use SaiFE as a first-stage
screening tool for speed management. The outputs can support:

1. **National speed-limit review programs**

   Agencies can identify segments where posted limits may not align with Safe
   System principles, especially in urban or vulnerable-user contexts.

2. **Corridor enforcement planning**

   Segments with high percent-over-limit and high F85 speed gaps can be
   prioritized for average-speed enforcement, fixed cameras, mobile enforcement,
   or speed feedback signs.

3. **Road-design review**

   Curved or highly curved roads with high operating speeds can be flagged for
   curve treatment, delineation, shoulder improvements, rumble strips, roadside
   hazard review, or access management.

4. **Field validation and data-quality checks**

   Some segments may reflect incorrect speed-limit inventory, unusual local
   context, or map-matching problems. SaiFE explicitly flags these cases so they
   can be checked before policy decisions are made.

5. **Crash-data integration**

   The score can be joined to fatal and serious injury crash records to identify
   where speed-risk signals overlap with actual harm.

6. **Time-based or dynamic speed-management pilots**

   The current GeoJSON files do not contain timestamp or day/night fields, but
   SaiFE identifies candidate locations where segment-hour speed data should be
   collected first. These can support future variable speed limits, school-zone
   timing, night enforcement, or motorcycle safety programs.

## Specific Decisions the Model Could Inform

SaiFE can inform practical agency decisions such as:

- Which road segments should be reviewed first for speed-limit alignment?
- Where should enforcement resources be deployed?
- Which corridors should be selected for average-speed camera pilots?
- Where are signs alone unlikely to be enough because road geometry is part of
  the problem?
- Which records require speed-limit inventory QA before policy interpretation?
- Where should crash-data matching and field audits be prioritized?
- Which locations should be selected for future time-of-day speed analysis?

The model is best used to prioritize investigation, not to make automatic final
decisions.

## Where Governments Should Prioritize Action

Based on the current outputs, governments should prioritize:

1. **Critical-review Thailand segments**

   These are the highest-scoring locations and should be reviewed first. They
   combine high speeds, urban or major-road context, geometry, and exposure
   signals.

2. **High-priority urban major roads**

   Urban trunk and primary roads deserve special attention because pedestrians,
   cyclists, and powered two-wheeler users are more likely to be present or
   exposed nearby.

3. **High-F85 corridors**

   Segments where the 85th percentile speed is far above the posted limit should
   be reviewed for enforcement, design, or speed-limit credibility.

4. **Curved or highly curved high-speed roads**

   These locations may require engineering treatment, not only enforcement.

5. **Maharashtra trunk and primary roads**

   Maharashtra's results suggest a practical first program focused on trunk and
   primary road speed management, with separate interpretation for urban and
   rural settings.

6. **Temporal-pilot candidates**

   The generated time-based candidate list identifies where governments should
   request segment-hour speed data first if they want to explore variable speed
   limits, night enforcement, or school/time-window speed management.

## Applying SaiFE in Countries With Less Data

SaiFE is designed to scale across different countries because it uses common
road-safety data elements. A country with less data availability could apply the
method in stages.

### Minimum Data Version

At minimum, a country would need:

- road-segment geometry,
- posted speed limit,
- road class,
- urban/rural or land-use category.

With these fields, SaiFE can produce a basic Safe System alignment screen that
flags high posted speeds in urban or vulnerable-user contexts and identifies
geometrically challenging segments.

### Improved Version

A stronger version would add:

- median speed,
- 85th percentile speed,
- percent over limit,
- sample count or traffic-volume proxy.

This enables the full current SaiFE score and priority map.

### Advanced Version

The most complete version would add:

- fatal and serious injury crashes,
- pedestrian, cyclist, and motorcycle crashes,
- traffic volumes,
- motorcycle exposure,
- pedestrian and cyclist activity,
- school, market, and transit locations,
- enforcement history,
- segment-hour speed data,
- weather and lighting conditions.

This would allow the model to move from screening to stronger validation and
time-based speed-management planning.

## Main Limitation

The supplied datasets do not include crash outcomes, traffic volumes,
vulnerable-user exposure counts, or time-of-day speed records. For that reason,
SaiFE should be treated as a transparent prioritization and screening model, not
as a final crash-prediction model.

This limitation is also why the model is useful: it gives agencies a defensible
way to decide where to collect better data, conduct field validation, and focus
limited road-safety resources first.
