from __future__ import annotations

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from demo_data import build_demo_bundle


st.set_page_config(page_title="Route Audit Demo", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background: #f7f8f5;
        color: #172033;
    }
    .block-container {
        max-width: 1240px;
        padding-top: 1.15rem;
        padding-bottom: 2.2rem;
    }
    .hero {
        background: #113044;
        color: #fffaf0;
        border-radius: 16px;
        padding: 1.65rem 1.75rem;
        margin-bottom: 1rem;
        box-shadow: 0 18px 36px rgba(17, 48, 68, 0.16);
    }
    .hero h1, .hero p, .hero div {
        color: #fffaf0 !important;
    }
    .hero h1 {
        margin: .25rem 0 .55rem 0;
        font-size: 2.25rem;
        line-height: 1.12;
    }
    .eyebrow {
        color: #9a5a1f !important;
        font-size: .78rem;
        font-weight: 800;
        letter-spacing: .08em;
        text-transform: uppercase;
    }
    .chip-row {
        display: flex;
        gap: .5rem;
        flex-wrap: wrap;
        margin-top: .85rem;
    }
    .chip {
        border: 1px solid rgba(255,250,240,.28);
        border-radius: 999px;
        padding: .32rem .68rem;
        font-weight: 700;
        font-size: .86rem;
    }
    .card {
        background: rgba(255,255,255,.92);
        border: 1px solid rgba(23,32,51,.08);
        border-radius: 12px;
        padding: 1rem 1.05rem;
        box-shadow: 0 10px 24px rgba(23,32,51,.05);
        margin-bottom: .85rem;
        min-height: 145px;
    }
    .card h3 {
        margin: .25rem 0 .35rem 0;
        color: #172033 !important;
        font-size: 1.08rem;
    }
    .muted {
        color: #526070 !important;
        line-height: 1.6;
    }
    div[data-testid="stMetric"] {
        background: rgba(255,255,255,.95);
        border: 1px solid rgba(23,32,51,.08);
        border-radius: 12px;
        padding: .75rem .9rem;
        box-shadow: 0 10px 22px rgba(23,32,51,.05);
        min-height: 104px;
    }
    [data-testid="stMetricLabel"] p,
    [data-testid="stMetricValue"],
    [data-testid="stMetricDelta"] {
        color: #172033 !important;
        white-space: normal !important;
    }
    div[data-testid="stDataFrame"] {
        background: rgba(255,255,255,.94);
        border-radius: 12px;
        padding: .35rem;
    }
    .risk {
        border-left: 5px solid #c2410c;
    }
    .ok {
        border-left: 5px solid #0f766e;
    }
    .route-note {
        display: inline-block;
        border-radius: 999px;
        background: #e8f2ef;
        color: #0f5f51 !important;
        padding: .18rem .55rem;
        font-weight: 800;
        margin-right: .35rem;
        font-size: .84rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


bundle = build_demo_bundle()
monthly = bundle.monthly_trend.copy()
employees = bundle.employees.copy()
route_events = bundle.route_events.copy()

st.markdown(
    """
    <section class="hero">
        <div class="eyebrow" style="color:#f6c28b !important;">Function Route Report Demo</div>
        <h1>外勤路徑與油資稽核展示版</h1>
        <p>
            這份 demo 使用 2026-02 到 2026-05 的模擬資料，呈現北區醫院、南區醫院、
            北區診所藥局與中區混合通路的拜訪型態差異。重點是讓管理者看見趨勢、
            申報差異與追查優先順序，而不是只看單日單點。
        </p>
        <div class="chip-row">
            <span class="chip">多月趨勢</span>
            <span class="chip">區域角色差異</span>
            <span class="chip">公開院所資料情境</span>
            <span class="chip">Route API 稽核邏輯</span>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

metric_cols = st.columns(4)
for col, row in zip(metric_cols, bundle.kpis.to_dict("records")):
    col.metric(row["label"], row["value"], row["note"])

tab_overview, tab_roles, tab_route, tab_risk = st.tabs(
    ["全業務趨勢", "展示角色", "單日路徑", "稽核說明"]
)

with tab_overview:
    st.subheader("全業務月趨勢")
    chart_left, chart_right = st.columns([1.35, 1.0])
    with chart_left:
        trend_fig = px.line(
            monthly,
            x="month",
            y="claimed_km",
            color="employee",
            markers=True,
            labels={"month": "月份", "claimed_km": "申報里程(km)", "employee": "業務"},
        )
        trend_fig.update_layout(height=380, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(trend_fig, width="stretch")
    with chart_right:
        variance_fig = px.bar(
            monthly,
            x="month",
            y="variance_km",
            color="employee",
            barmode="group",
            labels={"month": "月份", "variance_km": "申報差異(km)", "employee": "業務"},
        )
        variance_fig.update_layout(height=380, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(variance_fig, width="stretch")

    latest = monthly.loc[monthly["month"].eq("2026-05")].sort_values("variance_km", ascending=False)
    st.markdown("#### 2026-05 追查優先順序")
    st.dataframe(
        latest.rename(
            columns={
                "employee": "業務",
                "persona": "展示角色",
                "estimated_km": "系統估算里程",
                "claimed_km": "申報里程",
                "variance_km": "差異里程",
                "variance_pct": "差異率",
                "risk_days": "風險天數",
            }
        ),
        width="stretch",
        hide_index=True,
        column_config={
            "系統估算里程": st.column_config.NumberColumn(format="%.0f km"),
            "申報里程": st.column_config.NumberColumn(format="%.0f km"),
            "差異里程": st.column_config.NumberColumn(format="%.0f km"),
            "差異率": st.column_config.NumberColumn(format="%.1%"),
        },
    )

with tab_roles:
    st.subheader("模擬角色與院所情境")
    role_cols = st.columns(2)
    for index, row in enumerate(employees.to_dict("records")):
        with role_cols[index % 2]:
            css = "risk" if row["employee"].startswith(("B001", "C001")) else "ok"
            st.markdown(
                f"""
                <div class="card {css}">
                    <div class="eyebrow">{row["persona"]}</div>
                    <h3>{row["employee"]}</h3>
                    <div class="muted"><strong>區域：</strong>{row["territory"]}</div>
                    <div class="muted"><strong>主要客戶：</strong>{row["primary_targets"]}</div>
                    <div class="muted" style="margin-top:.35rem;">{row["story"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.markdown("#### 公開院所資料模擬來源")
    st.dataframe(
        bundle.places.rename(columns={"region": "區域", "example": "示例院所", "source": "資料語境"}),
        width="stretch",
        hide_index=True,
    )

with tab_route:
    st.subheader("單日路徑與拜訪點")
    selected_employee = st.selectbox(
        "選擇展示路線",
        options=route_events["employee"].drop_duplicates().tolist(),
        index=1,
    )
    selected_route = route_events.loc[route_events["employee"].eq(selected_employee)].copy()

    map_fig = go.Figure()
    map_fig.add_trace(
        go.Scattermapbox(
            lat=selected_route["lat"],
            lon=selected_route["lon"],
            mode="lines+markers+text",
            text=selected_route["seq"].astype(str),
            textposition="top center",
            marker=dict(size=13, color="#113044"),
            line=dict(width=4, color="#0f766e"),
            hovertext=selected_route["time"] + " " + selected_route["place"] + " | " + selected_route["risk"],
            hoverinfo="text",
            name="拜訪順序",
        )
    )
    map_fig.update_layout(
        mapbox=dict(
            style="carto-positron",
            center=dict(lat=float(selected_route["lat"].mean()), lon=float(selected_route["lon"].mean())),
            zoom=9,
        ),
        height=470,
        margin=dict(l=0, r=0, t=0, b=0),
    )
    st.plotly_chart(map_fig, width="stretch")

    event_cols = st.columns(2)
    for index, row in enumerate(selected_route.to_dict("records")):
        with event_cols[index % 2]:
            st.markdown(
                f"""
                <div class="card">
                    <span class="route-note">#{row["seq"]}</span>
                    <span class="route-note">{row["time"]}</span>
                    <h3>{row["place"]}</h3>
                    <div class="muted"><strong>類型：</strong>{row["type"]}</div>
                    <div class="muted"><strong>稽核訊號：</strong>{row["risk"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

with tab_risk:
    st.subheader("稽核解讀")
    risk_cols = st.columns(3)
    for index, row in enumerate(bundle.risk_cases.to_dict("records")):
        with risk_cols[index % 3]:
            st.markdown(
                f"""
                <div class="card risk">
                    <div class="eyebrow">{row["employee"]}</div>
                    <h3>{row["case"]}</h3>
                    <div class="muted"><strong>訊號：</strong>{row["signal"]}</div>
                    <div class="muted" style="margin-top:.35rem;"><strong>建議：</strong>{row["action"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        """
        <div class="card ok">
            <div class="eyebrow">Demo narrative</div>
            <h3>為什麼要拉長模擬期間？</h3>
            <div class="muted">
                單日路線能說明 GPS 與院所匹配，但管理決策更需要月趨勢。當 B001 的南區醫院路線
                在 5 月申報差異突然擴大，或 C001 的北區診所藥局路線持續出現住家附近打卡，
                系統就能把「偶發事件」和「行為趨勢」分開，讓 HR、財務與業務主管用同一份資料討論。
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.caption("Demo data is synthetic and designed for Streamlit deployment review.")
