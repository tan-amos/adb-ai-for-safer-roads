#!/usr/bin/env python3
"""Build an interactive HTML proposal for ADB."""

from __future__ import annotations

import sys
from pathlib import Path

import plotly.graph_objects as go
import plotly.io as pio
from plotly.offline.offline import get_plotlyjs


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "ADB_road_speed_policy_proposal_interactive.html"
OFFLINE_OUTPUT = ROOT / "ADB_road_speed_policy_proposal_interactive_offline.html"

sys.path.insert(0, str(ROOT / "risk_diagnosis_v1"))
sys.path.insert(0, str(ROOT / "maharashtra_speed_limit_audit"))

import build_curve_regional_policy_story as thai_story  # noqa: E402
import build_maharashtra_speed_limit_audit as maha_audit  # noqa: E402

PLOTLY_CONFIG = {
    "displayModeBar": True,
    "responsive": True,
    "displaylogo": False,
    "modeBarButtonsToRemove": ["lasso2d", "select2d"],
}

BASELINE = [
    {
        "dataset": "Thailand",
        "total_features": 55_884,
        "valid_rows": 11_544,
        "usable_rows": 11_134,
        "candidates": 4_907,
        "dominant_limit": 90,
        "avg_over": 22.6,
        "avg_f85_gap": -2.4,
        "trunk_over": 41.9,
        "trunk_f85_gap": 11.2,
    },
    {
        "dataset": "Maharashtra",
        "total_features": 14_082,
        "valid_rows": 4_010,
        "usable_rows": 3_577,
        "candidates": 500,
        "dominant_limit": 55,
        "avg_over": 27.8,
        "avg_f85_gap": 3.6,
        "trunk_over": 43.3,
        "trunk_f85_gap": 16.9,
    },
]

THAI_REGIONS = [
    {
        "region": "Northeast",
        "avg_over": 24.3,
        "weighted_over": 32.8,
        "valid_rows": 2_844,
        "sample_total": 967_714_524,
        "proposal": "Broader trunk + primary compliance program",
    },
    {
        "region": "South",
        "avg_over": 23.2,
        "weighted_over": 30.7,
        "valid_rows": 1_919,
        "sample_total": 661_509_722,
        "proposal": "Trunk-road speed-management pilot",
    },
    {
        "region": "North",
        "avg_over": 22.4,
        "weighted_over": 33.1,
        "valid_rows": 2_668,
        "sample_total": 889_805_565,
        "proposal": "Trunk-road speed-management pilot",
    },
    {
        "region": "Central/Bangkok/East/West",
        "avg_over": 19.0,
        "weighted_over": 25.9,
        "valid_rows": 4_112,
        "sample_total": 6_282_654_155,
        "proposal": "High-exposure corridor validation track",
    },
]

THAI_TRUNK = [
    {"region": "North", "avg_over": 46.6, "weighted_over": 49.6},
    {"region": "South", "avg_over": 45.1, "weighted_over": 42.6},
    {"region": "Central/Bangkok/East/West", "avg_over": 35.9, "weighted_over": 34.4},
    {"region": "Northeast", "avg_over": 35.5, "weighted_over": 40.4},
]

THAI_ROAD_CLASSES = [
    {"road_class": "trunk", "avg_over": 40.4, "avg_f85_gap": 10.8, "valid_segments": 2_085},
    {"road_class": "motorway", "avg_over": 32.9, "avg_f85_gap": 5.4, "valid_segments": 142},
    {"road_class": "primary", "avg_over": 26.8, "avg_f85_gap": 2.1, "valid_segments": 3_312},
    {"road_class": "secondary", "avg_over": 12.4, "avg_f85_gap": -9.4, "valid_segments": 6_005},
]

THAI_REGION_ACTIONS = [
    {
        "region": "Central/Bangkok/East/West",
        "qa": 71,
        "decrease": 762,
        "enforcement": 524,
        "design": 307,
    },
    {"region": "North", "qa": 49, "decrease": 385, "enforcement": 429, "design": 272},
    {"region": "Northeast", "qa": 56, "decrease": 343, "enforcement": 588, "design": 214},
    {"region": "South", "qa": 73, "decrease": 318, "enforcement": 329, "design": 187},
]

THAI_CREDIBILITY = [
    {"region": "Northeast", "road_class": "motorway", "f85_gap": 32.6, "avg_over": 65.7, "valid_segments": 4},
    {"region": "South", "road_class": "trunk", "f85_gap": 14.5, "avg_over": 45.1, "valid_segments": 513},
    {"region": "North", "road_class": "trunk", "f85_gap": 13.8, "avg_over": 46.6, "valid_segments": 451},
    {"region": "Northeast", "road_class": "trunk", "f85_gap": 8.8, "avg_over": 35.5, "valid_segments": 443},
    {"region": "Central/Bangkok/East/West", "road_class": "trunk", "f85_gap": 7.3, "avg_over": 35.9, "valid_segments": 678},
    {"region": "South", "road_class": "primary", "f85_gap": 4.8, "avg_over": 29.3, "valid_segments": 373},
    {"region": "Northeast", "road_class": "primary", "f85_gap": 4.6, "avg_over": 31.1, "valid_segments": 1_121},
    {"region": "Central/Bangkok/East/West", "road_class": "motorway", "f85_gap": 4.6, "avg_over": 32.0, "valid_segments": 138},
]

THAI_TOP_SEGMENTS = [
    {
        "road": "Buraphawithi Expressway",
        "province": "Samut Prakan",
        "region": "Central/Bangkok/East/West",
        "road_class": "motorway",
        "percent_over": 72.5,
        "f85_gap": 19.9,
        "sample": 79_510_537,
        "length": 15.3,
    },
    {
        "road": "Buraphawithi Expressway",
        "province": "Samut Prakan",
        "region": "Central/Bangkok/East/West",
        "road_class": "motorway",
        "percent_over": 72.7,
        "f85_gap": 29.9,
        "sample": 81_032_639,
        "length": 10.1,
    },
    {
        "road": "Rama II Road",
        "province": "Samut Sakhon",
        "region": "Central/Bangkok/East/West",
        "road_class": "trunk",
        "percent_over": 27.9,
        "f85_gap": 10.2,
        "sample": 74_244_168,
        "length": 20.9,
    },
    {
        "road": "Phahon Yothin Road",
        "province": "Ayutthaya",
        "region": "Central/Bangkok/East/West",
        "road_class": "trunk",
        "percent_over": 33.4,
        "f85_gap": 10.6,
        "sample": 44_973_186,
        "length": 22.8,
    },
    {
        "road": "Phahonyothin Road",
        "province": "Tak",
        "region": "North",
        "road_class": "trunk",
        "percent_over": 66.1,
        "f85_gap": 20.6,
        "sample": 7_075_011,
        "length": 72.5,
    },
]

