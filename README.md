# Route Audit Demo

Standalone Streamlit demo for the Function Route Report / Route Audit concept.

This repository is the lightweight public demo app used for Streamlit Community Cloud deployment. It does not contain the full production pipeline or private HR source data. The demo uses synthetic monthly data to explain how GPS check-ins, public medical facility context, route estimation, mileage claims, and audit signals can be reviewed together.

## 中文說明

這個 repo 是 Function Route Report / Route Audit 的公開展示版，用於部署到 Streamlit Community Cloud。它不是正式版系統，也不包含真實員工、客戶、打卡或醫療院所內部資料。

展示版使用合成資料模擬四種外勤業務情境：北區醫院、南區醫院、北區診所藥局與中區混合通路。透過四個月的趨勢資料，可以示範系統如何把 GPS 打卡、院所拜訪脈絡、系統估算里程、員工申報里程與稽核訊號放在同一個畫面中檢視。

本 demo 的重點不是追蹤個人，而是把原本需要人工比對的外勤路徑與費用核銷流程，整理成可討論、可覆核、可追查優先順序的管理視角。

## Demo Scope

The current demo story covers four months of synthetic activity:

- `2026-02` to `2026-05`
- A001: north Taiwan hospital sales route
- B001: south Taiwan hospital sales route
- C001: north Taiwan clinic and pharmacy route
- D001: central Taiwan mixed channel route

The goal is to show trend-based audit review, not only a single-day map. For example, the demo highlights how a south-region employee's claimed mileage can drift upward over several months, and how a clinic/pharmacy route can repeatedly trigger near-home check-in review signals.

## App Pages

- **全業務趨勢**: Monthly claimed mileage, estimated mileage, variance, and risk-day ranking.
- **展示角色**: A/B/C/D route personas and their territory/customer type differences.
- **單日路徑**: Map-based route sequence for selected demo employees.
- **稽核說明**: How mileage variance, near-home check-ins, and normal baseline behavior are interpreted.

## 中文頁面導覽

- **全業務趨勢**：查看 2026-02 到 2026-05 的申報里程、系統估算里程、差異里程與風險天數排行。
- **展示角色**：說明 A/B/C/D 四種業務型態，包含北區醫院、南區醫院、北區診所藥局與中區混合通路。
- **單日路徑**：用地圖展示單日拜訪順序、拜訪點類型與可能的稽核訊號。
- **稽核說明**：說明申報差異、住家附近打卡、正常基準線等訊號如何協助 HR、財務與業務主管判讀。

## Files

- `demo_app.py`: Streamlit UI and charts.
- `demo_data.py`: Synthetic demo dataset builder.
- `requirements.txt`: Runtime dependencies for Streamlit Cloud.
- `.streamlit/config.toml`: Streamlit display/runtime configuration.
- `DEPLOYMENT.md`: Deployment notes.

## Run Locally

```bash
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run demo_app.py
```

On macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run demo_app.py
```

## Deployment

This repository is intended to deploy directly on Streamlit Community Cloud:

- Repository: `fordissi/route-audit-demo`
- Branch: `main`
- Main file path: `demo_app.py`
- Python: compatible with the Streamlit Cloud default runtime

No API keys or private credentials are required for this standalone demo.

## Relationship To The Production Repo

The full working project lives separately in the production repository. This demo repo is intentionally smaller and self-contained, so public deployment stays simple and safe. When the production project gains new report concepts, the demo can be updated here by translating those concepts into synthetic, non-private examples.
