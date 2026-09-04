# %%
import pandas as pd
from pathlib import Path

# 檔案路徑
BASE_DIR = Path(__file__).resolve().parent

csv_file_path =BASE_DIR.parent / "01_raw_data"/csv_name

df = pd.read_csv(
    BASE_DIR.parent / "01_raw_data/secom.data",
    sep=r"\s+",
    header=None
)

labels = pd.read_csv(
    BASE_DIR.parent /"01_raw_data/secom_labels.data",
    sep=r"\s+",
    header=None
)
df.head()
df.shape
labels.head()
labels.shape
labels[labels[0] == -1].shape[0]
labels[labels[0] == 1].shape[0]
labels[0].value_counts()
labels[0].value_counts(normalize=True)

rate_number=[]
df_miss_rate =((df.shape[0]-df.count())/df.shape[0])
rate_number.append(df_miss_rate[df_miss_rate >= 0.9].shape[0])
rate_number.append(df_miss_rate[(df_miss_rate < 0.9) & (df_miss_rate >= 0.8) ].shape[0])
rate_number.append(df_miss_rate[(df_miss_rate < 0.8) & (df_miss_rate >= 0.7) ].shape[0])
rate_number.append(df_miss_rate[(df_miss_rate < 0.7) & (df_miss_rate >= 0.6) ].shape[0])
rate_number.append(df_miss_rate[(df_miss_rate < 0.6) & (df_miss_rate >= 0.5) ].shape[0])
rate_number.append(df_miss_rate[(df_miss_rate < 0.5) & (df_miss_rate >= 0.4) ].shape[0])
rate_number.append(df_miss_rate[(df_miss_rate < 0.4) & (df_miss_rate >= 0.3) ].shape[0])
rate_number.append(df_miss_rate[(df_miss_rate < 0.3) & (df_miss_rate >= 0.2) ].shape[0])
rate_number.append(df_miss_rate[(df_miss_rate < 0.2) & (df_miss_rate >= 0.1) ].shape[0])
rate_number.append(df_miss_rate[(df_miss_rate < 0.1)].shape[0])
sum(rate_number)

((df.shape[0]-df.count())/df.shape[0]).describe()
((df.shape[0]-df.count())/df.shape[0]).sort_values(ascending=False).head(20)

df.isnull().mean()

# 找出缺失率小於 10% 的欄位名稱
clean_columns = df.columns[df.isnull().mean() < 0.1]

# 提取出這 538 個欄位，作為你第一輪的訓練資料
df_first_round = df[clean_columns]

print(f"第一輪使用的資料集形狀: {df_first_round.shape}")