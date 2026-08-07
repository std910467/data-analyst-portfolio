#%%
import os
from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
df = pd.read_csv(BASE_DIR.parent/"data/orders.csv")

df.head(5)
df.columns
df.dtypes
df["order_date"]=pd.to_datetime(df["order_date"]) #將日期字串轉乘為 日期格式
# 測試用
# df_127=df[df["customer_id"]==127]
# # print(df_127["amount"])
# print(customer_RFM[customer_RFM["customer_id"]==127])
customer_RFM =df.groupby("customer_id").agg(
                                            R=("order_date","max"  ),
                                            F=("customer_id","count"),
                                            M=("amount", "sum")
                                        ).reset_index()
customer_RFM["M"]=customer_RFM["M"].round(2) #將數字有浮點數處理掉。
customer_RFM["R"]=(pd.to_datetime("today")-pd.Timedelta(days=1)-customer_RFM["R"]).dt.days

customer_RFM_SQL = pd.read_csv(BASE_DIR.parent/"output_test/customer_RFM.csv")
customer_RFM_SQL = customer_RFM_SQL.sort_values(by="customer_id").reset_index(drop=True)

diff = customer_RFM.compare(customer_RFM_SQL)
diff


# 當無法compare報錯，欄位不一致時，測試每個欄位是不是有不一樣
# print(customer_RFM.shape)
# print(customer_RFM_SQL.shape)
# print(customer_RFM.columns.tolist())
# print(customer_RFM_SQL.columns.tolist())
# print(set(customer_RFM.columns) - set(customer_RFM_SQL.columns))
# print(set(customer_RFM_SQL.columns) - set(customer_RFM.columns))
# customer_RFM = customer_RFM.sort_index(axis=1)
# customer_RFM_SQL = customer_RFM_SQL.sort_index(axis=1)
# type(customer_RFM_SQL)
# %%