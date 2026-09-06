# %%
import pandas as pd
from pathlib import Path
import numpy as np

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

# 第一階段分析，先針對缺失值小於10%(不含10%)的進行，並且把有缺失的資料移除
first_columns = df.columns[df.isnull().mean() < 0.1]
df_first_round = df[first_columns]
df_first_round = pd.concat([df_first_round, labels],axis=1)
df_first_round = df_first_round.dropna()
print(f"原資料集形狀(不考慮labels): {df.shape}")
print(f"第一輪使用的資料集形狀(不考慮labels): {df_first_round.shape[0], df_first_round.shape[1] - 2}")
print(f"第一輪使用的保留資料比例(不考慮labels): {round(df_first_round.shape[0]*(df_first_round.shape[1] - 2)/(df.shape[0]*df.shape[1]),2)}")
# 看一下 不良品 跟良品的資料筆數
# df_first_round["label"].value_counts()
# labels["label"].value_counts()

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
        (
            (len(pass_data) - 1) * pass_std**2
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

# # 看一下平均數的差異。
# for i in range(9, 0, -1):
#     threshold = i / 10
#     count = (effect_df["abs_cohens_d"] >= threshold).sum()
    
#     print(f"Cohen's d >= {threshold:.1f}：{count} 筆")

#針對前面7個差異較大的7個特徵設立門檻
top_features = effect_df.head(7).copy()
top_features["threshold"] = (
    top_features["pass_mean"]
    + top_features["cohens_d"] * top_features["pass_std"]
)

#測試一下每個條件自已的準確度
rule_result = []

for _, row in top_features.iterrows():
    feature = int(row["feature"])
    threshold = row["threshold"]

    # 單一 Feature 規則
    pred_fail = df_first_round[feature] > threshold
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




#回頭測試~原始資料看準確度
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