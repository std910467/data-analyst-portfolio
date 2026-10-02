# Data Analysis Portfolio

資料分析作品集，主要使用 **SQL、Python、Power BI** 進行資料處理、分析與視覺化，並透過不同領域的公開資料，實作從資料整理、探索分析到結果呈現的完整分析流程。

目前作品涵蓋 **電商分析、設備維運、半導體製程品質**，並持續擴充網路資料蒐集與非結構化文字分析等應用。

---

## Projects

### 01. E-Commerce Data Analysis (Olist)

以巴西 Olist 電商資料分析營收、顧客留存、顧客價值與商品結構。

**Tools:** MySQL / Python / Power BI

* 建立 SQL 中間表與分析 Mart
* Cohort Retention 與顧客價值分群
* 營收與商品結構分析
* Power BI 互動式儀表板

📁 [查看專案](./01.ECommerce_date_analyst/)

---

### 02. Equipment Maintenance Analysis

使用 Microsoft Azure Predictive Maintenance 資料，分析設備故障、維保與感測器變化，並建立基礎故障預警。

**Tools:** MySQL / Python / Power BI

* 整合設備、Telemetry、Error、Maintenance、Failure 資料
* 分析設備故障前的特徵變化
* 建立 Rule-Based 預警並以 Precision / Recall / F1 評估
* Power BI 設備維運儀表板

📁 [查看專案](./02.Equipment_Maintenance_Analysis/)

---

### 03. Semiconductor Manufacturing Quality Analysis (SECOM)

使用 UCI SECOM 半導體製程資料，分析 Pass / Fail 特徵差異，並比較 Rule-Based 與 Machine Learning 的品質篩檢效果。

**Tools:** Python / Statistics / Scikit-learn

* 高維度資料與類別不平衡處理
* Cohen's d 特徵差異分析
* Rule-Based 品質篩檢
* Logistic Regression、Decision Tree、Random Forest、Gradient Boosting
* 以 Recall 與 Inspection Rate 評估模型

📁 [查看專案](./03.SECOM_Manufacturing_Quality_Analysis/)

---

### 04. Financial News Analysis with LLM 🚧

以公開財經新聞建立資料蒐集與文字分析流程，目前持續開發中。

**Tools:** Python / Web Scraping / MySQL

目前已完成：

* Requests / BeautifulSoup 財經新聞爬蟲
* 新聞正文清理與時間格式處理
* URL 去重與 MySQL 資料儲存
* 重複資料寫入防護

後續將加入 LLM 進行新聞內容結構化分析。

📁 [查看專案](./04.Online_news_Analysis/)

---

## Technical Skills

**SQL / Database**
MySQL、DBeaver、CTE、Window Function、資料整合、分析 Mart

**Python**
Pandas、Matplotlib、Scikit-learn、Web Scraping、資料處理與分析

**BI / Analytics**
Power BI、Power Query、DAX、統計分析、Machine Learning

**Development**
Git、GitHub
