# Data Analysis Portfolio

資料分析作品集，主要使用 **SQL、Python、Power BI** 進行資料處理、分析與視覺化，並結合統計分析、Machine Learning 與 LLM，實作完整的資料分析流程。

目前包含四個不同領域的專案：**電商分析、設備維運、半導體製程品質、財經新聞文字分析**。

---

## Projects

### 01. E-Commerce Data Analysis (Olist)

使用巴西 Olist 電商資料，分析營收變化、顧客留存、顧客價值與商品結構。

**Tools:** MySQL / Python / Power BI

- SQL 資料整合、中間表與分析 Mart
- Cohort Retention、RFM 顧客分群
- 營收成長與商品集中度分析
- Power BI 互動式儀表板

📁 [查看專案](./01.ECommerce_date_analyst/)

---

### 02. Equipment Maintenance Analysis

使用 Microsoft Azure Predictive Maintenance 資料，分析設備故障與感測器變化，建立故障風險預警。

**Tools:** MySQL / Python / Power BI

- 整合 Telemetry、Error、Maintenance、Failure 資料
- 分析設備故障前的感測器特徵
- Rule-Based 預警與 Precision / Recall / F1 評估
- Power BI 設備維運儀表板

📁 [查看專案](./02.Equipment_Maintenance_Analysis/)

---

### 03. Semiconductor Manufacturing Quality Analysis (SECOM)

使用 UCI SECOM 半導體製程資料，透過統計分析與 Machine Learning 比較品質風險篩檢效果。

**Tools:** Python / Statistics / Scikit-learn

- 高維度資料清理與類別不平衡分析
- Cohen's d 特徵差異與篩選
- Rule-Based 與多種 Machine Learning 模型比較
- 以 Recall ≥ 90% 為目標，評估 Inspection Rate

📁 [查看專案](./03.SECOM_Manufacturing_Quality_Analysis/)

---

### 04. Financial News Analysis with LLM

使用 Python 爬取公開財經新聞，透過 Gemini LLM 將文字轉換為結構化資料，並分析產業、公司與熱門議題。

**Tools:** Python / Web Scraping / MySQL / Gemini API / Power BI

- 網頁爬蟲、新聞清理、去重與 MySQL 儲存
- Gemini LLM 結構化擷取產業、公司及關鍵字
- 比較 V1 自由分類與 V2 GICS 產業分類
- 人工產業標準化與 Power BI 視覺化比較

📁 [查看專案](./04.Online_news_Analysis/)

---

## Technical Skills

**SQL / Database**  
MySQL、DBeaver、CTE、Window Functions、資料整合、分析 Mart

**Python / Data Analysis**  
Pandas、NumPy、Matplotlib、Scikit-learn、Web Scraping

**BI / Statistics**  
Power BI、Power Query、DAX、統計分析、Machine Learning

**LLM / Development**  
Gemini API、Pydantic、Structured Output、Git、GitHub