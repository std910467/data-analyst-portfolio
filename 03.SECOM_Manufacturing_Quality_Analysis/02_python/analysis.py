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


clean_columns = df.columns[df.isnull().mean() < 0.1]
df_first_round = df[clean_columns]
df_first_round = pd.concat([df_first_round, labels],axis=1)
df_first_round = df_first_round.dropna()
print(f"原資料集形狀(不考慮labels): {df.shape}")
print(f"第一輪使用的資料集形狀(不考慮labels): {df_first_round.shape[0], df_first_round.shape[1] - 2}")
print(f"第一輪使用的保留資料比例(不考慮labels): {round(df_first_round.shape[0]*(df_first_round.shape[1] - 2)/(df.shape[0]*df.shape[1]),2)}")
df_first_round["label"].value_counts()
labels["label"].value_counts()

## 計算看看不良品跟良品 有沒有特徵是平均值+標準差沒重疊的
feature_cols = df_first_round.columns[:-2]
feature_cols[feature_cols == 230]
# 分成良品 / 不良品
pass_df = df_first_round[df_first_round["label"] == -1]
fail_df = df_first_round[df_first_round["label"] == 1]


print(result_df)
print("不重疊 feature 數量：", len(result_df))


## 計算看看不良品跟良品 特徵平均值+標準差重疊的多寡
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

print(effect_df["abs_cohens_d"].head(20))
effect_df[["feature","abs_cohens_d"]].tail(20)
effect_df["abs_cohens_d"].mean()
df_first_round[289][df_first_round["label"]==-1].describe()
df_first_round[289][df_first_round["label"]==1].describe()
df[289]

df_first_round.loc[
    df_first_round[289].idxmax(),
    [289, "label", "timedata"]
]

df_first_round[
    [289, "label", "timedata"]
].sort_values(
    289,
    ascending=False
).head(10)

pass_289 = df_first_round[
    (df_first_round["label"] == -1) &
    (df_first_round.index != 539)
][289]

print(pass_289.describe())


df.head()
df.shape
labels.head()
labels.shape
labels[labels[0] == -1].shape[0]
labels[labels[0] == 1].shape[0]
labels[0].value_counts()
labels[0].value_counts(normalize=True)
