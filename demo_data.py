from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True, slots=True)
class DemoBundle:
    kpis: pd.DataFrame
    employees: pd.DataFrame
    monthly_trend: pd.DataFrame
    quadrant: pd.DataFrame
    route_events: pd.DataFrame
    places: pd.DataFrame
    risk_cases: pd.DataFrame
    risk_sources: pd.DataFrame
    talk_tracks: pd.DataFrame


MONTHS = ["2026-02", "2026-03", "2026-04", "2026-05"]


def _build_monthly_trend() -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    profiles = [
        {
            "employee": "A001 林北醫",
            "persona": "北區醫院業務",
            "estimated": [182, 196, 211, 224],
            "claimed": [190, 204, 220, 235],
            "risk_days": [1, 1, 2, 2],
            "risk_score": [10, 12, 15, 18],
            "review_score": [8, 10, 12, 14],
            "confidence": [0.92, 0.92, 0.91, 0.91],
        },
        {
            "employee": "B001 陳南院",
            "persona": "南區醫院業務",
            "estimated": [238, 254, 281, 318],
            "claimed": [292, 338, 411, 486],
            "risk_days": [2, 3, 5, 7],
            "risk_score": [24, 30, 36, 42],
            "review_score": [38, 52, 66, 76],
            "confidence": [0.84, 0.80, 0.76, 0.73],
        },
        {
            "employee": "C001 張北診",
            "persona": "北區診所藥局業務",
            "estimated": [132, 141, 139, 136],
            "claimed": [126, 132, 128, 122],
            "risk_days": [3, 4, 5, 6],
            "risk_score": [34, 42, 51, 58],
            "review_score": [18, 22, 25, 28],
            "confidence": [0.78, 0.73, 0.70, 0.68],
        },
        {
            "employee": "D001 吳中區",
            "persona": "中區混合業務",
            "estimated": [168, 182, 191, 205],
            "claimed": [188, 207, 222, 244],
            "risk_days": [1, 2, 2, 3],
            "risk_score": [16, 20, 24, 28],
            "review_score": [20, 26, 32, 38],
            "confidence": [0.87, 0.85, 0.83, 0.82],
        },
    ]
    for profile in profiles:
        for index, month in enumerate(MONTHS):
            estimate_km = profile["estimated"][index]
            claim_km = profile["claimed"][index]
            risk_score = profile["risk_score"][index]
            review_score = profile["review_score"][index]
            rows.append(
                {
                    "month": month,
                    "employee": profile["employee"],
                    "persona": profile["persona"],
                    "estimated_km": estimate_km,
                    "claimed_km": claim_km,
                    "variance_km": claim_km - estimate_km,
                    "variance_pct": (claim_km - estimate_km) / max(estimate_km, 1),
                    "risk_days": profile["risk_days"][index],
                    "risk_score": risk_score,
                    "review_score": review_score,
                    "priority_score": risk_score * 3 + review_score,
                    "confidence": profile["confidence"][index],
                }
            )
    return pd.DataFrame(rows)


def _build_employees(latest: pd.DataFrame) -> pd.DataFrame:
    employees = pd.DataFrame(
        [
            {
                "employee": "A001 林北醫",
                "persona": "北區醫院業務",
                "territory": "台北 / 新北 / 桃園",
                "primary_targets": "醫學中心、區域醫院、重點科別",
                "status": "正常基準",
                "story": "北區醫院行程穩定，申報里程與推估路線接近，可作為核銷容忍區間的展示基準。",
            },
            {
                "employee": "B001 陳南院",
                "persona": "南區醫院業務",
                "territory": "高雄 / 台南 / 屏東",
                "primary_targets": "大型醫院、跨縣市重點客戶",
                "status": "立即追查",
                "story": "南區醫院拜訪合理，但申報里程連續四個月放大，五月差異已達 168 km，適合展示趨勢預警。",
            },
            {
                "employee": "C001 張北診",
                "persona": "北區診所藥局業務",
                "territory": "新北 / 台北社區商圈",
                "primary_targets": "診所、藥局、社區通路",
                "status": "出勤佐證",
                "story": "診所藥局點位密集，里程不高但風險天數偏多，常出現住家附近打卡與工時不足訊號。",
            },
            {
                "employee": "D001 吳中區",
                "persona": "中區混合業務",
                "territory": "台中 / 彰化 / 南投",
                "primary_targets": "醫院、診所、藥局混合",
                "status": "持續觀察",
                "story": "中區跨型態拜訪較多，差異和風險分同步上升，但尚未超過立即追查門檻。",
            },
        ]
    )
    return employees.merge(
        latest[
            [
                "employee",
                "estimated_km",
                "claimed_km",
                "variance_km",
                "risk_days",
                "risk_score",
                "review_score",
                "priority_score",
                "confidence",
            ]
        ],
        on="employee",
        how="left",
    )


