#%%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.colors as colors
from matplotlib.ticker import PercentFormatter
from pathlib import Path
from sqlalchemy import create_engine

# 檔案路徑
BASE_DIR = Path(__file__).resolve().parent
# 格式: mysql+pymysql://<帳號>:<密碼>@<主機>/<資料庫名稱>
engine = create_engine("mysql+pymysql://root:123456@localhost/azure_pdm")

#作出讀取檔案的函式
def read_table(table_name, order_by=None):
    query = f"SELECT * FROM {table_name}"
    if order_by:
        query += f" ORDER BY {order_by}"
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

df_machine_summary = read_table("mart_machine_summary", order_by="total_failures DESC")
cols_maint = ["comp1_times","comp2_times","comp3_times","comp4_times"]
cols_fail = ["comp1_failure","comp2_failure","comp3_failure","comp4_failure"]

maint_sum = df_machine_summary[cols_maint].sum()
fail_sum = df_machine_summary[cols_fail].sum()

result = pd.DataFrame({
    "maint": maint_sum.values,
    "failure": fail_sum.values
}, index=["comp1","comp2","comp3","comp4"])

result["failure_per_maint"] = result["failure"] / result["maint"]
result[["maint","failure"]].plot(kind="bar")
result["failure_per_maint"].plot(kind="bar")

# %%
