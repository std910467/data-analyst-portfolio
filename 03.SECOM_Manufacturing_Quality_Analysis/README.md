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


## 隨手筆記
第一階段，評估一下這資料是不是以風險篩檢為目標。

### 9/6 分析筆記

今天先以單一 Feature 為單位，比較 Pass / Fail 的差異。

- 使用 Cohen's d 將不同尺度的 Feature 標準化後進行比較。
- 目前沒有 `|d| >= 0.7` 的 Feature，`|d| >= 0.6` 有 2 個、`>= 0.5` 有 5 個、`>= 0.4` 有 15 個。
- 第一輪人工分析先以前 7 個 Feature 為主，暫時不考慮 Feature 之間的交互作用。
- 檢查部分低 Cohen's d Feature 時發現極端值可能明顯影響標準差，但若 Pass / Fail 的中心位置仍接近，第一階段先不深入處理 Outlier。
- 以 Pass 作為正常製程基準，暫時使用 `Pass Mean + Cohen's d × Pass Std` 建立各 Feature 的人工門檻。

將 7 條規則組合後測試：
- 至少 1 條成立即標記為高風險時，Recall 約 77.8%。
- 約 45.3% 的產品會被標記，其中不良率（Precision）約 12.2%。
- 清理後全部資料的不良率約 7.1%，因此目前規則已能將部分不良品集中到較小的檢查範圍，但仍有改善空間。

目前對商業目的的想法也有所調整：
這個分析不一定要直接取代最終品質檢查，而是可以先利用製程 Feature 做風險篩選。在盡量維持高 Recall、避免漏掉不良品的前提下，降低需要進一步檢查的產品比例。

下一步預計先觀察 7 個 Feature 各自的 Recall、Precision 與誤判情況，再嘗試人工調整各 Feature 的權重與規則。

### 9/8 分析筆記
Rule-based 第一階段規則設計：
以高 Recall 為優先，先建立一個 Gatekeeper（門神）盡可能攔截 Fail，再利用其他候選特徵逐步排除門神誤抓的 Pass，以降低最終 Inspection Rate。初步比較 Cohen's d 篩選出的候選特徵後，Feature 510 在高 Recall 區間具有較好的檢查效率，因此進一步測試 Fail quantile 0～0.10 的門檻變化。結果顯示 q=0.01 時，僅由 100% Recall 降至 98.99%（99 個 Fail 中漏掉 1 個），Inspection Rate 則由 98.995% 降至 94.616%，約減少 4.38 個百分點，因此暫定 Feature 510、q=0.01（threshold ≈ 23.124）作為第一階段 Gatekeeper。後續將針對 Gatekeeper 攔截的樣本，利用其餘候選特徵嘗試釋放 False Positive，並觀察降低 Inspection Rate 時造成的 True Positive 損失。

### 9/9 筆記
第一階段以 Feature 510 作為 Gatekeeper，利用 Fail quantile 尋找高 Recall 門檻，最後將 q=0.009 附近作為主規則設定，使第一階段盡可能保留 Fail。第二階段則使用其餘 4 個候選特徵（59、103、348、431）協助排除 Gatekeeper 誤抓的 Pass，並以 pass_mean + pass_std、pass_mean + 0.5*pass_std、pass_mean 三種統一門檻進行測試。結果顯示門檻越寬鬆，Recall 會提高，但 Inspection Rate 也隨之上升。其中以 pass_mean 作為第二階段門檻、且至少一項特徵成立時，最終 TP=90、FP=968、FN=9、TN=326，Recall=90.91%，Inspection Rate=75.95%。目前暫以此作為人工 Rule-based screening baseline，後續可與 ML 模型在相近 Recall 條件下比較 Inspection Rate。

### 9/11筆記
### 2026/09/11 Logistic Regression 初步測試

開始進入 ML 分類模型測試，第一階段先使用前述 Cohen's d 篩選出的 Top 5 Features（59、103、510、348、431）建立 Logistic Regression baseline。

資料以 80/20 分為 Train / Test，並使用 stratified split 維持 Pass / Fail 原始比例。缺失值以 Train data 的 median 進行填補，再使用 StandardScaler 進行標準化，避免不同 Feature 尺度影響模型訓練。

Logistic Regression 訓練完成後，以 `predict_proba()` 取得 Test data 的 Fail probability，並測試不同 probability threshold。在 Recall ≥ 90% 的條件下，目前選定 threshold = 0.032：

- TP = 19
- FP = 236
- FN = 2
- TN = 57
- Recall = 90.48%
- Precision = 7.45%
- Inspection Rate = 81.21%

目前結果先作為 Logistic Regression Top 5 baseline。由於先前人工 Rule-based 結果使用全資料進行規則建立與評估，兩者目前不能直接作公平比較，後續再統一評估方式。