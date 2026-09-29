# Data Analysis Portfolio

這個 Repository 用來整理我轉職 Data Analyst 過程中的練習與作品。

目前主要使用 **SQL（MySQL / DBeaver）、Python、Power BI**，透過公開資料練習從資料整理、分析到視覺化的完整流程，並逐步加入統計分析與 Machine Learning。

目前已完成三個專案，分別從電商、工業設備維運與半導體製程品質等不同方向進行分析。

---

## 專案列表

### 01. E-Commerce Data Analysis (Olist)

使用巴西 Olist 電商公開資料，練習從 SQL 資料整理、Python 分析到 Power BI 儀表板。

**主要內容**

* SQL：建立中間表與分析表，整理營收、留存、顧客分群與商品資料
* Python：營收趨勢、Cohort 留存、顧客價值與商品結構分析
* Power BI：製作總覽／顧客／商品共 3 頁互動式儀表板

**主要觀察**

* 營收成長主要來自新客，回購比例較低
* 約 97% 顧客僅消費一次，留存偏低
* 促銷月份可帶動營收與新客，但未看到留存同步改善
* 商品營收由多個品類共同支撐，沒有單一商品長期主導

📁 [查看專案](./01.ECommerce_data_analyst/)

---

### 02. Equipment Maintenance Analysis

使用 Microsoft Azure Predictive Maintenance 公開資料，分析工業設備的故障、維保與感測資料，並嘗試建立簡單的故障預警。

**主要內容**

* SQL：整合 telemetry、error、maintenance、failure、machine 等多張資料表，建立每日機台資料與分析表
* Python：分析機型、機台、零件故障分布，以及各零件故障前的 telemetry / error 變化
* Rule-Based 預警：依故障前觀察到的特徵建立簡單預警規則，並使用 Precision、Recall、F1-Score 評估
* Power BI：製作設備維運總覽與單一機台分析共 2 頁互動式儀表板

**主要觀察**

* model1、model2 的平均每台故障數較高，高故障機台也主要集中於這兩種機型
* comp2 的故障次數與故障／維保比相對較高
* comp1～comp4 在故障前呈現不同的 telemetry 與 error 變化
* Rule-Based 預警 Recall 約 86%～95%，但 Precision 約 36%～41%，目前較偏向降低漏報的基礎預警方式

📁 [查看專案](./02.Equipment_Maintenance_Analysis/)

---

### 03. Semiconductor Manufacturing Quality Analysis (SECOM)

使用 UCI SECOM 半導體製程資料進行品質分析，進一步練習統計分析、特徵篩選與 Machine Learning，並比較不同方法在製程品質篩檢上的效果。

**主要內容**

* 資料處理：檢查高維度資料、缺失值與類別不平衡問題
* 統計分析：使用 Cohen's d 比較 Pass / Fail 的特徵差異並進行特徵篩選
* Rule-Based：依差異較明顯的 Features 建立可解釋的篩檢規則
* Machine Learning：建立 Logistic Regression、Decision Tree、Random Forest 與 Gradient Boosting 等分類模型
* 模型評估：以 Recall 與 Inspection Rate 為主要指標，比較不同方法在降低漏判與檢查負擔之間的差異

**主要觀察**

* 在高類別不平衡資料中，Accuracy 無法單獨反映 Fail 的辨識效果
* 提高 Recall 通常也會增加 Inspection Rate，兩者之間需要取捨
* 在本次 Test set 中，較複雜的模型沒有明顯同時改善 Recall 與 Inspection Rate
* Rule-Based 在維持高 Recall 的情況下，仍具有具競爭力的篩檢效果
* Test set 僅有 21 個 Fail，因此單一樣本就會使 Recall 變動約 4.76 個百分點，模型差異需保守解讀

📁 [查看專案](./03.SECOM_Manufacturing_Quality_Analysis/)

---

## 使用技能

* **SQL（MySQL / DBeaver）**：資料清理、多表整合、CTE、Window Function、中間表與分析表
* **Python（Pandas / Matplotlib / Scikit-learn）**：資料處理、探索分析、視覺化、統計分析與基礎 Machine Learning
* **Power BI**：Power Query、基本 DAX、互動式儀表板
* **Git / GitHub**：專案版本管理與作品整理

---

## 目前方向

目前以 Data Analyst 為主要學習方向，持續練習：

**資料整理 → SQL 建表 → Python 分析 → Power BI 視覺化 → 統計／模型分析 → 結果解讀**

後續預計嘗試網路公開資料蒐集與 LLM 應用，練習將非結構化文字資料轉換為可分析的資料，持續擴充不同類型的資料分析實作。
