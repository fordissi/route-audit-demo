from __future__ import annotations

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from demo_data import build_demo_bundle


st.set_page_config(page_title="HR Route Audit Demo", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at top right, rgba(14, 116, 144, 0.14), transparent 28%),
            radial-gradient(circle at bottom left, rgba(245, 158, 11, 0.10), transparent 26%),
            linear-gradient(180deg, #f4efe6 0%, #fbfaf7 45%, #eef4f4 100%);
        color: #172033;
    }
    .block-container {
        max-width: 1220px;
        padding-top: 1.2rem;
        padding-bottom: 2.2rem;
    }
    .hero {
        background: linear-gradient(135deg, #12324a 0%, #16535f 52%, #9a3412 100%);
        color: #fff8ef;
        border-radius: 28px;
        padding: 1.8rem 1.9rem;
        box-shadow: 0 22px 44px rgba(23, 32, 51, 0.18);
        margin-bottom: 1rem;
    }
    .hero h1,
    .hero p,
    .hero span,
    .hero div {
        color: #fff8ef !important;
    }
    .hero h1 {
        margin: 0 0 0.4rem 0;
        font-size: 2.2rem;
        line-height: 1.1;
    }
    .hero p {
        margin: 0.2rem 0;
        font-size: 1rem;
        line-height: 1.6;
    }
    .chip-row {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin-top: 0.9rem;
    }
    .chip {
        background: rgba(255, 248, 239, 0.14);
        border: 1px solid rgba(255, 248, 239, 0.22);
        border-radius: 999px;
        padding: 0.35rem 0.7rem;
        font-size: 0.85rem;
        font-weight: 700;
    }
    .story-card {
        background: rgba(255,255,255,0.84);
        border: 1px solid rgba(23,32,51,0.08);
        border-radius: 22px;
        padding: 1rem 1.05rem;
        box-shadow: 0 16px 32px rgba(23,32,51,0.06);
        margin-bottom: 0.9rem;
        color: #172033;
        min-height: 168px;
    }
    .story-card h3,
    .story-card p,
    .story-card strong,
    .story-card div {
        color: #172033 !important;
    }
    .story-card h3 {
        margin-top: 0;
        margin-bottom: 0.4rem;
        font-size: 1.05rem;
    }
    .eyebrow {
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-size: 0.76rem;
        font-weight: 800;
        color: #9a3412 !important;
        margin-bottom: 0.35rem;
    }
    .mini-note {
        color: #526070 !important;
        font-size: 0.92rem;
    }
    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.88);
        border: 1px solid rgba(23,32,51,0.08);
        border-radius: 18px;
        padding: 0.75rem 0.9rem;
        box-shadow: 0 12px 24px rgba(23,32,51,0.05);
    }
    div[data-testid="stMetric"] label,
    div[data-testid="stMetric"] [data-testid="stMetricLabel"],
    div[data-testid="stMetric"] [data-testid="stMetricValue"],
    div[data-testid="stMetric"] [data-testid="stMetricDelta"],
    div[data-testid="stMetric"] p,
    div[data-testid="stMetric"] div {
        color: #172033 !important;
    }
    div[data-testid="stDataFrame"] {
        background: rgba(255,255,255,0.88);
        border-radius: 18px;
        padding: 0.35rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.35rem;
    }
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.72);
        border-radius: 12px 12px 0 0;
        padding-left: 0.9rem;
        padding-right: 0.9rem;
        color: #465469;
    }
    .stTabs [aria-selected="true"] {
        color: #12324a !important;
        font-weight: 800;
    }
    .candidate-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.98) 0%, rgba(245,248,250,0.98) 100%);
        border: 1px solid rgba(23,32,51,0.08);
        border-left: 6px solid #0f766e;
        border-radius: 18px;
        padding: 0.95rem 1rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 12px 24px rgba(23,32,51,0.05);
        color: #172033;
    }
    .candidate-meta {
        color: #526070 !important;
        font-size: 0.92rem;
        margin-bottom: 0.35rem;
    }
    .candidate-tag {
        display: inline-block;
        border-radius: 999px;
        padding: 0.16rem 0.55rem;
        margin-right: 0.35rem;
        font-size: 0.82rem;
        font-weight: 800;
        background: #d9f7ea;
        color: #0f6a52 !important;
    }
    .compare-card {
        background: rgba(255,255,255,0.94);
        border: 1px solid rgba(23,32,51,0.08);
        border-radius: 20px;
        padding: 1rem;
        box-shadow: 0 12px 24px rgba(23,32,51,0.05);
        color: #172033;
        min-height: 152px;
    }
    .compare-number {
        font-size: 2rem;
        font-weight: 900;
        line-height: 1.05;
        color: #12324a !important;
        margin: 0.2rem 0 0.55rem 0;
    }
    .sequence-card {
        background: rgba(255,255,255,0.94);
        border: 1px solid rgba(23,32,51,0.08);
        border-radius: 18px;
        padding: 0.9rem 1rem;
        box-shadow: 0 12px 24px rgba(23,32,51,0.05);
        color: #172033;
        min-height: 162px;
    }
    .sequence-time {
        font-size: 0.9rem;
        font-weight: 800;
        color: #9a3412 !important;
        margin-bottom: 0.3rem;
    }
    .visit-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.98) 0%, rgba(246,249,251,0.98) 100%);
        border: 1px solid rgba(23,32,51,0.08);
        border-top: 5px solid #0f766e;
        border-radius: 20px;
        padding: 1rem;
        box-shadow: 0 12px 24px rgba(23,32,51,0.05);
        color: #172033;
        margin-bottom: 0.9rem;
        min-height: 330px;
    }
    .visit-no {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 1.9rem;
        height: 1.9rem;
        border-radius: 999px;
        background: #12324a;
        color: #fff8ef !important;
        font-weight: 900;
        margin-right: 0.45rem;
    }
    .visit-subtitle {
        color: #526070 !important;
        font-size: 0.92rem;
        margin-bottom: 0.45rem;
    }
    .visit-line {
        font-size: 0.94rem;
        line-height: 1.6;
        margin-bottom: 0.2rem;
    }
    .rank-list {
        margin: 0.3rem 0 0 1.15rem;
        padding: 0;
        color: #172033;
    }
    .rank-list li {
        margin-bottom: 0.18rem;
        line-height: 1.5;
    }
    .insight-card {
        background: rgba(255,255,255,0.96);
        border: 1px solid rgba(23,32,51,0.08);
        border-radius: 20px;
        padding: 1rem;
        box-shadow: 0 12px 24px rgba(23,32,51,0.05);
        margin-bottom: 0.85rem;
        color: #172033;
        min-height: 206px;
    }
    .insight-title {
        font-size: 1.02rem;
        font-weight: 800;
        margin-bottom: 0.35rem;
        color: #172033 !important;
    }
    .score-chip {
        display: inline-block;
        padding: 0.2rem 0.55rem;
        border-radius: 999px;
        font-size: 0.82rem;
        font-weight: 800;
        margin-bottom: 0.45rem;
    }
    .score-high {
        background: #d9f7ea;
        color: #0f6a52 !important;
    }
    .audit-yellow {
        background: #fef3c7;
        color: #9a3412 !important;
    }
    .breakdown-row {
        display: flex;
        justify-content: space-between;
        gap: 0.8rem;
        padding: 0.48rem 0;
        border-bottom: 1px solid rgba(23,32,51,0.08);
    }
    .breakdown-row:last-child {
        border-bottom: none;
    }
    .breakdown-value {
        font-weight: 900;
        color: #12324a !important;
        white-space: nowrap;
    }
    .cta-panel {
        background: linear-gradient(135deg, #fff8ef 0%, #eef7f6 100%);
        border: 1px solid rgba(18,50,74,0.12);
        border-radius: 24px;
        padding: 1.2rem 1.25rem;
        box-shadow: 0 18px 34px rgba(23,32,51,0.07);
        margin-top: 0.5rem;
    }
    .cta-title {
        font-size: 1.3rem;
        font-weight: 900;
        color: #12324a !important;
        margin-bottom: 0.35rem;
    }
    .cta-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.8rem;
        margin-top: 0.9rem;
    }
    .cta-item {
        background: rgba(255,255,255,0.82);
        border-radius: 16px;
        padding: 0.8rem 0.85rem;
        border: 1px solid rgba(18,50,74,0.08);
        min-height: 120px;
    }
    .cta-item strong {
        display: block;
        margin-bottom: 0.25rem;
        color: #12324a !important;
    }
    .brief-card {
        background: rgba(255,255,255,0.96);
        border: 1px solid rgba(23,32,51,0.08);
        border-radius: 22px;
        padding: 1rem 1.05rem;
        box-shadow: 0 14px 28px rgba(23,32,51,0.05);
        margin-bottom: 0.9rem;
        min-height: 220px;
    }
    .brief-card h3,
    .brief-card p,
    .brief-card div,
    .brief-card strong {
        color: #172033 !important;
    }
    .brief-list {
        margin: 0.45rem 0 0 1.15rem;
        padding: 0;
    }
    .brief-list li {
        margin-bottom: 0.3rem;
        line-height: 1.55;
    }
    .callout-strip {
        background: linear-gradient(135deg, #12324a 0%, #1b5560 100%);
        border-radius: 22px;
        padding: 1rem 1.1rem;
        color: #fff8ef;
        box-shadow: 0 16px 32px rgba(23,32,51,0.12);
        margin-bottom: 0.9rem;
    }
    .callout-strip h3,
    .callout-strip p,
    .callout-strip div {
        color: #fff8ef !important;
    }
    .stMarkdown, .stText, .stCaption, p, li, h1, h2, h3, h4 {
        color: #172033;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


bundle = build_demo_bundle()
employee_summary = bundle.employee_summary.copy()
monthly_comparison = bundle.monthly_comparison.copy()
route_events = bundle.route_events.copy()
route_candidates = bundle.route_candidates.copy()
candidate_cards = bundle.candidate_cards.copy()
route_path_compare = bundle.route_path_compare.copy()
route_confidence_case = bundle.route_confidence_case.copy()
mileage_breakdown_case = bundle.mileage_breakdown_case.copy()
audit_case = bundle.audit_case.copy()
hr_exception_case = bundle.hr_exception_case.copy()
api_ops_case = bundle.api_ops_case.copy()

st.markdown(
    """
    <section class="hero">
        <div class="eyebrow" style="color:#fed7aa !important;">HR Analytics Demo</div>
        <h1>業務打卡路徑稽核與里程比對</h1>
        <p>把 104 GPS 打卡、醫療院所 open data、既有客戶資料與 route API 串成一個管理分析工具，讓主管能更快掌握外勤拜訪脈絡、里程合理性與需要複核的異常訊號。</p>
        <div class="chip-row">
            <span class="chip">Demo 使用模擬資料</span>
            <span class="chip">外勤路徑判讀</span>
            <span class="chip">公務里程核算</span>
            <span class="chip">異常訊號整理</span>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

metric_cols = st.columns(4)
for column, row in zip(metric_cols, bundle.kpis.to_dict("records")):
    column.metric(row["label"], row["value"], row["note"])

tab_overview, tab_scenario, tab_management, tab_build, tab_rollout, tab_talking = st.tabs(
    ["為什麼需要這個系統", "情境展示", "管理視角", "專案亮點", "推行節奏", "說明口徑"]
)

with tab_overview:
    left, right = st.columns([1.0, 1.0])
    with left:
        st.markdown(
            """
            <div class="story-card">
                <div class="eyebrow">Business Pain</div>
                <h3>資料很多，但主管不容易快速判讀</h3>
                <p>外勤業務每天的出勤地點都可能不同。雖然 GPS 打卡資料完整存在，但若仍要逐筆點地圖確認，管理成本高，也不利於持續做月度追蹤。</p>
                <p class="mini-note">這個展示案例模擬藥品經銷商業務拜訪醫院、診所與藥局，因此需要同時看打卡位置、拜訪對象、里程與異常訊號。</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="story-card">
                <div class="eyebrow">Core Idea</div>
                <h3>把 GPS 打卡翻譯成主管看得懂的管理畫面</h3>
                <p>系統先把打卡點和院所、客戶、住家座標比對，再用道路路網估算公務里程，最後把單日案例、月里程差異與 HR 異常整理成可快速複核的管理視圖。</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        st.markdown("#### Demo 流程")
        for step in bundle.process_steps.to_dict("records"):
            st.markdown(
                f"""
                <div class="story-card">
                    <h3>{step["step"]}</h3>
                    <div class="mini-note">{step["detail"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.markdown(
        """
        <div class="cta-panel">
            <div class="eyebrow">Mock CTA</div>
            <div class="cta-title">把人工查核，變成可複核的管理流程</div>
            <div>這個展示版聚焦在三件事：還原外勤拜訪脈絡、拆解公務里程、把 HR 與財務訊號整理成主管能快速判讀的畫面。</div>
            <div class="cta-grid">
                <div class="cta-item">
                    <strong>先看單日案例</strong>
                    看系統怎麼從 GPS 打卡推測拜訪順序、候選客戶與拜訪脈絡。
                </div>
                <div class="cta-item">
                    <strong>再看管理訊號</strong>
                    同步檢視未打卡、忘刷申請、實際加班與財務燈號。
                </div>
                <div class="cta-item">
                    <strong>最後看產品成熟度</strong>
                    展示 Route API 快取、用量估算與成本控制思維。
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with tab_scenario:
    st.markdown(
        """
        <div class="story-card">
            <div class="eyebrow">Case Review</div>
            <h3>範例業務 A01 林晨安</h3>
            <p>這位業務一天內先後拜訪醫院、診所與藥局。系統會把 GPS 打卡點轉成可閱讀的拜訪順序、候選客戶與行車路徑，讓主管快速判讀當日出勤與里程是否合理。</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### 當日事件順序")
    sequence_cols = st.columns(3)
    for index, row in enumerate(route_events.to_dict("records")):
        with sequence_cols[index % 3]:
            badge = f"拜訪 {row['visit_no']}" if row["visit_no"] else "起訖點"
            st.markdown(
                f"""
                <div class="sequence-card">
                    <div class="sequence-time">{row["time"]} | {badge}</div>
                    <h3 style="margin-bottom:0.35rem;">{row["event"]}</h3>
                    <div style="font-weight:700; margin-bottom:0.3rem;">{row["location"]}</div>
                    <div class="mini-note">節點類型：{row["category"]}，距離住家約 {row["km_from_home"]:.1f} 公里</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("#### 當日地圖路徑")
    color_map = {
        "home": "#b45309",
        "hospital": "#0f766e",
        "clinic": "#1d4ed8",
        "pharmacy": "#7c3aed",
    }
    map_fig = go.Figure()
    map_fig.add_trace(
        go.Scattermapbox(
            lat=route_events["lat"],
            lon=route_events["lon"],
            mode="lines",
            line={"width": 3, "color": "#94a3b8"},
            name="GPS 直線推估",
            hoverinfo="skip",
            opacity=0.55,
        )
    )
    route_lat = [
        25.0179, 25.0158, 25.0104, 25.0058, 24.9988, 25.0034, 25.0101, 25.0166,
        25.0202, 25.0185, 25.0138, 25.0201, 25.0287, 25.0358, 25.0379, 25.0311,
        25.0207, 25.0105, 24.9994, 25.0032, 25.0107, 25.0148, 25.0187,
    ]
    route_lon = [
        121.4303, 121.4378, 121.4441, 121.4485, 121.4526, 121.4602, 121.4689, 121.4738,
        121.4749, 121.4752, 121.4754, 121.4817, 121.4871, 121.4914, 121.4932, 121.5006,
        121.5052, 121.5076, 121.5078, 121.4964, 121.4806, 121.4561, 121.4316,
    ]
    map_fig.add_trace(
        go.Scattermapbox(
            lat=route_lat,
            lon=route_lon,
            mode="lines",
            line={"width": 6, "color": "#12324a"},
            name="Route API 行車路線",
            hoverinfo="skip",
        )
    )
    numbered_visits = route_events.loc[route_events["visit_no"].astype(str) != ""].copy()
    label_offsets = {
        "1": (0.0045, 0.0028),
        "2": (0.0035, 0.0032),
        "3": (0.0036, 0.0026),
        "4": (0.0038, 0.0028),
    }
    numbered_visits["label_lat"] = numbered_visits.apply(
        lambda row: float(row["lat"]) + label_offsets.get(str(row["visit_no"]), (0.0035, 0.0025))[0],
        axis=1,
    )
    numbered_visits["label_lon"] = numbered_visits.apply(
        lambda row: float(row["lon"]) + label_offsets.get(str(row["visit_no"]), (0.0035, 0.0025))[1],
        axis=1,
    )
    for category, color in color_map.items():
        slice_df = route_events.loc[route_events["category"] == category]
        if slice_df.empty:
            continue
        labels = slice_df.apply(
            lambda row: f"{row['time']} {row['location']}" + (f" (#{row['visit_no']})" if row["visit_no"] else ""),
            axis=1,
        )
        map_fig.add_trace(
            go.Scattermapbox(
                lat=slice_df["lat"],
                lon=slice_df["lon"],
                mode="markers+text",
                marker={"size": 14, "color": color},
                text=labels,
                textposition="top right",
                name=category,
                hovertemplate="%{text}<extra></extra>",
            )
        )
    map_fig.add_trace(
        go.Scattermapbox(
            lat=numbered_visits["label_lat"],
            lon=numbered_visits["label_lon"],
            mode="markers",
            marker={
                "size": 30,
                "color": "#0f172a",
                "opacity": 0.98,
                "symbol": "square",
            },
            name="拜訪編號外框",
            hoverinfo="skip",
            showlegend=False,
        )
    )
    map_fig.add_trace(
        go.Scattermapbox(
            lat=numbered_visits["label_lat"],
            lon=numbered_visits["label_lon"],
            mode="markers",
            marker={
                "size": 24,
                "color": "#fff8ef",
                "opacity": 0.98,
                "symbol": "square",
            },
            name="拜訪編號底色",
            hoverinfo="skip",
            showlegend=False,
        )
    )
    map_fig.add_trace(
        go.Scattermapbox(
            lat=numbered_visits["label_lat"],
            lon=numbered_visits["label_lon"],
            mode="text",
            text=numbered_visits["visit_no"],
            textfont={"size": 16, "color": "#0f172a"},
            textposition="middle center",
            name="拜訪編號",
            hovertemplate="拜訪 %{text}<extra></extra>",
        )
    )
    map_fig.update_layout(
        mapbox={"style": "carto-positron", "zoom": 11, "center": {"lat": 25.013, "lon": 121.473}},
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        height=620,
        legend={"orientation": "h", "y": 1.02, "x": 0.01},
    )
    st.plotly_chart(map_fig, width="stretch")

    info_left, info_right = st.columns([1.1, 0.9])
    with info_left:
        st.markdown("#### 拜訪推測字卡")
        visit_cols = st.columns(2)
        for index, row in enumerate(candidate_cards.to_dict("records")):
            top_candidates_html = "".join(
                f"<li>{candidate.strip()}</li>"
                for candidate in str(row["other_candidates"]).split("、")
                if candidate.strip()
            )
            with visit_cols[index % 2]:
                st.markdown(
                    f"""
                    <div class="visit-card">
                        <div class="visit-subtitle"><span class="visit-no">{row["visit_no"]}</span>{row["time"]} | {row["place_type"]} | 距離 GPS {row["distance_m"]} 公尺</div>
                        <h3 style="margin-bottom:0.35rem;">{row["place_name"]}</h3>
                        <div style="margin-bottom:0.45rem;">
                            <span class="candidate-tag">信心 {row["confidence"]}</span>
                            <span class="candidate-tag" style="background:#e0ecff;color:#1d4ed8 !important;">最近候選</span>
                        </div>
                        <div class="visit-line"><strong>最近既有客戶：</strong>{row["nearest_client"]}</div>
                        <div class="visit-line"><strong>最近醫院：</strong>{row["nearest_hospital"]}</div>
                        <div class="visit-line"><strong>其他可能客戶 Top 5：</strong></div>
                        <ol class="rank-list">{top_candidates_html}</ol>
                        <div class="mini-note" style="margin-top:0.45rem;">{row["reason"]}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    with info_right:
        confidence_row = route_confidence_case.iloc[0]
        audit_row = audit_case.iloc[0]
        hr_row = hr_exception_case.iloc[0]
        st.markdown("#### Route API 如何把節點調整成可開車的路")
        for row in route_path_compare.to_dict("records"):
            st.markdown(
                f"""
                <div class="compare-card">
                    <div class="eyebrow">{row["mode"]}</div>
                    <div class="compare-number">{row["distance_km"]:.1f} km</div>
                    <div style="font-weight:800; margin-bottom:0.35rem;">預估行車時間 {int(row["travel_min"])} 分鐘</div>
                    <div class="mini-note">{row["explanation"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown(
            """
            <div class="story-card">
                <h3>這個區塊在看什麼？</h3>
                <p>同一組打卡節點，如果只把點與點直接相連，通常會低估真實里程；改用 Route API 後，系統會沿著實際道路、轉向與橋梁重建行車路線，因此更接近業務真正移動的情況。</p>
                <p class="mini-note">地圖上的拜訪編號對應到當日事件順序，方便主管快速回到單點案例做複核。</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">管理摘要</div>
                <div class="score-chip score-high">{confidence_row["label"]} {confidence_row["score"]:.0%}</div>
                <div class="visit-line"><strong>財務燈號：</strong>{audit_row["light_label"]}，{audit_row["status"]}</div>
                <div class="visit-line"><strong>未打卡待處理：</strong>{int(hr_row["missing_punch_unprocessed"])} 次</div>
                <div class="visit-line"><strong>忘刷申請 / 實際加班：</strong>{int(hr_row["forget_punch_applications"])} 次 / {"是" if bool(hr_row["actual_overtime"]) else "否"}</div>
                <div class="mini-note" style="margin-top:0.35rem;">{confidence_row["summary"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        breakdown_rows = "".join(
            f"""
            <div class="breakdown-row">
                <div>
                    <div style="font-weight:800;">{row["label"]}</div>
                    <div class="mini-note">{row["note"]}</div>
                </div>
                <div class="breakdown-value">{row["value"]:.1f} {row["unit"]}</div>
            </div>
            """
            for row in mileage_breakdown_case.to_dict("records")
        )
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">公務里程拆解</div>
                {breakdown_rows}
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.caption(f"判斷依據：{confidence_row['signals']}")
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">財務與 HR 複核說明</div>
                <div class="score-chip audit-yellow">{audit_row["light_label"]} | {audit_row["status"]}</div>
                <div class="visit-line"><strong>月申請里程：</strong>{audit_row["claimed_km"]:.1f} km</div>
                <div class="visit-line"><strong>核算公務里程：</strong>{audit_row["approved_km"]:.1f} km</div>
                <div class="visit-line"><strong>差異率：</strong>{audit_row["variance_pct"]:.0%}</div>
                <div class="visit-line"><strong>參考日當費：</strong>{int(audit_row["per_diem"])} 元</div>
                <div class="visit-line"><strong>HR 異常訊號：</strong>{hr_row["summary"]}</div>
                <div class="mini-note" style="margin-top:0.35rem;">{audit_row["reason"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        with st.expander("查看原始候選明細"):
            st.dataframe(
                route_candidates.rename(
                    columns={
                        "time": "時間",
                        "gps_point": "GPS 點位",
                        "candidate": "推測拜訪對象",
                        "distance_m": "距離(公尺)",
                        "type": "類型",
                        "confidence_label": "信心",
                    }
                ),
                width="stretch",
                hide_index=True,
            )

with tab_management:
    st.markdown("#### 月度里程比較")
    compare_fig = px.bar(
        monthly_comparison.melt(
            id_vars=["employee", "variance_km"],
            value_vars=["predicted_km", "claimed_km"],
            var_name="metric",
            value_name="km",
        ),
        x="employee",
        y="km",
        color="metric",
        barmode="group",
        color_discrete_map={"predicted_km": "#0f766e", "claimed_km": "#c2410c"},
        labels={"employee": "業務", "km": "公里數", "metric": "指標"},
    )
    compare_fig.update_layout(height=380, margin={"l": 10, "r": 10, "t": 10, "b": 10})
    st.plotly_chart(compare_fig, width="stretch")

    rank_cols = st.columns([1.0, 1.0])
    with rank_cols[0]:
        scatter_fig = px.scatter(
            employee_summary,
            x="predicted_km",
            y="claimed_km",
            size="risk_days",
            color="confidence",
            hover_name="employee",
            color_continuous_scale=["#f59e0b", "#0f766e"],
            labels={
                "predicted_km": "系統預估月公務里程",
                "claimed_km": "實際申請里程",
                "confidence": "平均信心",
                "risk_days": "高風險天數",
            },
        )
        scatter_fig.add_shape(
            type="line",
            x0=550,
            y0=550,
            x1=950,
            y1=950,
            line={"color": "#64748b", "width": 2},
        )
        scatter_fig.update_layout(height=400, margin={"l": 10, "r": 10, "t": 10, "b": 10})
        st.plotly_chart(scatter_fig, width="stretch")
    with rank_cols[1]:
        st.markdown("#### 高風險案例規則")
        for row in bundle.risk_cases.to_dict("records"):
            st.markdown(
                f"""
                <div class="story-card">
                    <h3>{row["case"]}</h3>
                    <div class="mini-note"><strong>訊號</strong>：{row["signal"]}</div>
                    <div class="mini-note"><strong>建議</strong>：{row["action"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    display_summary = employee_summary.rename(
        columns={
            "employee": "業務",
            "region": "區域",
            "visits": "拜訪次數",
            "risk_days": "高風險天數",
            "predicted_km": "預估里程",
            "claimed_km": "申請里程",
            "variance_km": "差異公里",
            "variance_pct": "差異率",
            "confidence": "平均信心",
        }
    )
    st.dataframe(
        display_summary,
        width="stretch",
        hide_index=True,
        column_config={
            "預估里程": st.column_config.NumberColumn(format="%.0f km"),
            "申請里程": st.column_config.NumberColumn(format="%.0f km"),
            "差異公里": st.column_config.NumberColumn(format="%.0f km"),
            "差異率": st.column_config.NumberColumn(format="%.1f%%"),
            "平均信心": st.column_config.NumberColumn(format="%.2f"),
        },
    )

with tab_build:
    ops_row = api_ops_case.iloc[0]
    left, right = st.columns(2)
    with left:
        st.markdown(
            """
            <div class="story-card">
                <div class="eyebrow">Decision Value</div>
                <h3>這個系統帶來的管理價值</h3>
                <p>這套工具不是為了增加管理摩擦，而是為了把原本分散、難查的出勤與里程資料，整理成主管可以快速複核的決策輔助畫面。</p>
                <p class="mini-note">實際使用上，主管可以先看高風險日與差異較大的月份，再回頭查看單日路徑，不需要每筆打卡都人工檢視。</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="story-card">
                <div class="eyebrow">Project Method</div>
                <h3>這個專案的實作重點</h3>
                <p>專案以真實商業場景為出發點，串接資料清洗、座標比對、地理推論、里程估算、BI 呈現與 Streamlit 產品化，將人工作業轉成可持續重複使用的分析流程。</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">Google Routes 快取與用量估算</div>
                <div class="visit-line"><strong>本月預估 API 呼叫：</strong>{int(ops_row["estimated_calls"])} 次</div>
                <div class="visit-line"><strong>Essentials 免費剩餘：</strong>{int(ops_row["free_cap_remaining"])} 次</div>
                <div class="visit-line"><strong>快取命中率：</strong>{ops_row["cache_hit_rate"]:.0%}</div>
                <div class="mini-note" style="margin-top:0.35rem;">{ops_row["diagnosis"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        st.markdown(
            """
            <div class="story-card">
                <div class="eyebrow">Architecture Snapshot</div>
                <h3>系統組成</h3>
                <p>104 打卡匯出 → 清洗與群組化 → 院所 / 客戶 / 住家比對 → 路由估算 → 月度里程比對 → 視覺化報表。</p>
                <p class="mini-note">正式版可接真實 CSV / XLSX；展示版則使用去識別化模擬資料，方便安全地公開部署與說明系統流程。</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="story-card">
                <div class="eyebrow">Next Step</div>
                <h3>後續可以延伸的方向</h3>
                <p>後續可以再加入更多模擬案例，例如住家打卡、陌生點打卡、里程差異過高等情境，讓使用者更快理解系統如何協助主管判讀異常。</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

with tab_rollout:
    st.markdown(
        """
        <div class="callout-strip">
            <div class="eyebrow" style="color:#fed7aa !important;">Rollout Brief</div>
            <h3>先對齊原則，再對外說明</h3>
            <p>這一頁適合在正式說明前，先用來確認推行原則、試行方式與配套，避免現場被問到關鍵問題時沒有一致口徑。</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    rollout_cols = st.columns(2)
    with rollout_cols[0]:
        st.markdown(
            """
            <div class="brief-card">
                <div class="eyebrow">推行目的</div>
                <h3>希望解決的是判讀成本，不是增加摩擦</h3>
                <ul class="brief-list">
                    <li>把人工點地圖改成有脈絡的輔助判讀。</li>
                    <li>降低主管、助理、財會逐筆確認的時間成本。</li>
                    <li>讓里程、拜訪脈絡與異常訊號有一致依據。</li>
                    <li>避免只看單點 GPS 造成誤判。</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="brief-card">
                <div class="eyebrow">先拍板</div>
                <h3>建議先確認的三件事</h3>
                <ul class="brief-list">
                    <li>是否設 1 到 2 個月試行期，不直接連動負向處理。</li>
                    <li>黃燈 / 紅燈案件是否保留人工複核與補充說明。</li>
                    <li>是否同步給出正向配套，而不是只有管理要求。</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with rollout_cols[1]:
        st.markdown(
            """
            <div class="brief-card">
                <div class="eyebrow">配套建議</div>
                <h3>若要降低反彈，最好同步確認</h3>
                <ul class="brief-list">
                    <li>里程或補貼核定時效是否可加快。</li>
                    <li>是否減少重複填報或手工說明。</li>
                    <li>是否可將認真跑點、跨區支援等正向表現納入可見度。</li>
                    <li>特殊情況如臨時支援、步行拜訪、忘刷補登，是否保留申覆機制。</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="brief-card">
                <div class="eyebrow">建議結論</div>
                <h3>比較穩的推法</h3>
                <ul class="brief-list">
                    <li>對內主軸用「公平、效率、可複核」，不要用「抓異常」。</li>
                    <li>先看單日案例與月度差異，再處理少數需要複核的事件。</li>
                    <li>工具作為輔助判讀，不作為單一裁量依據。</li>
                    <li>制度上線時，同步宣布試行期與補充說明流程。</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

with tab_talking:
    st.markdown(
        """
        <div class="callout-strip">
            <div class="eyebrow" style="color:#fed7aa !important;">導入說明</div>
            <h3>新的輔助檢視方式，想解決的是公平與效率</h3>
            <p>這套方式的目的，不是增加第一線負擔，而是把原本很花時間、也容易因為人工判讀產生落差的查核流程，整理成更有脈絡、更容易複核的方式。</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    talking_cols = st.columns(2)
    with talking_cols[0]:
        st.markdown(
            """
            <div class="brief-card">
                <div class="eyebrow">先說重點</div>
                <h3>這套方式的基本原則</h3>
                <ul class="brief-list">
                    <li>這不是只看單一打卡點，而是看整體拜訪脈絡。</li>
                    <li>這不是直接判定誰有問題，而是整理出需要複核的訊號。</li>
                    <li>這套方式的目標，是讓判斷更公平，也讓資料說明更完整。</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="brief-card">
                <div class="eyebrow">對大家的幫助</div>
                <h3>這樣做的好處</h3>
                <ul class="brief-list">
                    <li>認真跑點的人比較不容易被誤判。</li>
                    <li>若有臨時支援、補登、特殊路線，也比較能回到完整脈絡一起看。</li>
                    <li>里程與補貼核對有機會更透明、更快。</li>
                    <li>主管在判讀時會更有依據，不是只靠印象或逐筆人工點地圖。</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with talking_cols[1]:
        st.markdown(
            """
            <div class="brief-card">
                <div class="eyebrow">系統怎麼看</div>
                <h3>這套工具會一起整理哪些資訊</h3>
                <ul class="brief-list">
                    <li>當日拜訪順序與地圖路徑。</li>
                    <li>最近既有客戶、最近醫院與其他候選對象。</li>
                    <li>公務里程、通勤扣除與月申請里程差異。</li>
                    <li>未打卡、忘刷申請、實際加班等需要複核的訊號。</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="brief-card">
                <div class="eyebrow">最後說明</div>
                <h3>希望大家先理解的事</h3>
                <ul class="brief-list">
                    <li>工具的目的，是讓判斷更公平，不是增加第一線負擔。</li>
                    <li>系統標示的是需要複核的訊號，不是直接定論。</li>
                    <li>若有特殊情況，仍保留補充說明與人工判讀空間。</li>
                    <li>初期會持續依照實際工作情境調整，讓規則更貼近現場。</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.caption("此頁面使用模擬資料呈現正式版專案概念，方便安全地展示系統流程與分析結果。")
