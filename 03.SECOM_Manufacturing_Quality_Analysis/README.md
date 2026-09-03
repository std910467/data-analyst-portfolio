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

專案剛開始，目前先進行資料讀取與資料品質檢查。

後續會隨分析進度持續更新。