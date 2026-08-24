# Data Analysis Portfolio

這個 Repository 用來整理我轉職 Data Analyst 過程中的練習與作品。  
目前主要使用 **SQL（MySQL / DBeaver）+ Python + Power BI**，透過公開資料把分析流程實際跑過一遍。

作品會持續更新。第一個電商專案已走完 SQL → Python → BI；第二個改往工業設備維運方向。

---

## 專案列表

### 01. E-Commerce Data Analysis (Olist)

使用巴西 Olist 電商公開資料，練習從資料清理、SQL 建模到 Python 視覺化與 Power BI 儀表板。

**主要內容**
- SQL：建立中間表與分析表（營收、留存、顧客分群、商品）
- Python：資料驗證與圖表（營收、留存、客群、商品）
- Power BI：總覽／顧客／商品共 3 頁儀表板

**目前觀察**
- 營收成長主要來自新客，回購很少
- 約 97% 顧客為一次性消費，留存偏低
- 大促可拉高營收與新客，但不代表留存會變好
- 商品端較像多個穩定品類共同支撐，而非單一爆品長期主導

📁 [專案資料夾](./01.ECommerce_data_analyst/)

---

### 02. Equipment Failure & Maintenance Analysis

使用 Microsoft Azure Predictive Maintenance 資料，練習工業設備故障與維運分析（多表：感測、錯誤、維修、故障、設備主檔）。

**目前進度**
- SQL：已完成每日中間表與機台／月度分析表
- Python：進行中
- Power BI：進行中

**預定分析方向**
- 機台故障排行、零件故障結構
- 機型／機齡與故障關係
- 錯誤與故障的分布與趨勢

📁 [專案資料夾](./02.Equipment_Maintenance_Analysis/)

---

### 03. 生產效率／停機分析（規劃中）

後續預計延伸到產線效率、停機或 OEE 相關主題。

---

## 使用技能

- **SQL（MySQL + DBeaver）**：資料清理、中間表、分析表
- **Python（Pandas / Matplotlib 等）**：資料處理與視覺化
- **Power BI**：互動儀表板

---

## 目前方向

- 把分析流程跑熟：SQL → Python → BI
- 練習把結果寫成清楚、可理解的觀察
- 電商與工業各至少累積一個完整作品

---

## 備註

內容會不定期更新。  
若檔案無法開啟或路徑有調整，以各專案資料夾內的 README 為準。