def _build_route_events() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"seq": 1, "time": "08:42", "employee": "A001 林北醫", "place": "台北住家打卡", "type": "home", "lat": 25.032, "lon": 121.565, "risk": "正常"},
            {"seq": 2, "time": "10:05", "employee": "A001 林北醫", "place": "台北榮民總醫院", "type": "hospital", "lat": 25.119, "lon": 121.521, "risk": "正常"},
            {"seq": 3, "time": "13:30", "employee": "A001 林北醫", "place": "新北亞東醫院", "type": "hospital", "lat": 24.997, "lon": 121.452, "risk": "正常"},
            {"seq": 4, "time": "17:58", "employee": "A001 林北醫", "place": "返回住家", "type": "home", "lat": 25.032, "lon": 121.565, "risk": "正常"},
            {"seq": 1, "time": "08:55", "employee": "B001 陳南院", "place": "高雄住家打卡", "type": "home", "lat": 22.666, "lon": 120.303, "risk": "正常"},
            {"seq": 2, "time": "10:18", "employee": "B001 陳南院", "place": "高雄長庚紀念醫院", "type": "hospital", "lat": 22.649, "lon": 120.356, "risk": "正常"},
            {"seq": 3, "time": "14:20", "employee": "B001 陳南院", "place": "屏東基督教醫院", "type": "hospital", "lat": 22.671, "lon": 120.489, "risk": "跨區里程偏高"},
            {"seq": 4, "time": "18:08", "employee": "B001 陳南院", "place": "返回住家", "type": "home", "lat": 22.666, "lon": 120.303, "risk": "正常"},
            {"seq": 1, "time": "09:02", "employee": "C001 張北診", "place": "板橋住家附近打卡", "type": "home", "lat": 25.016, "lon": 121.464, "risk": "居家附近"},
            {"seq": 2, "time": "10:12", "employee": "C001 張北診", "place": "新埔社區藥局", "type": "pharmacy", "lat": 25.014, "lon": 121.466, "risk": "正常"},
            {"seq": 3, "time": "11:40", "employee": "C001 張北診", "place": "板橋家庭診所", "type": "clinic", "lat": 25.018, "lon": 121.475, "risk": "正常"},
            {"seq": 4, "time": "16:10", "employee": "C001 張北診", "place": "江子翠藥局", "type": "pharmacy", "lat": 25.030, "lon": 121.472, "risk": "工時不足"},
            {"seq": 5, "time": "17:35", "employee": "C001 張北診", "place": "返回住家", "type": "home", "lat": 25.015, "lon": 121.463, "risk": "居家附近"},
        ]
    )