THAI_QA_30 = [
    {"province": "Pattani", "road_class": "trunk", "land_use": "RURAL", "median_gap": 70.6, "f85_gap": 88.0, "sample": 283_627},
    {"province": "Narathiwat", "road_class": "trunk", "land_use": "RURAL", "median_gap": 67.1, "f85_gap": 85.0, "sample": 106_094},
    {"province": "Pattani", "road_class": "trunk", "land_use": "RURAL", "median_gap": 66.4, "f85_gap": 84.0, "sample": 276_466},
    {"province": "Pattani", "road_class": "trunk", "land_use": "URBAN", "median_gap": 67.0, "f85_gap": 83.0, "sample": 272_585},
    {"province": "Ayutthaya", "road_class": "primary", "land_use": "RURAL", "median_gap": 63.7, "f85_gap": 79.0, "sample": 237_727},
]

THAI_ACTIONS = {
    "Enforcement / speed management": 1_870,
    "Investigate possible decrease": 1_808,
    "Road design change": 980,
    "Investigate possible increase / QA": 249,
}

MAHA_ACTIONS = {
    "Enforcement / speed management": 368,
    "Investigate possible increase / QA": 93,
    "Investigate possible decrease": 20,
    "Road design change": 19,
}

MAHA_ROAD_CLASS_ACTIONS = [
    {"road_class": "trunk", "action": "Enforcement / speed management", "count": 260},
    {"road_class": "trunk", "action": "Investigate possible increase / QA", "count": 84},
    {"road_class": "trunk", "action": "Road design change", "count": 18},
    {"road_class": "trunk", "action": "Investigate possible decrease", "count": 13},
    {"road_class": "primary", "action": "Enforcement / speed management", "count": 91},
    {"road_class": "primary", "action": "Investigate possible increase / QA", "count": 6},
    {"road_class": "primary", "action": "Investigate possible decrease", "count": 7},
    {"road_class": "motorway", "action": "Enforcement / speed management", "count": 17},
    {"road_class": "motorway", "action": "Investigate possible increase / QA", "count": 3},
    {"road_class": "motorway", "action": "Road design change", "count": 1},
]

MAHA_LAND_USE = [
    {"land_use": "Rural", "enforcement": 246, "qa": 82, "decrease": 7, "design": 18},
    {"land_use": "Urban", "enforcement": 122, "qa": 11, "decrease": 13, "design": 1},
]

ACTION_COLORS = {
    "Enforcement / speed management": "#f59e0b",
    "Investigate possible increase / QA": "#7c3aed",
    "Investigate possible decrease": "#dc2626",
    "Road design change": "#0891b2",
}


def apply_layout(fig: go.Figure, title: str, height: int = 460) -> go.Figure:
    fig.update_layout(
        title={"text": title, "x": 0.02, "xanchor": "left"},
        height=height,
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin={"l": 55, "r": 30, "t": 72, "b": 60},
        font={"family": "Inter, Arial, sans-serif", "size": 13, "color": "#172033"},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1},
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(gridcolor="#e5e7eb", zeroline=False)
    return fig


def fig_to_html(fig: go.Figure, div_id: str) -> str:
    return pio.to_html(
        fig,
        include_plotlyjs=False,
        full_html=False,
        config=PLOTLY_CONFIG,
        div_id=div_id,
    )


def baseline_chart() -> go.Figure:
    fig = go.Figure()
    for metric, label, color in [
        ("usable_rows", "Usable speed rows", "#2563eb"),
        ("candidates", "Action candidates", "#dc2626"),
    ]:
        fig.add_trace(
            go.Bar(
                x=[row["dataset"] for row in BASELINE],
                y=[row[metric] for row in BASELINE],
                name=label,
                marker_color=color,
                hovertemplate="%{x}<br>" + label + ": %{y:,}<extra></extra>",
            )
        )
    fig.add_trace(
        go.Scatter(
            x=[row["dataset"] for row in BASELINE],
            y=[row["avg_over"] for row in BASELINE],
            name="Avg % over limit",
            mode="lines+markers+text",
            text=[f"{row['avg_over']:.1f}%" for row in BASELINE],
            textposition="top center",
            marker={"size": 12, "color": "#111827"},
            yaxis="y2",
            hovertemplate="%{x}<br>Avg over limit: %{y:.1f}%<extra></extra>",
        )
    )
    fig.update_layout(
        yaxis={"title": "Rows / candidate segments"},
        yaxis2={
            "title": "Avg % over limit",
            "overlaying": "y",
            "side": "right",
            "ticksuffix": "%",
            "range": [0, 50],
            "showgrid": False,
        },
        barmode="group",
    )
    return apply_layout(fig, "Shared Baseline: Same Screening Method, Different Scale")


def speed_limit_chart() -> go.Figure:
    fig = go.Figure(
        data=[
            go.Bar(
                x=[row["dataset"] for row in BASELINE],
                y=[row["dominant_limit"] for row in BASELINE],
                marker_color=["#2563eb", "#16a34a"],
                text=[f"{row['dominant_limit']} km/h" for row in BASELINE],
                textposition="outside",
                hovertemplate="%{x}<br>Dominant posted limit: %{y} km/h<extra></extra>",
            )
        ]
    )
    fig.update_layout(yaxis_title="Dominant posted speed limit (km/h)")
    return apply_layout(fig, "Why the Stories Split: Thailand's 90 km/h Pattern vs Maharashtra's 55 km/h Pattern", 390)


