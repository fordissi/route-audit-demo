# Deployment

## 推薦方式

最簡單的部署方式是使用 Streamlit Community Cloud。

原因：

- 原生支援 `streamlit`
- 適合公開展示 demo
- 不需要另外建 API 或資料庫

## Streamlit Community Cloud

1. 將此資料夾推到獨立的 GitHub repository。
2. 登入 Streamlit Community Cloud。
3. 建立新 app。
4. Repository 指向這個 repo。
5. Main file path 設定為 `demo_app.py`。
6. Python version 選 `3.13`。
7. Deploy。

## 建議設定

- Python 版本：`3.13`
- Main file：`demo_app.py`
- Branch：`main`
- App visibility：依你的公開需求選擇 Public 或 Unlisted

## 上線前檢查

- `demo_app.py` 可在本機正常執行
- `requirements.txt` 僅保留 demo 所需依賴
- `.streamlit/config.toml` 已存在
- 專案內不含真實客戶或員工資料

## 此 repo 已包含

- `demo_app.py`：Streamlit 入口
- `demo_data.py`：模擬資料
- `requirements.txt`：最小部署依賴
- `.streamlit/config.toml`：Streamlit Cloud 友善設定
- `README.md`：專案介紹

## 建議上線名稱

- `Route Audit Demo`
- `HR Route Audit Demo`
- `Field Visit Audit Demo`

## 公開頁介紹短文

> 這是一個以外勤管理為場景的 HR analytics 展示專案。系統將 GPS 打卡、醫療院所 open data、既有客戶資料與 Route API 概念串接，協助主管快速理解外勤拜訪脈絡、公務里程合理性，以及需要複核的 HR 與財務異常訊號。
