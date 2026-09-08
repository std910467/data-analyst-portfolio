# %%
import pandas as pd
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# 檔案路徑
BASE_DIR = Path(__file__).resolve().parent
df = pd.read_csv(
    BASE_DIR.parent / "01_raw_data/secom.data",
    sep=r"\s+",
    header=None
)

labels = pd.read_csv(
    BASE_DIR.parent /"01_raw_data/secom_labels.data",
    sep=r"\s+",
    header=None)

labels.columns = ["label","timedata"]

# 移除特徵無變化的欄位(有116欄)
constant_cols = [
    col for col in df.columns
    if df[col].nunique() <= 1]
len(constant_cols)
df = df.drop(columns=constant_cols)

# 第一階段分析，只保留缺失值小於10%(不含10%)欄位，並且把有缺失值的資料行移除
first_columns = df.columns[df.isnull().mean() < 0.1]
df_first_round = df[first_columns]
df_first_round = pd.concat([df_first_round, labels],axis=1)
df_first_round = df_first_round.dropna()
# print(f"原資料集形狀(不考慮labels): {df.shape}")
# print(f"第一輪使用的資料集形狀(不考慮labels): {df_first_round.shape[0], df_first_round.shape[1] - 2}")
# print(f"第一輪使用的保留資料比例(不考慮labels): {round(df_first_round.shape[0]*(df_first_round.shape[1] - 2)/(df.shape[0]*df.shape[1]),2)}")
# 原資料集形狀(不考慮labels): (1567, 474)
# 第一輪使用的資料集形狀(不考慮labels): (1393, 422)
# 第一輪使用的保留資料比例(不考慮labels): 0.79

feature_cols= df_first_round.columns[:-2]
pass_df = df_first_round[df_first_round["label"]== -1]
fail_df = df_first_round[df_first_round["label"]==  1]

## 計算看看不良品跟良品 特徵平均值+標準差重疊的多寡，並將重疊比例越少的排越前面。
result = []
for col in feature_cols:
    pass_data = pass_df[col]
    fail_data = fail_df[col]
    pass_mean = pass_data.mean()
    fail_mean = fail_data.mean()
    pass_std = pass_data.std()
    fail_std = fail_data.std()
    # pooled standard deviation
    pooled_std = np.sqrt(
        ((len(pass_data) - 1) * pass_std**2
            + (len(fail_data) - 1) * fail_std**2
        )
        /
        (len(pass_data) + len(fail_data) - 2)
    )
    if pooled_std != 0:
        cohens_d = (fail_mean - pass_mean) / pooled_std
    else:
        cohens_d = 0
    result.append([
        col,
        pass_mean,
        fail_mean,
        pass_std,
        fail_std,
        cohens_d,
        abs(cohens_d)
    ])
effect_df = pd.DataFrame(
    result,
    columns=[
        "feature",
        "pass_mean",
        "fail_mean",
        "pass_std",
        "fail_std",
        "cohens_d",
        "abs_cohens_d"
    ]
)
effect_df = effect_df.sort_values(
    "abs_cohens_d",
    ascending=False
)

# 看一下大小的cohen's d(效果量)存在多少筆欄位。
for i in range(9, 0, -1):
    threshold = i / 10
    count = (effect_df["abs_cohens_d"] >= threshold).sum()
    print(f"Cohen's d >= {threshold:.1f}：{count} 筆")

#針對abs_cohen's d大於0.5特徵當作設立門檻值的規劃
top_features = effect_df[
    effect_df["abs_cohens_d"] >= 0.5
].copy()

# 再抓到固定數量100%~70%不良品的情況下，看所有特徵inspection_rate(檢查率)。
quantile_list = np.arange(0, 0.31, 0.01)
result = []
for feature in top_features["feature"]:
    feature = int(feature)
    for q in quantile_list:
        threshold = fail_df[feature].quantile(q)
        pred_fail = df_first_round[feature] >= threshold
        actual_fail = df_first_round["label"] == 1
        TP = (pred_fail & actual_fail).sum()
        FP = (pred_fail & ~actual_fail).sum()
        FN = (~pred_fail & actual_fail).sum()
        TN = (~pred_fail & ~actual_fail).sum()
        recall = TP / (TP + FN)
        inspection_rate = (TP + FP) / len(df_first_round)
        result.append([
            feature,
            q,
            threshold,
            recall,
            inspection_rate
        ])
result_df = pd.DataFrame(
    result,
    columns=[
        "feature",
        "quantile",
        "threshold",
        "recall",
        "inspection_rate"
    ]
)
plt.figure(figsize=(10, 6))

for feature in top_features["feature"]:
    feature = int(feature)

    plot_df = result_df[result_df["feature"] == feature]

    plt.plot(
        plot_df["quantile"],
        plot_df["inspection_rate"],
        marker="o",
        label=f"Feature {feature}"
    )
