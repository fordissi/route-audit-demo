from __future__ import annotations

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from demo_data import build_demo_bundle


st.set_page_config(page_title="Route Audit Demo", layout="wide")

ACCENT = "#f0b45b"
TEAL = "#2dd4bf"
RED = "#f87171"
INK = "#111827"
PANEL = "#182130"


st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at 85% 8%, rgba(45, 212, 191, .12), transparent 24rem),
            linear-gradient(145deg, #0d1118 0%, #151b24 48%, #10131a 100%);
        color: #edf2f7;
    }
    .block-container {
        max-width: 1320px;
        padding-top: 1rem;
        padding-bottom: 2.25rem;
    }
    h1, h2, h3, p, div, span, label {
        letter-spacing: 0 !important;
    }
    .command-hero {
        border: 1px solid rgba(240, 180, 91, .34);
        background: linear-gradient(135deg, rgba(24, 33, 48, .98), rgba(17, 24, 39, .94));
        border-radius: 8px;
        padding: 1.35rem 1.45rem;
        margin-bottom: .85rem;
        box-shadow: 0 18px 42px rgba(0, 0, 0, .25);
    }
    .command-hero h1 {
        color: #fff7ed !important;
        font-size: 2.35rem;
        line-height: 1.12;
        margin: .2rem 0 .45rem 0;
    }
    .command-hero p {
        color: #cbd5e1 !important;
        max-width: 920px;
        line-height: 1.65;
        margin: 0;
    }
    .eyebrow {
        color: #f0b45b !important;
        font-size: .76rem;
        font-weight: 800;
        text-transform: uppercase;
    }
    .signal-row {
        display: flex;
        gap: .55rem;
        flex-wrap: wrap;
        margin-top: .9rem;
    }
    .signal {
        border: 1px solid rgba(203, 213, 225, .18);
        background: rgba(15, 23, 42, .58);
        color: #e5e7eb !important;
        border-radius: 999px;
        padding: .28rem .72rem;
        font-size: .86rem;
        font-weight: 700;
    }
    .resume-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: .75rem;
        margin-top: 1rem;
    }
    .resume-note {
        border: 1px solid rgba(148, 163, 184, .22);
        border-radius: 8px;
        background: rgba(15, 23, 42, .62);
        padding: .8rem .9rem;
    }
    .resume-note strong {
        color: #fff7ed !important;
        display: block;
        margin-bottom: .25rem;
    }
    .resume-note span {
        color: #cbd5e1 !important;
        line-height: 1.5;
    }
    div[data-testid="stMetric"] {
        border: 1px solid rgba(148, 163, 184, .22);
        border-radius: 8px;
        background: rgba(24, 33, 48, .86);
        padding: .82rem .9rem;
        min-height: 106px;
    }
    [data-testid="stMetricLabel"] p {
        color: #94a3b8 !important;
        font-weight: 700;
    }
    [data-testid="stMetricValue"] {
        color: #fff7ed !important;
    }
    [data-testid="stMetricDelta"] {
        color: #2dd4bf !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: .65rem;
        border: 1px solid rgba(148, 163, 184, .26);
        border-radius: 8px;
        padding: .55rem;
        background: rgba(15, 23, 42, .78);
        margin-top: .8rem;
        margin-bottom: 1rem;
    }
    .stTabs [data-baseweb="tab"] {
        color: #f8fafc;
        border: 1px solid rgba(148, 163, 184, .28);
        background: rgba(30, 41, 59, .86);
        border-radius: 8px;
        padding: .78rem 1rem;
        min-height: 3rem;
        font-weight: 850;
        box-shadow: inset 0 -2px 0 rgba(148, 163, 184, .16);
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(240, 180, 91, .34), rgba(45, 212, 191, .16));
        border-color: rgba(240, 180, 91, .72);
        color: #fff7ed !important;
        box-shadow: 0 10px 22px rgba(0, 0, 0, .22), inset 0 -3px 0 #f0b45b;
    }
    .stTabs [data-baseweb="tab"]:hover {
        border-color: rgba(45, 212, 191, .62);
        background: rgba(45, 212, 191, .12);
    }
    .panel {
        border: 1px solid rgba(148, 163, 184, .2);
        border-radius: 8px;
        background: rgba(24, 33, 48, .82);
        padding: 1rem;
        margin-bottom: .85rem;
    }
    .story-card {
        border: 1px solid rgba(148, 163, 184, .22);
        border-radius: 8px;
        background: rgba(17, 24, 39, .84);
        padding: 1rem;
        min-height: 188px;
        margin-bottom: .8rem;
    }
    .story-card h3 {
        color: #fff7ed !important;
        font-size: 1.05rem;
        margin: .25rem 0 .45rem 0;
    }
    .story-card p, .muted {
        color: #cbd5e1 !important;
        line-height: 1.58;
    }
    .danger { border-left: 4px solid #f87171; }
    .warn { border-left: 4px solid #f0b45b; }
    .calm { border-left: 4px solid #2dd4bf; }
    .route-pill {
        display: inline-block;
        border: 1px solid rgba(45, 212, 191, .35);
        border-radius: 999px;
        color: #ccfbf1 !important;
        padding: .15rem .55rem;
        margin: 0 .28rem .35rem 0;
        font-size: .82rem;
        font-weight: 800;
    }
    div[data-testid="stDataFrame"] {
        border-radius: 8px;
        overflow: hidden;
    }
    @media (max-width: 900px) {
        .resume-grid {
            grid-template-columns: 1fr;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: .4rem;
        }
        .stTabs [data-baseweb="tab"] {
            padding: .65rem .72rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def plotly_theme(fig: go.Figure, height: int = 390) -> go.Figure:
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(17,24,39,.55)",
        font=dict(color="#e5e7eb"),
        height=height,
        margin=dict(l=24, r=18, t=34, b=24),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )
    fig.update_xaxes(gridcolor="rgba(148,163,184,.16)", zerolinecolor="rgba(148,163,184,.22)")
    fig.update_yaxes(gridcolor="rgba(148,163,184,.16)", zerolinecolor="rgba(148,163,184,.22)")
    return fig


def story_card(row: dict[str, object], tone: str) -> None:
    st.markdown(
        f"""
        <div class="story-card {tone}">
            <div class="eyebrow">{row["persona"]} · {row["status"]}</div>
            <h3>{row["employee"]}</h3>
            <p><strong>區域</strong>：{row["territory"]}</p>
            <p><strong>目標</strong>：{row["primary_targets"]}</p>
            <p>{row["story"]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


bundle = build_demo_bundle()
monthly = bundle.monthly_trend.copy()
employees = bundle.employees.copy()
quadrant = bundle.quadrant.copy()
route_events = bundle.route_events.copy()

st.markdown(
    """
    <section class="command-hero">
        <div class="eyebrow">Function Route Report · HR Portfolio Demo</div>
        <h1>給 HR 看的外勤稽核作品集</h1>
        <p>
            履歷展示專案非正式版：把外勤員工的 GPS 打卡(104企業大師匯出)、拜訪點位與車資申報
            轉成可追查的風險排序。HR 團隊可以先看誰需要優先覆核、為什麼被標記、下一步要問什麼，
            不必只靠人工抽查或單日異常判斷。適合非定點且客戶位置複雜的業務出勤管理。
        </p>
        <div class="signal-row">
            <span class="signal">HR 團隊常見痛點</span>
            <span class="signal">風險優先排序</span>
            <span class="signal">四個月趨勢追蹤</span>
            <span class="signal">關鍵技術說明</span>
        </div>
        <div class="resume-grid">
            <div class="resume-note">
                <strong>要解決的問題</strong>
                <span>外勤申報、GPS 打卡與拜訪紀錄分散，HR 很難快速判斷哪些案件值得優先追查。</span>
            </div>
            <div class="resume-note">
                <strong>HR 可以怎麼用</strong>
                <span>先看風險分與趨勢，再用路徑和話術準備員工訪談與主管覆核。</span>
            </div>
            <div class="resume-note">
                <strong>關鍵技術</strong>
                <span>Python / Streamlit / Pandas / Plotly，搭配路徑推估、風險分層與互動式資料視覺化。</span>
            </div>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

metric_cols = st.columns(4)
for col, row in zip(metric_cols, bundle.kpis.to_dict("records")):
    col.metric(row["label"], row["value"], row["note"])

tab_command, tab_quadrant, tab_trend, tab_route, tab_talk = st.tabs(
    ["01 問題總覽", "02 風險排序", "03 趨勢證據", "04 路徑檢視", "05 技術與話術"]
)

with tab_command:
    left, right = st.columns([1.18, 1.0])
    with left:
        fig = px.scatter(
            quadrant,
            x="review_score",
            y="risk_score",
            size="priority_score",
            color="status",
            text="employee",
            color_discrete_map={
                "立即追查": RED,
                "出勤佐證": ACCENT,
                "持續觀察": "#60a5fa",
                "正常基準": TEAL,
            },
            labels={
                "review_score": "開發/覆核分",
                "risk_score": "異常風險分",
                "priority_score": "綜合優先分",
                "status": "稽核狀態",
            },
        )
        fig.add_vline(x=40, line_dash="dot", line_color="rgba(240,180,91,.8)")
        fig.add_hline(y=35, line_dash="dot", line_color="rgba(240,180,91,.8)")
        fig.update_traces(textposition="top center", marker=dict(line=dict(width=1, color="#111827")))
        st.plotly_chart(plotly_theme(fig, 430), width="stretch")
    with right:
        source_fig = px.bar(
            bundle.risk_sources,
            x="score",
            y="employee",
            color="source",
            orientation="h",
            color_discrete_map={"申報落差": RED, "居家附近": ACCENT, "工時不足": TEAL},
            labels={"score": "來源分數", "employee": "業務", "source": "風險來源"},
        )
        st.plotly_chart(plotly_theme(source_fig, 430), width="stretch")

    st.markdown('<div class="eyebrow">展示重點：本月優先故事線</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    ordered = employees.set_index("employee").loc[["B001 陳南院", "C001 張北診", "A001 林北醫"]].reset_index()
    tones = ["danger", "warn", "calm"]
    for col, (_, row), tone in zip(cols, ordered.iterrows(), tones):
        with col:
            story_card(row.to_dict(), tone)

with tab_quadrant:
    st.markdown("### 2026-05 風險優先排序：讓 HR 先處理最值得追查的案件")
    sorted_quadrant = quadrant.sort_values("priority_score", ascending=False)
    rank_fig = px.bar(
        sorted_quadrant,
        x="priority_score",
        y="employee",
        color="status",
        orientation="h",
        text="priority_score",
        color_discrete_map={
            "立即追查": RED,
            "出勤佐證": ACCENT,
            "持續觀察": "#60a5fa",
            "正常基準": TEAL,
        },
        labels={"priority_score": "綜合優先分", "employee": "業務", "status": "狀態"},
    )
    st.plotly_chart(plotly_theme(rank_fig, 410), width="stretch")
    st.dataframe(
        sorted_quadrant.rename(
            columns={
                "employee": "業務",
                "persona": "角色",
                "status": "狀態",
                "risk_score": "異常風險分",
                "review_score": "開發/覆核分",
                "priority_score": "綜合優先分",
                "confidence": "信心分",
                "variance_km": "申報差異 km",
                "risk_days": "風險天數",
            }
        ),
        width="stretch",
        hide_index=True,
        column_config={
            "信心分": st.column_config.NumberColumn(format="%.0%%"),
            "申報差異 km": st.column_config.NumberColumn(format="%d km"),
        },
    )

with tab_trend:
    st.markdown("### 四個月趨勢：避免只看單日異常造成誤判")
    left, right = st.columns([1.1, 1.0])
    with left:
        variance_fig = px.line(
            monthly,
            x="month",
            y="variance_km",
            color="employee",
            markers=True,
            labels={"month": "月份", "variance_km": "申報差異 km", "employee": "業務"},
        )
        st.plotly_chart(plotly_theme(variance_fig, 400), width="stretch")
    with right:
        priority_fig = px.line(
            monthly,
            x="month",
            y="priority_score",
            color="employee",
            markers=True,
            labels={"month": "月份", "priority_score": "綜合優先分", "employee": "業務"},
        )
        st.plotly_chart(plotly_theme(priority_fig, 400), width="stretch")
    st.dataframe(
        monthly.sort_values(["month", "priority_score"], ascending=[True, False]).rename(
            columns={
                "month": "月份",
                "employee": "業務",
                "persona": "角色",
                "estimated_km": "推估里程",
                "claimed_km": "申報里程",
                "variance_km": "差異",
                "variance_pct": "差異率",
                "risk_days": "風險天數",
                "risk_score": "異常風險分",
                "review_score": "開發/覆核分",
                "priority_score": "綜合優先分",
                "confidence": "信心分",
            }
        ),
        width="stretch",
        hide_index=True,
        column_config={
            "推估里程": st.column_config.NumberColumn(format="%d km"),
            "申報里程": st.column_config.NumberColumn(format="%d km"),
            "差異": st.column_config.NumberColumn(format="%d km"),
            "差異率": st.column_config.NumberColumn(format="%.1%%"),
            "信心分": st.column_config.NumberColumn(format="%.0%%"),
        },
    )

with tab_route:
    st.markdown("### 單日路徑：把抽象分數轉成 HR 可追問的事實")
    selected_employee = st.selectbox(
        "選擇展示角色",
        options=route_events["employee"].drop_duplicates().tolist(),
        index=1,
    )
    selected_route = route_events.loc[route_events["employee"].eq(selected_employee)].copy()

    map_fig = go.Figure()
    marker_colors = selected_route["risk"].map(
        {"正常": TEAL, "跨區里程偏高": RED, "居家附近": ACCENT, "工時不足": "#60a5fa"}
    ).fillna(ACCENT)
    map_fig.add_trace(
        go.Scattermapbox(
            lat=selected_route["lat"],
            lon=selected_route["lon"],
            mode="lines+markers+text",
            text=selected_route["seq"].astype(str),
            textposition="top center",
            marker=dict(size=15, color=marker_colors, opacity=0.96),
            line=dict(width=4, color=ACCENT),
            hovertext=selected_route["time"] + " · " + selected_route["place"] + " · " + selected_route["risk"],
            hoverinfo="text",
            name="拜訪路徑",
        )
    )
    map_fig.update_layout(
        mapbox=dict(
            style="carto-darkmatter",
            center=dict(lat=float(selected_route["lat"].mean()), lon=float(selected_route["lon"].mean())),
            zoom=9,
        ),
        height=470,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(map_fig, width="stretch")

    cols = st.columns(2)
    for index, row in enumerate(selected_route.to_dict("records")):
        with cols[index % 2]:
            st.markdown(
                f"""
                <div class="story-card">
                    <span class="route-pill">#{row["seq"]}</span>
                    <span class="route-pill">{row["time"]}</span>
                    <h3>{row["place"]}</h3>
                    <p><strong>類型</strong>：{row["type"]}</p>
                    <p><strong>訊號</strong>：{row["risk"]}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

with tab_talk:
    st.markdown("### 稽核話術：從數字走到可執行處置")
    cols = st.columns(3)
    for index, row in enumerate(bundle.talk_tracks.to_dict("records")):
        tone = "danger" if row["employee"].startswith("B001") else "warn" if row["employee"].startswith("C001") else "calm"
        with cols[index % 3]:
            st.markdown(
                f"""
                <div class="story-card {tone}">
                    <div class="eyebrow">{row["employee"]}</div>
                    <h3>訪談順序</h3>
                    <p><strong>開場</strong>：{row["opening"]}</p>
                    <p><strong>佐證</strong>：{row["evidence"]}</p>
                    <p><strong>決策</strong>：{row["decision"]}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("### 公開醫療機構情境")
    st.dataframe(
        bundle.places.rename(columns={"region": "區域", "example": "展示點位", "source": "資料來源"}),
        width="stretch",
        hide_index=True,
    )
    st.markdown("### 追查案例")
    st.dataframe(
        bundle.risk_cases.rename(columns={"case": "案例", "employee": "業務", "signal": "系統訊號", "action": "建議處置"}),
        width="stretch",
        hide_index=True,
    )
    st.markdown("### 關鍵技術")
    st.markdown(
        """
        <div class="panel">
            <p class="muted">
                <strong>資料處理：</strong>使用 Pandas 整理外勤打卡、拜訪點位、推估里程與申報里程，建立可比較的月趨勢資料。
            </p>
            <p class="muted">
                <strong>風險模型：</strong>將申報落差、住家附近打卡、工時不足等訊號轉成異常風險分，再加上開發/覆核分形成綜合優先分。
            </p>
            <p class="muted">
                <strong>互動展示：</strong>以 Streamlit 和 Plotly 製作可操作的作品集 demo，包含象限圖、趨勢圖、地圖路徑與稽核訪談話術。
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.caption("Demo data is synthetic and designed for Streamlit deployment review. 醫療機構情境採公開資料整理後抽象化模擬。")
