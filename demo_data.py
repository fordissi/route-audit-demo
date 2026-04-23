from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True, slots=True)
class DemoBundle:
    kpis: pd.DataFrame
    employee_summary: pd.DataFrame
    route_events: pd.DataFrame
    route_candidates: pd.DataFrame
    candidate_cards: pd.DataFrame
    monthly_comparison: pd.DataFrame
    process_steps: pd.DataFrame
    risk_cases: pd.DataFrame
    route_path_compare: pd.DataFrame
    route_confidence_case: pd.DataFrame
    mileage_breakdown_case: pd.DataFrame
    audit_case: pd.DataFrame
    hr_exception_case: pd.DataFrame
    api_ops_case: pd.DataFrame


def build_demo_bundle() -> DemoBundle:
    kpis = pd.DataFrame(
        [
            {"label": "月處理打卡筆數", "value": "4,268", "note": "模擬 42 位外勤同仁"},
            {"label": "可判讀拜訪事件", "value": "1,184", "note": "GPS 比對客戶 / 院所 / 員工住家"},
            {"label": "高風險出勤日", "value": "27", "note": "偏離拜訪軌跡或住家打卡"},
            {"label": "里程差異警示", "value": "11%", "note": "申請里程與預估里程差距過高"},
        ]
    )

    employee_summary = pd.DataFrame(
        [
            {"employee": "A01 林晨安", "region": "北區", "visits": 124, "risk_days": 2, "predicted_km": 814, "claimed_km": 836, "confidence": 0.91},
            {"employee": "A02 陳品妤", "region": "桃竹", "visits": 108, "risk_days": 1, "predicted_km": 692, "claimed_km": 705, "confidence": 0.89},
            {"employee": "A03 黃柏勳", "region": "中區", "visits": 97, "risk_days": 5, "predicted_km": 744, "claimed_km": 926, "confidence": 0.82},
            {"employee": "A04 吳若寧", "region": "南區", "visits": 113, "risk_days": 0, "predicted_km": 781, "claimed_km": 768, "confidence": 0.94},
            {"employee": "A05 張家豪", "region": "高屏", "visits": 88, "risk_days": 4, "predicted_km": 658, "claimed_km": 812, "confidence": 0.79},
            {"employee": "A06 李思穎", "region": "東區", "visits": 64, "risk_days": 1, "predicted_km": 592, "claimed_km": 601, "confidence": 0.87},
        ]
    )
    employee_summary["variance_km"] = employee_summary["claimed_km"] - employee_summary["predicted_km"]
    employee_summary["variance_pct"] = employee_summary["variance_km"] / employee_summary["claimed_km"]

    route_events = pd.DataFrame(
        [
            {"seq": 0, "visit_no": "", "time": "08:12", "event": "上班打卡", "location": "板橋住家附近", "category": "home", "lat": 25.0179, "lon": 121.4303, "km_from_home": 0.2},
            {"seq": 1, "visit_no": "1", "time": "09:06", "event": "抵達", "location": "亞東紀念醫院", "category": "hospital", "lat": 24.9988, "lon": 121.4526, "km_from_home": 2.0},
            {"seq": 2, "visit_no": "2", "time": "10:18", "event": "拜訪", "location": "板橋合康診所", "category": "clinic", "lat": 25.0138, "lon": 121.4754, "km_from_home": 4.5},
            {"seq": 3, "visit_no": "3", "time": "11:42", "event": "拜訪", "location": "宏恩藥局", "category": "pharmacy", "lat": 25.0379, "lon": 121.4932, "km_from_home": 7.1},
            {"seq": 4, "visit_no": "4", "time": "13:55", "event": "抵達", "location": "雙和醫院", "category": "hospital", "lat": 24.9994, "lon": 121.5078, "km_from_home": 8.4},
            {"seq": 5, "visit_no": "", "time": "17:58", "event": "下班打卡", "location": "住家附近", "category": "home", "lat": 25.0187, "lon": 121.4316, "km_from_home": 0.1},
        ]
    )

    route_candidates = pd.DataFrame(
        [
            {"time": "09:06", "gps_point": "亞東紀念醫院", "candidate": "亞東紀念醫院", "distance_m": 62, "type": "醫院", "confidence_label": "高"},
            {"time": "10:18", "gps_point": "板橋合康診所", "candidate": "板橋合康診所", "distance_m": 41, "type": "診所", "confidence_label": "高"},
            {"time": "11:42", "gps_point": "宏恩藥局", "candidate": "宏恩藥局", "distance_m": 28, "type": "藥局", "confidence_label": "高"},
            {"time": "13:55", "gps_point": "雙和醫院", "candidate": "衛生福利部雙和醫院", "distance_m": 87, "type": "醫院", "confidence_label": "高"},
            {"time": "17:58", "gps_point": "住家附近", "candidate": "員工住家", "distance_m": 16, "type": "住家", "confidence_label": "高"},
        ]
    )

    candidate_cards = pd.DataFrame(
        [
            {
                "visit_no": "1",
                "time": "09:06",
                "place_name": "亞東紀念醫院",
                "place_type": "醫院",
                "distance_m": 62,
                "reason": "GPS 點落在院區周邊，且與當日第一站醫院拜訪模式吻合",
                "confidence": "高",
                "nearest_client": "亞東醫療體系採購窗口 85m",
                "nearest_hospital": "亞東紀念醫院 62m",
                "other_candidates": "遠東聯合診所 180m、板橋仁安藥局 260m、雙和醫院台北門診 410m、宏福診所 480m、板橋康佑藥局 530m",
            },
            {
                "visit_no": "2",
                "time": "10:18",
                "place_name": "板橋合康診所",
                "place_type": "診所",
                "distance_m": 41,
                "reason": "與前後站形成順向移動，且最接近既有客戶主檔",
                "confidence": "高",
                "nearest_client": "板橋合康診所 41m",
                "nearest_hospital": "亞東紀念醫院 1.7km",
                "other_candidates": "板橋安泰診所 96m、板橋佑心藥局 133m、幸福聯合診所 165m、民安診所 212m、重慶藥局 254m",
            },
            {
                "visit_no": "3",
                "time": "11:42",
                "place_name": "宏恩藥局",
                "place_type": "藥局",
                "distance_m": 28,
                "reason": "GPS 點位與既有客戶主檔高度吻合，且位於兩家醫院之間的合理補貨路線",
                "confidence": "高",
                "nearest_client": "宏恩藥局 28m",
                "nearest_hospital": "臺北醫院板橋院區 1.2km",
                "other_candidates": "宏康藥局 74m、樂欣診所 102m、文化藥局 151m、板新耳鼻喉科 185m、泰和診所 231m",
            },
            {
                "visit_no": "4",
                "time": "13:55",
                "place_name": "衛生福利部雙和醫院",
                "place_type": "醫院",
                "distance_m": 87,
                "reason": "午後回到大型醫院客戶，搭配路網重建後可形成更合理的環狀拜訪動線",
                "confidence": "高",
                "nearest_client": "雙和醫院採購窗口 126m",
                "nearest_hospital": "衛生福利部雙和醫院 87m",
                "other_candidates": "雙和門診大樓 142m、永和康源藥局 214m、中和安平診所 255m、南勢角聯合診所 331m、連城藥局 402m",
            },
        ]
    )

    monthly_comparison = pd.DataFrame(
        [
            {"employee": "A01 林晨安", "predicted_km": 814, "claimed_km": 836},
            {"employee": "A02 陳品妤", "predicted_km": 692, "claimed_km": 705},
            {"employee": "A03 黃柏勳", "predicted_km": 744, "claimed_km": 926},
            {"employee": "A04 吳若寧", "predicted_km": 781, "claimed_km": 768},
            {"employee": "A05 張家豪", "predicted_km": 658, "claimed_km": 812},
            {"employee": "A06 李思穎", "predicted_km": 592, "claimed_km": 601},
        ]
    )
    monthly_comparison["variance_km"] = monthly_comparison["claimed_km"] - monthly_comparison["predicted_km"]

    process_steps = pd.DataFrame(
        [
            {"step": "1. 匯入 104 打卡匯出", "detail": "解析上下班打卡、GPS、異常申請與排班資訊"},
            {"step": "2. 建立地點底圖", "detail": "整合全台醫療院所、既有客戶與員工住家座標"},
            {"step": "3. 推測拜訪路徑", "detail": "以最近距離與規則推估實際拜訪順序與停靠點"},
            {"step": "4. 估算里程", "detail": "使用 route API 或離線估算換算公務里程"},
            {"step": "5. 輸出管理洞察", "detail": "比對月申請里程、標記高風險日、產出報表"},
        ]
    )

    risk_cases = pd.DataFrame(
        [
            {"case": "住家上下班打卡", "signal": "打卡點與住家距離 < 50m，且當日缺乏拜訪節點", "action": "提示主管複核"},
            {"case": "里程申請偏高", "signal": "申請里程高於系統預估 20% 以上", "action": "檢視當月路徑與申請依據"},
            {"case": "陌生點打卡", "signal": "與院所 / 客戶 / 住家都不接近", "action": "列入低信心事件"},
            {"case": "打卡與拜訪順序異常", "signal": "路徑無法形成合理往返順序", "action": "檢查漏打卡或補登"},
        ]
    )

    route_path_compare = pd.DataFrame(
        [
            {"mode": "GPS 直線推估", "distance_km": 15.1, "travel_min": 30, "explanation": "直接把節點用直線串起來，會忽略橋梁、單行道與道路限制"},
            {"mode": "Route API 行車路線", "distance_km": 22.8, "travel_min": 49, "explanation": "依道路網、轉向與可行車路徑重建，較接近實際拜訪動線"},
        ]
    )

    route_confidence_case = pd.DataFrame(
        [
            {
                "score": 0.91,
                "label": "高信心",
                "summary": "打卡點大多落在既有客戶或醫院 100 公尺內，且拜訪順序與路網重建結果一致。",
                "signals": "最近候選一致、既有客戶命中、拜訪順序合理、沒有陌生孤點。",
            }
        ]
    )

    mileage_breakdown_case = pd.DataFrame(
        [
            {"label": "Route API 總里程", "value": 22.8, "unit": "km", "note": "當日從出門到返家的全部行車路徑"},
            {"label": "基礎通勤扣除", "value": 6.0, "unit": "km", "note": "依員工通勤基準扣除往返通勤"},
            {"label": "核算公務里程", "value": 16.8, "unit": "km", "note": "作為月申請里程比對與財務核定基礎"},
            {"label": "預估行車時間", "value": 49.0, "unit": "分", "note": "依道路網推估的行車總時間"},
        ]
    )

    audit_case = pd.DataFrame(
        [
            {
                "light_label": "黃燈",
                "variance_pct": 0.18,
                "claimed_km": 19.9,
                "approved_km": 16.8,
                "per_diem": 250,
                "status": "需主管複核",
                "reason": "本月申請里程高於系統核算公務里程 18%，已超過綠燈門檻，但尚未達紅燈。",
            }
        ]
    )

    hr_exception_case = pd.DataFrame(
        [
            {
                "missing_punch_unprocessed": 1,
                "forget_punch_applications": 2,
                "actual_overtime": True,
                "summary": "本案例當日有 1 次未打卡待處理，並曾提出 2 次忘刷申請；同時出現實際加班標記，屬於需主管一起判讀的高關注日。",
            }
        ]
    )

    api_ops_case = pd.DataFrame(
        [
            {
                "estimated_calls": 684,
                "free_cap_remaining": 9316,
                "cache_hit_rate": 0.72,
                "diagnosis": "大多數重複路段可直接命中快取，能有效降低 API 成本與等待時間。",
            }
        ]
    )

    return DemoBundle(
        kpis=kpis,
        employee_summary=employee_summary,
        route_events=route_events,
        route_candidates=route_candidates,
        candidate_cards=candidate_cards,
        monthly_comparison=monthly_comparison,
        process_steps=process_steps,
        risk_cases=risk_cases,
        route_path_compare=route_path_compare,
        route_confidence_case=route_confidence_case,
        mileage_breakdown_case=mileage_breakdown_case,
        audit_case=audit_case,
        hr_exception_case=hr_exception_case,
        api_ops_case=api_ops_case,
    )