def thailand_region_chart() -> go.Figure:
    max_sample = max(row["sample_total"] for row in THAI_REGIONS)
    sizes = [24 + 58 * (row["sample_total"] / max_sample) ** 0.5 for row in THAI_REGIONS]
    fig = go.Figure(
        data=[
            go.Scatter(
                x=[row["avg_over"] for row in THAI_REGIONS],
                y=[row["weighted_over"] for row in THAI_REGIONS],
                mode="markers+text",
                text=[row["region"] for row in THAI_REGIONS],
                textposition="top center",
                marker={
                    "size": sizes,
                    "color": [row["sample_total"] for row in THAI_REGIONS],
                    "colorscale": "Blues",
                    "showscale": True,
                    "colorbar": {"title": "Sample total"},
                    "line": {"color": "#172033", "width": 1},
                },
                customdata=[
                    [row["valid_rows"], row["sample_total"], row["proposal"]]
                    for row in THAI_REGIONS
                ],
                hovertemplate=(
                    "<b>%{text}</b><br>"
                    "Avg over: %{x:.1f}%<br>"
                    "Sample-weighted over: %{y:.1f}%<br>"
                    "Valid rows: %{customdata[0]:,}<br>"
                    "Sample total: %{customdata[1]:,}<br>"
                    "Proposal: %{customdata[2]}<extra></extra>"
                ),
            )
        ]
    )
    fig.update_layout(
        xaxis_title="Average % over limit",
        yaxis_title="Sample-weighted % over limit",
    )
    return apply_layout(fig, "Thailand: Central Has Exposure; Outer Regions Have Weaker Compliance")


def thailand_trunk_chart() -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=[row["region"] for row in THAI_TRUNK],
            y=[row["avg_over"] for row in THAI_TRUNK],
            name="Trunk avg % over",
            marker_color="#2563eb",
            hovertemplate="%{x}<br>Avg over: %{y:.1f}%<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[row["region"] for row in THAI_TRUNK],
            y=[row["weighted_over"] for row in THAI_TRUNK],
            name="Trunk sample-weighted % over",
            mode="lines+markers+text",
            text=[f"{row['weighted_over']:.1f}%" for row in THAI_TRUNK],
            textposition="top center",
            marker={"size": 11, "color": "#dc2626"},
            hovertemplate="%{x}<br>Weighted over: %{y:.1f}%<extra></extra>",
        )
    )
    fig.update_layout(yaxis_title="% over posted limit", yaxis_ticksuffix="%")
    return apply_layout(fig, "Thailand: Trunk Roads Are the First Road Class to Investigate")


def thailand_road_class_chart() -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=[row["road_class"] for row in THAI_ROAD_CLASSES],
            y=[row["avg_over"] for row in THAI_ROAD_CLASSES],
            name="Avg % over limit",
            marker_color="#2563eb",
            customdata=[[row["valid_segments"]] for row in THAI_ROAD_CLASSES],
            hovertemplate="%{x}<br>Avg over: %{y:.1f}%<br>Valid segments: %{customdata[0]:,}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[row["road_class"] for row in THAI_ROAD_CLASSES],
            y=[row["avg_f85_gap"] for row in THAI_ROAD_CLASSES],
            name="Avg F85 gap",
            mode="lines+markers+text",
            text=[f"{row['avg_f85_gap']:+.1f}" for row in THAI_ROAD_CLASSES],
            textposition="top center",
            marker={"size": 11, "color": "#dc2626"},
            yaxis="y2",
            hovertemplate="%{x}<br>Avg F85 gap: %{y:+.1f} km/h<extra></extra>",
        )
    )
    fig.update_layout(
        yaxis={"title": "Avg % over limit", "ticksuffix": "%"},
        yaxis2={
            "title": "Avg F85 gap (km/h)",
            "overlaying": "y",
            "side": "right",
            "showgrid": False,
        },
    )
    return apply_layout(fig, "Thailand: Road-Class Evidence Behind the Trunk Recommendation")


def thailand_region_action_chart() -> go.Figure:
    fig = go.Figure()
    mapping = [
        ("enforcement", "Enforcement / speed management"),
        ("decrease", "Investigate possible decrease"),
        ("design", "Road design change"),
        ("qa", "Investigate possible increase / QA"),
    ]
    for key, label in mapping:
        fig.add_trace(
            go.Bar(
                x=[row["region"] for row in THAI_REGION_ACTIONS],
                y=[row[key] for row in THAI_REGION_ACTIONS],
                name=label,
                marker_color=ACTION_COLORS[label],
                hovertemplate="%{x}<br>" + label + ": %{y:,}<extra></extra>",
            )
        )
    fig.update_layout(barmode="stack", yaxis_title="Candidate segments")
    return apply_layout(fig, "Thailand: What Each Region Should Investigate Next", 500)


def thailand_credibility_chart() -> go.Figure:
    labels = [f"{row['region']}<br>{row['road_class']}" for row in THAI_CREDIBILITY]
    fig = go.Figure(
        data=[
            go.Bar(
                x=labels,
                y=[row["f85_gap"] for row in THAI_CREDIBILITY],
                marker_color=[
                    "#9ca3af" if row["valid_segments"] < 20 else "#2563eb"
                    for row in THAI_CREDIBILITY
                ],
                customdata=[
                    [row["avg_over"], row["valid_segments"]]
                    for row in THAI_CREDIBILITY
                ],
                hovertemplate=(
                    "%{x}<br>Avg F85 gap: %{y:+.1f} km/h<br>"
                    "Avg over: %{customdata[0]:.1f}%<br>"
                    "Valid segments: %{customdata[1]:,}<extra></extra>"
                ),
            )
        ]
    )
    fig.update_layout(yaxis_title="Avg F85 minus posted limit (km/h)")
    return apply_layout(fig, "Thailand: Speed-Limit Credibility Signals by Region and Road Class", 500)


