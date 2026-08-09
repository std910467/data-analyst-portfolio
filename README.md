# data-analyst-portfolio
data-analyst-portfolio

先用放入基本假資料，測試。
找到電商資料，加進來做測試
加入第一個專案

先做一些紀錄 後面再修
## 01.ECommerce_date_analyst
🔹 分析主軸
    營收成長（Revenue）
    顧客留存（Retention / Cohort）
    顧客價值（RFM）
    商品結構（Top 商品 + 集中度）
🔹 資料處理
    使用 customer_unique_id 當作真實顧客
    分析區間：2017-01 ~ 2018-08
    （排除 2016 測試期、2018-09 資料不完整）
    缺失商品分類 → 統一補 Uncategorized
🔹 中間表設計
    int_order_summary（訂單層）
    int_order_product（商品層） (因為一筆訂單可能有多項商品)
🔹 Mart 表
    mart_monthly_revenue（營收 + 成長率）
    mart_monthly_retention（新客 + 留存）
    mart_month_customer_segment（RFM 分群）
    mart_month_product（Top 商品 + Top3 占比）
🔹 重要發現
    約 97% 顧客只買一次 → 留存率極低（正常現象），平台屬於「低頻高單價」電商
    營收成長主要來自「新客導入」，不是回購
    高價客每月穩定出現，但不會累積成長期 VIP
    部分月份商品營收集中度偏高（需注意風險）
🔹 分析邏輯
    Revenue：月營收 + MoM 成長
    Customer：新客數 + 回購率
    Retention：Cohort（M1 / M2 / M3）
    RFM：用 M 排序分群（R 在此場景意義較弱）
    Product：Top 商品 + Top3 占比
🔹 技術流程
    SQL → Python尚未開始（畫圖）→ BI尚未開始（Dashboard）