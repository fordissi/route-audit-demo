# Route Audit Demo

Standalone Streamlit demo for the Function Route Report / Route Audit concept.

This repository is the lightweight public demo app used for Streamlit Community Cloud deployment. It does not contain the full production pipeline or private HR source data. The demo uses synthetic monthly data to explain how GPS check-ins, public medical facility context, route estimation, mileage claims, and audit signals can be reviewed together.

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
