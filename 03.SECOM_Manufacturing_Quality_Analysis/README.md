# 03. SECOM Manufacturing Quality Analysis

## 專案說明

本專案使用 UCI SECOM 半導體製程公開資料，練習製造業品質資料分析。

SECOM 資料包含大量製程特徵，以及每筆資料對應的 Pass / Fail 結果。  
這次希望從前兩個專案的資料整理與描述性分析，再往統計分析、特徵篩選與 Machine Learning 延伸。

目前專案進行中。

---

## 資料來源

UCI Machine Learning Repository - SECOM

原始資料：

- `secom.data`：製程特徵資料
- `secom_labels.data`：Pass / Fail 與時間資料
- `secom.names`：資料集說明

---

## 預計分析方向

- 檢查資料結構、缺失值與資料品質
- 觀察 Pass / Fail 分布與類別不平衡
- 比較 Pass / Fail 的製程特徵差異
- 進行特徵篩選，找出較有影響的製程特徵
- 嘗試建立基礎 Machine Learning 分類模型
- 使用 Precision、Recall、F1-Score 等指標評估模型

---

## 使用技術

- Python
- Pandas
- Matplotlib
- Scikit-learn（後續）

---

## 目前進度

## 目前進度

### 第一階段
第一階段先以單一 Feature 為單位，比較 Pass / Fail 的差異，暫不考慮 Feature 間的交互作用。
先檢查原始 Feature，若欄位中的有效數值種類只有 1 種（包含其餘為 NaN 的情況），代表該 Feature 沒有可用的變化資訊，因此直接移除。(116欄無效)
單變量
先處理缺失值，保留缺失率低於 10% 的 Feature，再將剩餘缺失資料以 `dropna()` 移除。

- 原始資料：1,567 筆、590 Features
- 第一輪資料：1,393 筆、538 Features
- Pass：1,463 → 1,294
- Fail：104 → 99
- Fail 樣本仍保留約 95%

目前先使用這份資料進行分析。

接著比較 Pass / Fail 各 Feature 的平均值與標準差：

- `Mean ± 1 SD` 完全不重疊的 Feature：0 個
- 因不同 Feature 尺度不同，改使用 Cohen's d 比較兩群的相對差異
- 標準差使用 pooled standard deviation，依 Pass / Fail 各自的變異與樣本數合併
- 目前較明顯：Feature 59（|d| ≈ 0.64）、Feature 100（|d| ≈ 0.61）
- 後續可視情況比較 Glass's Δ，以 Pass 的標準差作為正常製程基準

目前先記錄分析結果，不直接以 Cohen's d 作為 Feature 篩選條件。