def thailand_exposure_segment_chart() -> go.Figure:
    labels = [
        f"{row['road']}<br>{row['province']}"
        for row in THAI_TOP_SEGMENTS
    ]
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=labels,
            y=[row["sample"] for row in THAI_TOP_SEGMENTS],
            name="Observed speed samples",
            marker_color="#64748b",
            customdata=[
                [row["region"], row["road_class"], row["percent_over"], row["f85_gap"], row["length"]]
                for row in THAI_TOP_SEGMENTS
            ],
            hovertemplate=(
                "%{x}<br>Region: %{customdata[0]}<br>"
                "Class: %{customdata[1]}<br>"
                "Samples: %{y:,}<br>"
                "% over: %{customdata[2]:.1f}%<br>"
                "F85 gap: %{customdata[3]:+.1f} km/h<br>"
                "Length: %{customdata[4]:.1f} km<extra></extra>"
            ),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=labels,
            y=[row["percent_over"] for row in THAI_TOP_SEGMENTS],
            name="% over limit",
            mode="lines+markers+text",
            text=[f"{row['percent_over']:.1f}%" for row in THAI_TOP_SEGMENTS],
            textposition="top center",
            marker={"size": 10, "color": "#dc2626"},
            yaxis="y2",
            hovertemplate="%{x}<br>% over limit: %{y:.1f}%<extra></extra>",
        )
    )
    fig.update_layout(
        yaxis={"title": "Observed speed samples"},
        yaxis2={
            "title": "% over limit",
            "overlaying": "y",
            "side": "right",
            "ticksuffix": "%",
            "showgrid": False,
        },
    )
    return apply_layout(fig, "Thailand: Why Central Still Matters Despite Better Average Compliance", 540)


def action_mix_chart() -> go.Figure:
    labels = list(THAI_ACTIONS)
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=labels,
            y=[THAI_ACTIONS[label] for label in labels],
            name="Thailand",
            marker_color="#2563eb",
            hovertemplate="Thailand<br>%{x}: %{y:,}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            x=labels,
            y=[MAHA_ACTIONS.get(label, 0) for label in labels],
            name="Maharashtra",
            marker_color="#16a34a",
            hovertemplate="Maharashtra<br>%{x}: %{y:,}<extra></extra>",
        )
    )
    fig.update_layout(barmode="group", yaxis_title="Candidate segments")
    return apply_layout(fig, "Same Formula, Different Action Mix", 500)


def maharashtra_road_class_chart() -> go.Figure:
    road_classes = ["trunk", "primary", "motorway"]
    fig = go.Figure()
    for action in ACTION_COLORS:
        values = [
            sum(row["count"] for row in MAHA_ROAD_CLASS_ACTIONS if row["road_class"] == rc and row["action"] == action)
            for rc in road_classes
        ]
        fig.add_trace(
            go.Bar(
                x=road_classes,
                y=values,
                name=action,
                marker_color=ACTION_COLORS[action],
                hovertemplate="%{x}<br>" + action + ": %{y:,}<extra></extra>",
            )
        )
    fig.update_layout(barmode="stack", yaxis_title="Candidate segments")
    return apply_layout(fig, "Maharashtra: Trunk Roads Dominate the Action List")


def maharashtra_land_use_chart() -> go.Figure:
    fig = go.Figure()
    mapping = [
        ("enforcement", "Enforcement / speed management"),
        ("qa", "Investigate possible increase / QA"),
        ("decrease", "Investigate possible decrease"),
        ("design", "Road design change"),
    ]
    for key, label in mapping:
        fig.add_trace(
            go.Bar(
                x=[row["land_use"] for row in MAHA_LAND_USE],
                y=[row[key] for row in MAHA_LAND_USE],
                name=label,
                marker_color=ACTION_COLORS[label],
                hovertemplate="%{x}<br>" + label + ": %{y:,}<extra></extra>",
            )
        )
    fig.update_layout(barmode="stack", yaxis_title="Candidate segments")
    return apply_layout(fig, "Maharashtra: Rural and Urban Reviews Should Be Separated")


def workflow_chart() -> go.Figure:
    labels = [
        "Observed speed data",
        "Road class",
        "Speed limit",
        "Geometry",
        "Screening formula",
        "Enforcement",
        "Speed-limit QA",
        "Decrease review",
        "Design review",
        "Crash + field validation",
        "Pilot intervention",
    ]
    idx = {label: i for i, label in enumerate(labels)}
    sources = [
        "Observed speed data",
        "Road class",
        "Speed limit",
        "Geometry",
        "Screening formula",
        "Screening formula",
        "Screening formula",
        "Screening formula",
        "Screening formula",
        "Enforcement",
        "Speed-limit QA",
        "Decrease review",
        "Design review",
        "Crash + field validation",
    ]
    targets = [
        "Screening formula",
        "Screening formula",
        "Screening formula",
        "Screening formula",
        "Enforcement",
        "Speed-limit QA",
        "Decrease review",
        "Design review",
        "Crash + field validation",
        "Crash + field validation",
        "Crash + field validation",
        "Crash + field validation",
        "Crash + field validation",
        "Pilot intervention",
    ]
    values = [3, 2, 2, 2, 4, 2, 2, 2, 5, 2, 2, 2, 2, 8]
    fig = go.Figure(
        data=[
            go.Sankey(
                node={
                    "label": labels,
                    "pad": 18,
                    "thickness": 18,
                    "color": [
                        "#2563eb",
                        "#2563eb",
                        "#2563eb",
                        "#2563eb",
                        "#172033",
                        "#f59e0b",
                        "#7c3aed",
                        "#dc2626",
                        "#0891b2",
                        "#64748b",
                        "#16a34a",
                    ],
                },
                link={
                    "source": [idx[source] for source in sources],
                    "target": [idx[target] for target in targets],
                    "value": values,
                    "color": "rgba(100,116,139,0.28)",
                },
            )
        ]
    )
    return apply_layout(fig, "Proposed ADB Workflow: Screen, Validate, Then Intervene", 520)


def card(title: str, body: str, accent: str = "#2563eb") -> str:
    return f"""
    <article class="card" style="border-top-color:{accent}">
      <h3>{title}</h3>
      <p>{body}</p>
    </article>
    """


def thai_action_rows() -> str:
    return "\n".join(
        f"""<tr>
          <td>{row['region']}</td>
          <td>{row['qa']:,}</td>
          <td>{row['decrease']:,}</td>
          <td>{row['enforcement']:,}</td>
          <td>{row['design']:,}</td>
        </tr>"""
        for row in THAI_REGION_ACTIONS
    )


