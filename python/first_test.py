#%%
import os
from pathlib import Path
import pandas as pd
#調出本py檔案的路徑，確認相對位置一致
BASE_DIR = Path(__file__).resolve().parent
df = pd.read_csv(BASE_DIR.parent/"data/ecommerce_orders.csv")

#如果要設定相關參數可以考慮以下
# df = pd.read_csv(
#     "student.csv",
#     sep=",",          # 分隔符號
#     header=0,         # 第一列為欄位名稱
#     index_col=None,   # 不指定索引欄
#     encoding="utf-8"  # 編碼
# )

# 查看資料
print(df.head())      # 前 5 筆
print(df.tail())      # 後 5 筆
print(df.info())      # 資料型態
print(df.columns)     # 欄位名稱
print(df.shape)       # (列數, 欄數)
print(df.dtypes)      #查看型別

# 開始整理資
df["date"]=pd.to_datetime(df["date"]) #將日期字串，轉成日期格式
df["month"]=df["date"].dt.to_period("M")

month_revenue=df[["month","amount"]].groupby("month",as_index=False).agg(revenue=("amount","sum"))
month_revenue["previous"]=month_revenue["revenue"].shift(1)
month_revenue["glowth_rate"] =((month_revenue["revenue"]-month_revenue["previous"])/month_revenue["previous"]).round(2)
# %%
