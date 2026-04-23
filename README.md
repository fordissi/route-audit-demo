# Route Audit Demo

這是一個以外勤管理為場景的 HR analytics 展示專案。

系統將 GPS 打卡、醫療院所 open data、既有客戶資料與 Route API 的概念整合為一個可視化展示頁，協助主管快速理解：

- 外勤拜訪脈絡
- 公務里程合理性
- HR 與財務需要複核的異常訊號
- 導入後的管理價值與產品成熟度

本專案使用去識別化模擬資料，適合公開部署與展示，不包含正式員工或客戶資料。

## 本機執行

```bash
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run demo_app.py
```

## 首頁介紹文字

可直接放在 GitHub repo 或部署首頁：

> 把人工查核，變成可複核的管理流程。
>
> 這個展示版聚焦在三件事：還原外勤拜訪脈絡、拆解公務里程、整理 HR 與財務異常訊號，讓主管可以更快判讀單日案例與月度差異。

## 部署

部署方式請參考 [DEPLOYMENT.md](C:\Users\fordi\Documents\Codex\route-audit-demo\DEPLOYMENT.md)。