def thai_qa_rows() -> str:
    return "\n".join(
        f"""<tr>
          <td>{row['province']}</td>
          <td>{row['road_class']}</td>
          <td>{row['land_use']}</td>
          <td>30 km/h</td>
          <td>{row['median_gap']:+.1f} km/h</td>
          <td>{row['f85_gap']:+.1f} km/h</td>
          <td>{row['sample']:,}</td>
        </tr>"""
        for row in THAI_QA_30
    )


def render(include_plotlyjs: bool) -> str:
    plotlyjs = f"<script>{get_plotlyjs()}</script>" if include_plotlyjs else '<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>'
    thai_action_candidates = thai_story.load_action_candidates()
    maha_rows, _ = maha_audit.load_rows()
    maha_candidates = maha_audit.candidate_rows(maha_rows)
    charts = {
        "baseline": fig_to_html(baseline_chart(), "baseline-chart"),
        "speed_limit": fig_to_html(speed_limit_chart(), "speed-limit-chart"),
        "thai_region": fig_to_html(thailand_region_chart(), "thai-region-chart"),
        "thai_road_class": fig_to_html(thailand_road_class_chart(), "thai-road-class-chart"),
        "thai_trunk": fig_to_html(thailand_trunk_chart(), "thai-trunk-chart"),
        "thai_region_action": fig_to_html(thailand_region_action_chart(), "thai-region-action-chart"),
        "thai_credibility": fig_to_html(thailand_credibility_chart(), "thai-credibility-chart"),
        "thai_exposure": fig_to_html(thailand_exposure_segment_chart(), "thai-exposure-segment-chart"),
        "thai_policy_map": fig_to_html(thai_story.regional_policy_map(), "thai-policy-map"),
        "thai_action_map": fig_to_html(thai_story.action_audit_map(thai_action_candidates), "thai-action-map"),
        "action_mix": fig_to_html(action_mix_chart(), "action-mix-chart"),
        "maha_road": fig_to_html(maharashtra_road_class_chart(), "maha-road-class-chart"),
        "maha_land": fig_to_html(maharashtra_land_use_chart(), "maha-land-use-chart"),
        "maha_action_map": fig_to_html(maha_audit.action_map(maha_candidates), "maha-action-map"),
        "maha_road_class_map": fig_to_html(maha_audit.road_class_map(maha_candidates), "maha-road-class-map"),
        "workflow": fig_to_html(workflow_chart(), "workflow-chart"),
    }
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>ADB Road Speed Management Proposal</title>
  {plotlyjs}
  <style>
    :root {{
      --ink: #172033;
      --muted: #5b6475;
      --line: #d8dee9;
      --soft: #f4f7fb;
      --blue: #2563eb;
      --green: #16a34a;
      --red: #dc2626;
      --amber: #f59e0b;
      --teal: #0891b2;
      --purple: #7c3aed;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      color: var(--ink);
      background: #ffffff;
      font-family: Inter, Arial, sans-serif;
      line-height: 1.55;
    }}
    header {{
      min-height: 88vh;
      display: grid;
      align-items: end;
      padding: 56px 6vw;
      color: white;
      background:
        linear-gradient(90deg, rgba(13,23,43,0.92), rgba(13,23,43,0.58)),
        url("https://images.unsplash.com/photo-1544984243-ec57ea16fe25?auto=format&fit=crop&w=2200&q=80");
      background-size: cover;
      background-position: center;
    }}
    header .inner {{ max-width: 1000px; }}
    header p {{ max-width: 860px; color: rgba(255,255,255,0.88); font-size: 1.13rem; }}
    h1 {{
      margin: 0 0 20px;
      max-width: 980px;
      font-size: clamp(2.4rem, 5vw, 5.5rem);
      line-height: 0.98;
      letter-spacing: 0;
    }}
    h2 {{ margin: 0 0 14px; font-size: clamp(1.55rem, 2.5vw, 2.4rem); line-height: 1.12; }}
    h3 {{ margin: 0 0 8px; font-size: 1.05rem; }}
    p {{ margin: 0 0 16px; }}
    .eyebrow {{
      margin-bottom: 18px;
      color: rgba(255,255,255,0.78);
      text-transform: uppercase;
      font-size: 0.82rem;
      letter-spacing: 0.08em;
      font-weight: 700;
    }}
    .section {{
      padding: 64px 6vw;
      border-bottom: 1px solid var(--line);
    }}
    .section.soft {{ background: var(--soft); }}
    .wrap {{ max-width: 1180px; margin: 0 auto; }}
    .lead {{ max-width: 980px; color: var(--muted); font-size: 1.05rem; }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 16px;
      margin-top: 28px;
    }}
    .grid.two {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    .card {{
      background: white;
      border: 1px solid var(--line);
      border-top: 4px solid var(--blue);
      border-radius: 8px;
      padding: 20px;
      min-height: 142px;
    }}
    .card p {{ color: var(--muted); margin-bottom: 0; }}
    .metric-row {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
      margin-top: 28px;
    }}
    .metric {{
      padding: 18px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: white;
    }}
    .metric .value {{ display: block; font-size: 1.8rem; font-weight: 800; line-height: 1.1; }}
    .metric .label {{ display: block; margin-top: 6px; color: var(--muted); font-size: 0.92rem; }}
    .chart {{
      margin-top: 28px;
      background: white;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 8px;
      overflow: hidden;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      background: white;
      border: 1px solid var(--line);
      border-radius: 8px;
      overflow: hidden;
      margin-top: 24px;
      font-size: 0.94rem;
    }}
    th, td {{ padding: 12px 14px; text-align: left; border-bottom: 1px solid var(--line); vertical-align: top; }}
    th {{ background: #edf2f7; }}
    tr:last-child td {{ border-bottom: 0; }}
    .callout {{
      margin-top: 24px;
      padding: 20px;
      border-left: 5px solid var(--blue);
      background: #eff6ff;
      border-radius: 8px;
    }}
    .callout strong {{ display: block; margin-bottom: 6px; }}
    .split {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 22px;
      align-items: start;
      margin-top: 28px;
    }}
    ol, ul {{ margin: 12px 0 0 22px; padding: 0; color: var(--muted); }}
    li {{ margin: 7px 0; }}
    footer {{
      padding: 34px 6vw;
      color: var(--muted);
      background: #111827;
    }}
    footer a {{ color: white; }}
    @media (max-width: 820px) {{
      header {{ min-height: 74vh; padding: 38px 5vw; }}
      .section {{ padding: 44px 5vw; }}
      .grid, .grid.two, .metric-row, .split {{ grid-template-columns: 1fr; }}
      table {{ display: block; overflow-x: auto; }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="inner">
      <div class="eyebrow">Interactive Proposal for Asian Development Bank</div>
      <h1>Data-Driven Road Speed Management Screening</h1>
      <p>
        A two-country pilot for Thailand and Maharashtra that turns observed speed behavior, road class,
        speed limits, geometry, and sample exposure into field-review priorities for enforcement,
        speed-limit credibility review, and road-design intervention.
      </p>
    </div>
  </header>

  <section class="section">
    <div class="wrap">
      <h2>Proposal in one sentence</h2>
      <p class="lead">
        ADB should support a repeatable road-speed screening workflow: use the same technical formula
        to classify candidate corridors, then adapt the policy response to each geography before any
        speed-limit or construction decision is made.
      </p>
      <div class="metric-row">
        <div class="metric"><span class="value">55,884</span><span class="label">Thailand road features reviewed</span></div>
        <div class="metric"><span class="value">14,082</span><span class="label">Maharashtra road features reviewed</span></div>
        <div class="metric"><span class="value">4,907</span><span class="label">Thailand action candidates</span></div>
        <div class="metric"><span class="value">500</span><span class="label">Maharashtra action candidates</span></div>
      </div>
      <div class="callout">
        <strong>Main finding</strong>
        The method transfers; the narrative does not. Thailand is a regional exposure-versus-compliance
        problem. Maharashtra is a road-class, land-use, and speed-limit credibility problem.
      </div>
    </div>
  </section>

  <section class="section soft">
    <div class="wrap">
      <h2>Same baseline, then the stories split</h2>
      <p class="lead">
        Both datasets can be normalized into comparable fields: road class, speed limit, median speed,
        F85 speed, percent over limit, geometry, and sample count. But the distributions are different
        enough that copying one policy story into the other would be a mistake.
      </p>
      <div class="chart">{charts["baseline"]}</div>
      <div class="chart">{charts["speed_limit"]}</div>
      <table>
        <thead>
          <tr>
            <th>Dataset</th>
            <th>Usable rows</th>
            <th>Action candidates</th>
            <th>Dominant speed limit</th>
            <th>Avg % over limit</th>
            <th>Trunk % over</th>
            <th>Trunk F85 gap</th>
          </tr>
        </thead>
        <tbody>
          <tr><td>Thailand</td><td>11,134</td><td>4,907</td><td>90 km/h</td><td>22.6%</td><td>41.9%</td><td>+11.2 km/h</td></tr>
          <tr><td>Maharashtra</td><td>3,577</td><td>500</td><td>55 km/h</td><td>27.8%</td><td>43.3%</td><td>+16.9 km/h</td></tr>
        </tbody>
      </table>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <h2>The shared action formula</h2>
      <p class="lead">
        These categories are not final decisions. They are investigation tracks that tell a road agency
        what kind of evidence to collect next.
      </p>
      <div class="callout">
        <strong>How to present this to ADB</strong>
        The formula is a triage system. It separates road segments into the type of review they need:
        enforcement, speed-limit credibility review, possible lowering review, or engineering design
        review. It is not a final crash-risk score, and it is not a final recommendation to raise or
        lower speed limits.
      </div>
      <table>
        <thead>
          <tr>
            <th>Variable</th>
            <th>Definition</th>
            <th>Why it matters</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><code>sample_total</code></td>
            <td>Observed speed sample count from the dataset.</td>
            <td>Filters out weak evidence. A segment must have at least 50,000 observed speed samples to enter the action audit.</td>
          </tr>
          <tr>
            <td><code>median_gap</code></td>
            <td><code>MedianSpeed - SpeedLimit</code></td>
            <td>Shows whether typical drivers are above or below the posted limit.</td>
          </tr>
          <tr>
            <td><code>F85_gap</code></td>
            <td><code>F85thPercentileSpeed - SpeedLimit</code></td>
            <td>Shows whether faster operating speeds are materially above or below the posted limit.</td>
          </tr>
          <tr>
            <td><code>percent_over</code></td>
            <td><code>PercentOverLimit</code></td>
            <td>Shows the share of observed speeds exceeding the posted limit.</td>
          </tr>
          <tr>
            <td><code>major road</code></td>
            <td>Motorway, trunk, or primary road.</td>
            <td>Focuses enforcement screening on higher-order corridors.</td>
          </tr>
          <tr>
            <td><code>curved/highly curved</code></td>
            <td>Geometry bucket based on road sinuosity and bearing change per kilometer.</td>
            <td>Flags roads where speed should be interpreted against design speed and roadside context.</td>
          </tr>
        </tbody>
      </table>
      <table>
        <thead>
          <tr>
            <th>Action bucket</th>
            <th>Screening formula</th>
            <th>What ADB should understand</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Enforcement / speed management</td>
            <td><code>sample_total >= 50,000</code><br><code>major road</code><br><code>percent_over >= 35%</code><br><code>F85_gap >= +5 km/h</code></td>
            <td>Drivers are often exceeding the posted limit on a major corridor. Start with enforcement, average-speed management, corridor operations, or speed harmonization.</td>
          </tr>
          <tr>
            <td>Possible increase / QA</td>
            <td><code>sample_total >= 50,000</code><br><code>speed_limit <= 60 km/h</code><br><code>median_gap >= +15 km/h</code><br><code>F85_gap >= +25 km/h</code><br><code>percent_over >= 60%</code></td>
            <td>The limit may be miscoded, locally special, unrealistic, or severely ignored. This is a QA and field-review candidate, not an automatic increase.</td>
          </tr>
          <tr>
            <td>Possible decrease review</td>
            <td><code>sample_total >= 50,000</code><br><code>speed_limit >= 80 km/h</code><br><code>curved/highly curved</code><br><code>F85_gap <= -5 km/h</code><br><code>percent_over <= 15%</code></td>
            <td>Drivers are already operating below a high posted limit on a curved road. Check whether the posted limit is too high for design speed, roadside context, or crash history.</td>
          </tr>
          <tr>
            <td>Road design change</td>
            <td><code>sample_total >= 50,000</code><br><code>speed_limit >= 70 km/h</code><br><code>curved/highly curved</code><br><code>F85_gap >= 0 km/h OR percent_over >= 25%</code></td>
            <td>Drivers remain fast on curved roads. Signs alone may not solve the problem; review curve treatment, delineation, access, shoulder, and roadside forgiveness.</td>
          </tr>
        </tbody>
      </table>
      <div class="grid two">
        {card("Enforcement / speed management", "Major roads where at least 35% of observations are over the limit and F85 is at least 5 km/h above the posted limit.", "#f59e0b")}
        {card("Possible increase / QA", "Limits at or below 60 km/h where median, F85, and over-limit share are all far above the posted limit. This may be severe noncompliance, miscoding, map matching, or a special context.", "#7c3aed")}
        {card("Possible decrease review", "High-limit curved roads where F85 is already below the posted limit and over-limit share is low. Review design speed and roadside risk.", "#dc2626")}
        {card("Road design change", "Curved or highly curved roads where speeds remain high. Signs alone may not be enough; the road environment may need treatment.", "#0891b2")}
      </div>
      <div class="chart">{charts["action_mix"]}</div>
      <div class="callout">
        <strong>Result of applying the formula</strong>
        Thailand produces 4,907 candidate segments: 1,870 enforcement / speed management, 1,808 possible
        decrease review, 980 road design change, and 249 possible increase / QA. Maharashtra produces
        500 candidate segments: 368 enforcement / speed management, 93 possible increase / QA, 20 possible
        decrease review, and 19 road design change.
      </div>
    </div>
  </section>

  <section class="section soft">
    <div class="wrap">
      <h2>Thailand proposal: regional corridor programs backed by the speed evidence</h2>
      <p class="lead">
        The Thailand result is not "Central is bad" or "the Northeast is bad." The data separates into
        two policy questions. Outer regions show weaker compliance, while Central/Bangkok/East/West
        carries much larger observed speed exposure. ADB should fund both tracks, but for different reasons.
      </p>
      <div class="chart">{charts["thai_region"]}</div>
      <div class="callout">
        <strong>Thailand's key policy split</strong>
        Northeast, South, and North rank worse on average compliance. Central/Bangkok/East/West has
        better average compliance but 6.28 billion observed speed samples, far above the other regions.
        That means Central is an exposure-validation program, not a compliance-only program.
      </div>
      <table>
        <thead>
          <tr>
            <th>Question</th>
            <th>Best evidence lens</th>
            <th>What the Thailand data says</th>
            <th>Policy implication</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Where is speeding behavior worse?</td>
            <td>Average and sample-weighted % over limit</td>
            <td>Northeast, South, and North are weaker than Central/Bangkok/East/West.</td>
            <td>Use outer-region trunk and primary corridor programs.</td>
          </tr>
          <tr>
            <td>Where is exposure concentrated?</td>
            <td>Observed speed sample total</td>
            <td>Central/Bangkok/East/West has 6.28B observed samples.</td>
            <td>Match Central corridors against crash and fatality data before investment ranking.</td>
          </tr>
          <tr>
            <td>Which road class is the first screening target?</td>
            <td>Road-class % over limit and F85 gap</td>
            <td>Trunk roads show 40.4% average over-limit behavior and +10.8 km/h average F85 gap.</td>
            <td>Start with trunk-road speed management.</td>
          </tr>
          <tr>
            <td>Can we directly change speed limits?</td>
            <td>F85 gap, geometry, QA outliers, crash match</td>
            <td>The data identifies review candidates, not final changes.</td>
            <td>Run field validation before raising or lowering any limit.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <h2>Thailand: road-class and trunk evidence</h2>
      <p class="lead">
        This is the part that should not have been removed. The road-class numbers explain why trunk
        roads become the first national screening class, and the regional trunk chart explains where
        the first pilots should start.
      </p>
      <div class="chart">{charts["thai_road_class"]}</div>
      <div class="chart">{charts["thai_trunk"]}</div>
      <div class="grid">
        {card("Central/Bangkok/East/West", "Treat as a high-exposure corridor validation track. Better average compliance does not make it low priority because observed exposure is much larger.", "#2563eb")}
        {card("North and South", "Start trunk-road speed-management pilots. These regions show the weakest trunk-road compliance.", "#dc2626")}
        {card("Northeast", "Treat as a broader trunk-and-primary compliance program, not just a single road-class issue.", "#f59e0b")}
      </div>
    </div>
  </section>

  <section class="section soft">
    <div class="wrap">
      <h2>Thailand: what each region should investigate</h2>
      <p class="lead">
        The action matrix is the operational bridge from analysis to proposal. It does not say the
        road is dangerous. It says which type of agency review should happen next.
      </p>
      <div class="chart">{charts["thai_region_action"]}</div>
      <table>
        <thead>
          <tr>
            <th>Region</th>
            <th>Possible increase / QA</th>
            <th>Possible decrease</th>
            <th>Enforcement / speed management</th>
            <th>Road design change</th>
          </tr>
        </thead>
        <tbody>
          {thai_action_rows()}
        </tbody>
      </table>
      <div class="grid two">
        {card("What ADB can fund immediately", "A corridor validation program that chooses pilot corridors from these action buckets, then joins them with crash, fatality, motorcycle exposure, and traffic-volume data.", "#16a34a")}
        {card("What ADB should not fund from this alone", "A final speed-limit change list. The current dataset is strong for screening but incomplete for final statutory or engineering decisions.", "#dc2626")}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <h2>Thailand map: where the regional policy tracks start</h2>
      <p class="lead">
        This map is the spatial version of the Thailand proposal. The outer line color shows the regional
        work program. The inner line color shows road class. It is not saying every mapped road is dangerous;
        it is saying these are the corridors where each policy track should begin screening.
      </p>
      <div class="chart">{charts["thai_policy_map"]}</div>
    </div>
  </section>

  <section class="section soft">
    <div class="wrap">
      <h2>Thailand map: what kind of investigation each candidate needs</h2>
      <p class="lead">
        This is the operational map. Purple means possible increase or QA review, red means possible
        decrease review, amber means enforcement or speed management, and teal means road-design review.
        These are investigation buckets, not final decisions.
      </p>
      <div class="chart">{charts["thai_action_map"]}</div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <h2>Thailand: speed-limit credibility and QA outliers</h2>
      <p class="lead">
        This is where the proposal becomes more serious than a dashboard. Some roads point to enforcement;
        some point to design review; some point to possible speed-limit credibility or data QA issues.
        Those are different policy actions.
      </p>
      <div class="chart">{charts["thai_credibility"]}</div>
      <div class="callout">
        <strong>Important reading of the gray bar</strong>
        Northeast motorway has the highest F85 gap, but only 4 valid segments. It should be flagged,
        not overinterpreted. South trunk and North trunk are more defensible pilot targets because they
        have hundreds of valid segments and high F85 gaps.
      </div>
      <table>
        <thead>
          <tr>
            <th>Province</th>
            <th>Class</th>
            <th>Land use</th>
            <th>Posted limit</th>
            <th>Median gap</th>
            <th>F85 gap</th>
            <th>Sample</th>
          </tr>
        </thead>
        <tbody>
          {thai_qa_rows()}
        </tbody>
      </table>
      <div class="callout">
        <strong>How to read the 30 km/h cases</strong>
        These are urgent QA and field-review candidates, not automatic "most dangerous roads" and not
        automatic speed-limit increases. A 30 km/h limit with median speeds near 90-100 km/h could mean
        severe noncompliance, a miscoded limit, map-matching issues, or a special local road context.
      </div>
    </div>
  </section>

  <section class="section soft">
    <div class="wrap">
      <h2>Thailand: why high-exposure Central corridors stay in the proposal</h2>
      <p class="lead">
        The earlier analysis looked contradictory only if every chart was read as the same question.
        Central is not the weakest compliance region, but it dominates exposure-heavy inspection lists.
        That is why the correct recommendation is crash-data matching and corridor validation, not ignoring Central.
      </p>
      <div class="chart">{charts["thai_exposure"]}</div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <h2>Maharashtra proposal: road-class and land-use audit</h2>
      <p class="lead">
        Maharashtra should not be forced into Thailand's regional story. The dominant limit is 55 km/h,
        and the strongest signal is trunk-road operating speed exceeding posted limits, especially in
        rural contexts.
      </p>
      <div class="split">
        <div class="chart">{charts["maha_road"]}</div>
        <div class="chart">{charts["maha_land"]}</div>
      </div>
      <div class="grid">
        {card("Trunk roads first", "Trunk roads account for 260 enforcement / speed-management candidates and 84 possible increase / QA candidates.", "#16a34a")}
        {card("Rural and urban separate", "Rural candidates dominate enforcement and QA counts, but urban candidates need different safety interpretation because vulnerable-user exposure is likely different.", "#0891b2")}
        {card("Do not jump to raising limits", "Low limits with high speeds require credibility review, field checking, and crash matching before any recommendation.", "#7c3aed")}
      </div>
    </div>
  </section>

  <section class="section soft">
    <div class="wrap">
      <h2>Maharashtra maps: where the action candidates are</h2>
      <p class="lead">
        Maharashtra needs the same map treatment, but the story is different. The first map shows action
        buckets. The second keeps road-class outlines visible so trunk, primary, and motorway candidates
        can be interpreted separately.
      </p>
      <div class="chart">{charts["maha_action_map"]}</div>
      <div class="chart">{charts["maha_road_class_map"]}</div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <h2>Recommended ADB program</h2>
      <p class="lead">
        The value of the pilot is not a universal danger score. The value is a repeatable workflow that
        screens corridors, classifies the type of review needed, validates with crash and field data,
        and only then selects interventions.
      </p>
      <div class="chart">{charts["workflow"]}</div>
      <table>
        <thead>
          <tr><th>Phase</th><th>Purpose</th><th>Outputs</th></tr>
        </thead>
        <tbody>
          <tr>
            <td>1. Data validation and corridor screening</td>
            <td>Confirm speed-limit fields, map matching, geometry quality, and candidate classifications.</td>
            <td>Validated candidate list, QA log, priority maps, agency review dashboard.</td>
          </tr>
          <tr>
            <td>2. Crash and exposure integration</td>
            <td>Join speed findings with fatalities, serious injuries, motorcycle exposure, pedestrian exposure, traffic volume, access density, and land use.</td>
            <td>High-confidence corridors for enforcement, speed-limit review, or engineering intervention.</td>
          </tr>
          <tr>
            <td>3. Pilot interventions</td>
            <td>Deploy targeted enforcement, speed-limit review, or road-design treatments.</td>
            <td>Corridor pilots with defined before-and-after metrics.</td>
          </tr>
          <tr>
            <td>4. Monitoring and evaluation</td>
            <td>Measure F85 speed, median speed, percent over limit, crashes, fatalities, serious injuries, and compliance sustainability.</td>
            <td>Evidence for scaling, redesign, or stopping interventions.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <h2>Decision guardrails</h2>
      <p class="lead">
        This proposal deliberately avoids claiming that the speed data alone identifies the most dangerous
        roads. The speed data identifies where the next investigation should start.
      </p>
      <div class="grid two">
        {card("Required before final decisions", "Crash and fatality data, serious-injury records, traffic volume, motorcycle and pedestrian exposure, official speed-limit inventories, access density, and field inspection.", "#172033")}
        {card("What not to do", "Do not treat action counts as a crash-risk ranking. Do not raise or lower limits from probe-speed data alone. Do not copy Thailand's regional program into Maharashtra.", "#dc2626")}
      </div>
    </div>
  </section>

  <footer>
    <div class="wrap">
      Supporting files: risk_diagnosis_v1/curve_speed_limit_regional_policy_story.html,
      maharashtra_speed_limit_audit/maharashtra_speed_limit_action_audit_v2.html,
      thailand_maharashtra_shared_baseline_comparison.html.
    </div>
  </footer>
</body>
</html>
"""


def main() -> None:
    OUTPUT.write_text(render(include_plotlyjs=False), encoding="utf-8")
    OFFLINE_OUTPUT.write_text(render(include_plotlyjs=True), encoding="utf-8")
    print(f"Wrote {OUTPUT}")
    print(f"Wrote {OFFLINE_OUTPUT}")


if __name__ == "__main__":
    main()