plt.xlabel("Fail Quantile")
plt.ylabel("Inspection Rate")
plt.title("Inspection Rate by Fail Quantile")
plt.legend()
plt.grid(alpha=0.3)
plt.show()

# 第一階段 我打算先找一個主規則，以抓到9成以上不良品為目標，但inspection_rate(檢查率)最低的
# 從圖來看，特徵501作為第一主規則
#鎖定 501看 0~0.1之間的看一下檢查率變化
quantile_list = np.arange(0, 0.101, 0.01)
result = []
feature = 510
for q in quantile_list:
    threshold = fail_df[feature].quantile(q)
    pred_fail = df_first_round[feature] >= threshold
    actual_fail = df_first_round["label"] == 1
    TP = (pred_fail & actual_fail).sum()
    FP = (pred_fail & ~actual_fail).sum()
    FN = (~pred_fail & actual_fail).sum()
    TN = (~pred_fail & ~actual_fail).sum()
    recall = TP / (TP + FN)
    inspection_rate = (TP + FP) / len(df_first_round)
    result.append([
        q,
        threshold,
        TP,
        FP,
        FN,
        TN,
        recall,
        inspection_rate
    ])

feature_510_df = pd.DataFrame(
    result,
    columns=[
        "quantile", "threshold",
        "TP", "FP", "FN", "TN",
        "recall", "inspection_rate"
    ]
)
# 看一下哪個節點交換效益最好，
max_rate=feature_510_df["inspection_rate"].max()
feature_510_df["avg_inspection_drop"] = (
    (max_rate - feature_510_df["inspection_rate"])
    / feature_510_df["quantile"])

# 看起來0.01不錯，放棄一個fail ，減少4%多的檢查率。
rule_510 = result_df[
    (result_df["feature"] == 510) &
    (result_df["quantile"] == 0.01)
]
threshold_table = pd.DataFrame({
    "feature": [510],
    "role": ["gatekeeper"],
    "threshold": [rule_510["threshold"].iloc[0]]
})










#針對前面7個差異較大的7個特徵設立門檻
top_features = effect_df.head(7).copy()
top_features["threshold"] = (
    top_features["pass_mean"]
    + top_features["cohens_d"] * top_features["pass_std"]
)

#假設門檻值是，目標抓到多少不良品。
threshold_list = []
for feature in top_features["feature"]:
    feature = int(feature)
    threshold = fail_df[feature].quantile(0.25)
    threshold_list.append(threshold)
top_features["threshold"] = threshold_list



#測試一下每個條件自已的準確度
rule_result = []

for _, row in top_features.iterrows():
    feature = int(row["feature"])
    threshold = row["threshold"]

    # 單一 Feature 規則
    pred_fail = df_first_round[feature] >= threshold
    actual_fail = df_first_round["label"] == 1

    # TP / FP / FN / TN
    TP = (pred_fail & actual_fail).sum()
    FP = (pred_fail & ~actual_fail).sum()
    FN = (~pred_fail & actual_fail).sum()
    TN = (~pred_fail & ~actual_fail).sum()

    # 指標
    recall = TP / (TP + FN)
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    coverage = (TP + FP) / len(df_first_round)

    rule_result.append([
        feature,
        threshold,
        TP,
        FP,
        FN,
        TN,
        recall,
        precision,
        coverage
    ])

rule_df = pd.DataFrame(
    rule_result,
    columns=[
        "feature",
        "threshold",
        "TP",
        "FP",
        "FN",
        "TN",
        "recall",
        "precision",
        "coverage"
    ]
)

print(rule_df)





#用七個門檻規則測試~原始資料看準確度
rule_count = pd.Series(0, index=df_first_round.index)

for _, row in top_features.iterrows():
    feature = int(row["feature"])
    threshold = row["threshold"]

    rule_count += (df_first_round[feature] > threshold).astype(int)

# 至少 3 條規則成立 → 預測 Fail
pred_fail = rule_count >= 1

# 真實結果
actual_fail = df_first_round["label"] == 1


# TP / FP / FN / TN
TP = (pred_fail & actual_fail).sum()
FP = (pred_fail & ~actual_fail).sum()
FN = (~pred_fail & actual_fail).sum()
TN = (~pred_fail & ~actual_fail).sum()


# 指標
recall = TP / (TP + FN)
precision = TP / (TP + FP)

# 這裡把覆蓋率定義成：規則判定為 Fail 的資料，占全部資料多少
coverage = (TP + FP) / len(df_first_round)


print(f"TP：{TP}")
print(f"FP：{FP}")
print(f"FN：{FN}")
print(f"TN：{TN}")

print(f"Recall：{recall:.2%}")
print(f"Precision：{precision:.2%}")
print(f"標記率：{coverage:.2%}")

labels["label"].value_counts()
104/(1463+104)









feature_59 = result_df[result_df["feature"] == 59].copy()

feature_59[
    ["quantile", "threshold", "recall",
     "inspection_rate", "inspection_drop"]
]