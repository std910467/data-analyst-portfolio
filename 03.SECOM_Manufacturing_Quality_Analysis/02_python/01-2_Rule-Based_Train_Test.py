# %%
import pandas as pd
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from model_results import save_result
from sklearn.impute import SimpleImputer


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

labels.columns = ["label","timestamp"]

# 移除特徵無變化的欄位(有116欄)
constant_cols = [
    col for col in df.columns
    if df[col].nunique() <= 1]
len(constant_cols)
df = df.drop(columns=constant_cols)

# 第一階段分析，只保留缺失值小於10%(不含10%)欄位
first_columns = df.columns[df.isnull().mean() < 0.1]
df_first_round = df[first_columns]

x = df_first_round
y = labels["label"]

x_train.shape

x_train, x_test, y_train, y_test = train_test_split(
    x, y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

#把nan補上中位數，再把型態array轉成DF
x_train = pd.DataFrame(
    imputer.fit_transform(x_train),
    columns=x_train.columns,
    index=x_train.index
)
x_test = pd.DataFrame(
    imputer.transform(x_test),
    columns=x_test.columns,
    index=x_test.index
)

pass_df = x_train[y_train == -1]
fail_df = x_train[y_train ==  1]
feature_cols= x_train.columns


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

# 看一下各比例的cohen's d(效果量)存在多少筆欄位。
for i in range(9, 0, -1):
    threshold = i / 10
    count = (effect_df["abs_cohens_d"] >= threshold).sum()
    print(f"Cohen's d >= {threshold:.1f}：{count} 筆")

#針對abs_cohen's d大於0.5特徵當作設立門檻值，有3筆。
top_features = effect_df[
    effect_df["abs_cohens_d"] >= 0.5
].copy()

# 再抓到固定數量100%~80%不良品的情況下，看所有特徵inspection_rate(檢查率)。
quantile_list = np.arange(0, 0.21, 0.01)
result = []
for feature in top_features["feature"]:
    feature = int(feature)
    for q in quantile_list:
        threshold = fail_df[feature].quantile(q)
        pred_fail = x_train[feature] >= threshold
        actual_fail = y_train == 1
        TP = (pred_fail & actual_fail).sum()
        FP = (pred_fail & ~actual_fail).sum()
        FN = (~pred_fail & actual_fail).sum()
        TN = (~pred_fail & ~actual_fail).sum()
        recall = TP / (TP + FN)
        inspection_rate = (TP + FP) / (TP+FP+FN+TN)
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

# 第一階段 我打算先找一個主特徵，以抓到9成以上不良品為目標，但inspection_rate(檢查率)最低的
# 從圖來看，特徵510作為第一主規則
# 鎖定 510看 0~0.1之間的看一下檢查率變化
quantile_list = np.arange(0, 0.101, 0.001)
result = []
feature = 510
for q in quantile_list:
    threshold = fail_df[feature].quantile(q)
    pred_fail = x_train[feature] >= threshold
    actual_fail = y_train == 1
    TP = (pred_fail & actual_fail).sum()
    FP = (pred_fail & ~actual_fail).sum()
    FN = (~pred_fail & actual_fail).sum()
    TN = (~pred_fail & ~actual_fail).sum()
    recall = TP / (TP + FN)
    inspection_rate = (TP + FP) / (TP + FP + FN + TN)
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



# 把斜率最大的，也就是平均放棄一個fail減少最多檢查率的，當作門檻也就是0.09。
f510_threshold = feature_510_df.loc[feature_510_df["avg_inspection_drop"].idxmax(), "threshold"]
threshold_table = pd.DataFrame({
    "feature": [510],
    "role": ["gatekeeper"],
    "threshold": f510_threshold
})
# 看一下選了那個f510_threshold
# feature_510_df[feature_510_df["threshold"] == f510_threshold]


# 510特徵不動，調整另外2個門檻規則，用訓練資料調整為我想要的9成recall
# 用標準差的倍數來當微調機制+std太高、-std/2太低、-std/3太低。
# 最後用-std/4.3
top_features["threshold"] = (
    top_features["pass_mean"]
    - top_features["pass_std"]/4.3
    )
rule_count = pd.Series(0, index=x_train.index)
gatekeeper_rule = (
    x_train[510] >= f510_threshold)

for _, row in top_features[
    top_features["feature"] != 510
    ].iterrows():
    feature = int(row["feature"])
    threshold = row["threshold"]

    rule_count += (
        x_train[feature] > threshold
    ).astype(int)

# 510 成立，而且其他2個至少1個成立
pred_fail = gatekeeper_rule & (rule_count >= 1)

# 真實結果
actual_fail = y_train == 1


# TP / FP / FN / TN
TP = (pred_fail & actual_fail).sum()
FP = (pred_fail & ~actual_fail).sum()
FN = (~pred_fail & actual_fail).sum()
TN = (~pred_fail & ~actual_fail).sum()


# 指標
recall = TP / (TP + FN)
precision = TP / (TP + FP)
accuracy = (TP + TN) / (TP + FP + FN + TN)
inspection_rate = (TP + FP) / (TP + FP + FN + TN)


print(f"TP：{TP}")
print(f"FP：{FP}")
print(f"FN：{FN}")
print(f"TN：{TN}")

print(f"Recall：{recall:.2%}")
print(f"Precision：{precision:.2%}")
print(f"accuracy：{accuracy:.2%}")
print(f"inspection_rate：{inspection_rate:.2%}")

#最後 拿測試資料看看
rule_count = pd.Series(0, index=x_test.index)
gatekeeper_rule = (
    x_test[510] >= f510_threshold)

for _, row in top_features[
    top_features["feature"] != 510
    ].iterrows():
    feature = int(row["feature"])
    threshold = row["threshold"]

    rule_count += (
        x_test[feature] > threshold
    ).astype(int)

# 510 成立，而且其他2個至少1個成立
pred_fail = gatekeeper_rule & (rule_count >= 1)
# 真實結果
actual_fail = y_test == 1


# TP / FP / FN / TN
TP = (pred_fail & actual_fail).sum()
FP = (pred_fail & ~actual_fail).sum()
FN = (~pred_fail & actual_fail).sum()
TN = (~pred_fail & ~actual_fail).sum()


# 指標
recall = TP / (TP + FN)
precision = TP / (TP + FP)
accuracy = (TP + TN) / (TP + FP + FN + TN)
inspection_rate = (TP + FP) / (TP + FP + FN + TN)


print(f"TP：{TP}")
print(f"FP：{FP}")
print(f"FN：{FN}")
print(f"TN：{TN}")

print(f"Recall：{recall:.2%}")
print(f"Precision：{precision:.2%}")
print(f"accuracy：{accuracy:.2%}")
print(f"inspection_rate：{inspection_rate:.2%}")





save_result("Rule-Based_train_Test", TP, FP, FN, TN)