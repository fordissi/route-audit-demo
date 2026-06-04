from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True, slots=True)
class DemoBundle:
    kpis: pd.DataFrame
    employees: pd.DataFrame
    monthly_trend: pd.DataFrame
    route_events: pd.DataFrame
    places: pd.DataFrame
    risk_cases: pd.DataFrame


def _build_monthly_trend() -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    profiles = [
        ("A001 林北醫", "北區醫院業務", [182, 196, 211, 224], [190, 204, 220, 235], [1, 1, 2, 2]),
        ("B001 陳南院", "南區醫院業務", [238, 254, 281, 318], [292, 338, 411, 486], [2, 3, 5, 7]),
        ("C001 張北診", "北區診所藥局業務", [132, 141, 139, 136], [126, 132, 128, 122], [3, 4, 5, 6]),
        ("D001 吳中區", "中區混合業務", [168, 182, 191, 205], [188, 207, 222, 244], [1, 2, 2, 3]),
    ]
    months = ["2026-02", "2026-03", "2026-04", "2026-05"]
    for employee, persona, estimated, claimed, risk_days in profiles:
        for month, estimate_km, claim_km, risk_day_count in zip(months, estimated, claimed, risk_days):
            rows.append(
                {
                    "month": month,
                    "employee": employee,
                    "persona": persona,
                    "estimated_km": estimate_km,
                    "claimed_km": claim_km,
                    "variance_km": claim_km - estimate_km,
                    "variance_pct": (claim_km - estimate_km) / max(estimate_km, 1),
                    "risk_days": risk_day_count,
                }
            )
    return pd.DataFrame(rows)


def build_demo_bundle() -> DemoBundle:
    monthly_trend = _build_monthly_trend()
    latest = monthly_trend.loc[monthly_trend["month"].eq("2026-05")].copy()

    employees = pd.DataFrame(
        [
            {
                "employee": "A001 林北醫",
                "persona": "北區醫院業務",
                "territory": "台北 / 新北 / 桃園",
                "primary_targets": "醫學中心、區域醫院",
                "story": "穩定拜訪北部醫院，申報與系統估算接近，是正常基準線。",
            },
            {
                "employee": "B001 陳南院",
                "persona": "南區醫院業務",
                "territory": "高雄 / 台南 / 屏東",
                "primary_targets": "南部醫院與衛生所",
                "story": "南區移動距離較長，5 月申報里程快速升高，適合展示趨勢異常。",
            },
            {
                "employee": "C001 張北診",
                "persona": "北區診所藥局業務",
                "territory": "新北 / 台北基層通路",
                "primary_targets": "診所、藥局",
                "story": "拜訪點密集但距離短，偶爾出現住家附近打卡，適合展示風險原因。",
            },
            {
                "employee": "D001 吳中區",
                "persona": "中區混合業務",
                "territory": "台中 / 彰化 / 南投",
                "primary_targets": "醫院、診所、藥局",
                "story": "混合通路作為對照組，可看出不同區域與客戶型態的里程差異。",
            },
        ]
    ).merge(
        latest[["employee", "estimated_km", "claimed_km", "variance_km", "risk_days"]],
        on="employee",
        how="left",
    )

    kpis = pd.DataFrame(
        [
            {"label": "展示期間", "value": "4 個月", "note": "2026-02 到 2026-05"},
            {"label": "模擬業務", "value": "4 位", "note": "北醫、南院、北診藥局、中區混合"},
            {"label": "5 月申報差異", "value": f"{int(latest['variance_km'].sum())} km", "note": "全體 claimed - estimated"},
            {"label": "風險天數", "value": f"{int(latest['risk_days'].sum())} 天", "note": "用於展示追查優先序"},
        ]
    )

    route_events = pd.DataFrame(
        [
            {"seq": 1, "time": "08:42", "employee": "A001 林北醫", "place": "住家出發", "type": "home", "lat": 25.032, "lon": 121.565, "risk": "正常"},
            {"seq": 2, "time": "10:05", "employee": "A001 林北醫", "place": "台北醫學大學附設醫院", "type": "hospital", "lat": 25.026, "lon": 121.562, "risk": "正常"},
            {"seq": 3, "time": "13:30", "employee": "A001 林北醫", "place": "新北市立土城醫院", "type": "hospital", "lat": 24.973, "lon": 121.445, "risk": "正常"},
            {"seq": 4, "time": "17:58", "employee": "A001 林北醫", "place": "返家", "type": "home", "lat": 25.032, "lon": 121.565, "risk": "正常"},
            {"seq": 1, "time": "08:55", "employee": "B001 陳南院", "place": "住家出發", "type": "home", "lat": 22.666, "lon": 120.303, "risk": "正常"},
            {"seq": 2, "time": "10:18", "employee": "B001 陳南院", "place": "高雄榮民總醫院", "type": "hospital", "lat": 22.679, "lon": 120.322, "risk": "正常"},
            {"seq": 3, "time": "14:20", "employee": "B001 陳南院", "place": "屏東基督教醫院", "type": "hospital", "lat": 22.671, "lon": 120.489, "risk": "跨區距離偏高"},
            {"seq": 4, "time": "18:08", "employee": "B001 陳南院", "place": "返家", "type": "home", "lat": 22.666, "lon": 120.303, "risk": "正常"},
            {"seq": 1, "time": "09:02", "employee": "C001 張北診", "place": "住家附近打卡", "type": "home", "lat": 25.016, "lon": 121.464, "risk": "需覆核"},
            {"seq": 2, "time": "10:12", "employee": "C001 張北診", "place": "板橋文化路藥局", "type": "pharmacy", "lat": 25.014, "lon": 121.466, "risk": "正常"},
            {"seq": 3, "time": "11:40", "employee": "C001 張北診", "place": "新北民生診所", "type": "clinic", "lat": 25.018, "lon": 121.475, "risk": "正常"},
            {"seq": 4, "time": "17:35", "employee": "C001 張北診", "place": "返家", "type": "home", "lat": 25.015, "lon": 121.463, "risk": "需覆核"},
        ]
    )

    places = pd.DataFrame(
        [
            {"region": "北區醫院", "example": "台北醫學大學附設醫院、新北市立土城醫院、桃園長庚", "source": "公開院所資料整理"},
            {"region": "南區醫院", "example": "高雄榮總、屏東基督教醫院、台南新樓醫院", "source": "公開院所資料整理"},
            {"region": "北區診所藥局", "example": "板橋文化路藥局、新北民生診所、台北社區藥局", "source": "公開院所資料整理"},
        ]
    )

    risk_cases = pd.DataFrame(
        [
            {"case": "申報里程快速拉高", "employee": "B001 陳南院", "signal": "2026-05 claimed_km 比 estimated_km 高 168 km", "action": "優先檢查跨區拜訪是否有佐證"},
            {"case": "住家附近打卡", "employee": "C001 張北診", "signal": "外勤點與住家距離過近，且多次出現", "action": "要求補充客戶拜訪紀錄或主管覆核"},
            {"case": "正常基準線", "employee": "A001 林北醫", "signal": "申報與估算落差穩定，風險天數低", "action": "作為核銷寬容區間參考"},
        ]
    )

    return DemoBundle(
        kpis=kpis,
        employees=employees,
        monthly_trend=monthly_trend,
        route_events=route_events,
        places=places,
        risk_cases=risk_cases,
    )