def build_demo_bundle() -> DemoBundle:
    monthly_trend = _build_monthly_trend()
    latest = monthly_trend.loc[monthly_trend["month"].eq("2026-05")].copy()

    employees = _build_employees(latest)
    quadrant = employees[
        [
            "employee",
            "persona",
            "status",
            "risk_score",
            "review_score",
            "priority_score",
            "confidence",
            "variance_km",
            "risk_days",
        ]
    ].copy()

    highest = quadrant.sort_values("priority_score", ascending=False).iloc[0]
    kpis = pd.DataFrame(
        [
            {"label": "展示月份", "value": "2026-05", "note": "四個月趨勢收斂到本月"},
            {"label": "待追查員工", "value": "2 人", "note": "B001 與 C001 優先排查"},
            {"label": "申報差異", "value": f"{int(latest['variance_km'].sum())} km", "note": "claimed - estimated"},
            {"label": "最高優先分", "value": f"{int(highest['priority_score'])}", "note": highest["employee"]},
        ]
    )

    places = pd.DataFrame(
        [
            {"region": "北區醫院", "example": "台北榮總、新北亞東、桃園長庚", "source": "公開醫療機構資料整理"},
            {"region": "南區醫院", "example": "高雄長庚、台南成大、屏東基督教", "source": "公開醫療機構資料整理"},
            {"region": "北區診所藥局", "example": "板橋家庭診所、新埔社區藥局、江子翠藥局", "source": "公開醫療機構資料整理"},
        ]
    )

    risk_cases = pd.DataFrame(
        [
            {
                "case": "申報里程快速拉高",
                "employee": "B001 陳南院",
                "signal": "2026-05 claimed_km 比 estimated_km 高 168 km，且四個月持續放大。",
                "action": "優先檢查跨區拜訪佐證、客戶約訪紀錄與主管覆核說明。",
            },
            {
                "case": "住家附近打卡",
                "employee": "C001 張北診",
                "signal": "多個風險日集中在住家附近，拜訪點位密集但工作時段偏短。",
                "action": "要求補充客戶拜訪紀錄、當日行程目的與核銷佐證。",
            },
            {
                "case": "正常基準線",
                "employee": "A001 林北醫",
                "signal": "申報與推估路線接近，風險天數低且信心分數高。",
                "action": "可作為稽核溝通時的正常樣態對照。",
            },
        ]
    )

    risk_sources = pd.DataFrame(
        [
            {"employee": "A001 林北醫", "source": "申報落差", "score": 8},
            {"employee": "A001 林北醫", "source": "居家附近", "score": 6},
            {"employee": "A001 林北醫", "source": "工時不足", "score": 4},
            {"employee": "B001 陳南院", "source": "申報落差", "score": 44},
            {"employee": "B001 陳南院", "source": "居家附近", "score": 8},
            {"employee": "B001 陳南院", "source": "工時不足", "score": 14},
            {"employee": "C001 張北診", "source": "申報落差", "score": 10},
            {"employee": "C001 張北診", "source": "居家附近", "score": 35},
            {"employee": "C001 張北診", "source": "工時不足", "score": 28},
            {"employee": "D001 吳中區", "source": "申報落差", "score": 20},
            {"employee": "D001 吳中區", "source": "居家附近", "score": 10},
            {"employee": "D001 吳中區", "source": "工時不足", "score": 12},
        ]
    )

    talk_tracks = pd.DataFrame(
        [
            {
                "employee": "B001 陳南院",
                "opening": "先確認南區跨縣市拜訪是否有臨時任務或主管指派。",
                "evidence": "比對醫院簽到、客戶約訪、油資與 GPS 里程。",
                "decision": "若佐證不足，列為高優先核銷覆核案件。",
            },
            {
                "employee": "C001 張北診",
                "opening": "先釐清住家附近打卡是否為第一站或返家前補登。",
                "evidence": "要求提供診所藥局拜訪名單、停留時間與回報紀錄。",
                "decision": "若多日重複，改由主管確認外勤工作安排。",
            },
            {
                "employee": "A001 林北醫",
                "opening": "以正常路線作為比較基準，說明系統不是只抓高里程。",
                "evidence": "展示申報里程、推估里程與實際拜訪點一致。",
                "decision": "保留為 demo 中的低風險對照樣本。",
            },
        ]
    )

    return DemoBundle(
        kpis=kpis,
        employees=employees,
        monthly_trend=monthly_trend,
        quadrant=quadrant,
        route_events=_build_route_events(),
        places=places,
        risk_cases=risk_cases,
        risk_sources=risk_sources,
        talk_tracks=talk_tracks,
    )
