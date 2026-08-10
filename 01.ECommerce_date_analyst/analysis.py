#%%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sqlalchemy import create_engine
from pathlib import Path

# 檔案路徑
BASE_DIR = Path(__file__).resolve().parent
# 格式: mysql+pymysql://<帳號>:<密碼>@<主機>/<資料庫名稱>
engine = create_engine("mysql+pymysql://root:123456@localhost/olist")

#作出讀取檔案的函式
def read_table(table_name, order_by=None):
    query = f"SELECT * FROM {table_name}"
    if order_by:
        query += f" ORDER BY {order_by}"
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

df_revenue = read_table("mart_monthly_revenue", order_by="month")
df_customer_segment = read_table("mart_monthly_customer_segment", order_by="month")
df_retention = read_table("mart_monthly_retention", order_by="month")
df_product = read_table("mart_monthly_product", order_by="month")


df_revenue['month'] = pd.to_datetime(df_revenue['month'])
df_customer_segment['month'] = pd.to_datetime(df_customer_segment['month'])
df_retention['month'] = pd.to_datetime(df_retention['month'])
df_product['month'] = pd.to_datetime(df_product['month'])

# region 01、營收x成長率圖
fig,ax1 = plt.subplots()
ax1.bar(
    df_revenue["month"],
    df_revenue["revenue"],
    width=20,
    color="steelblue")

ax1.set_xlabel("Month")
ax1.set_ylabel("Revenue")
ax1.tick_params(axis="x", rotation=45)
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m")
)
ax2 = ax1.twinx()
ax2.plot(
    df_revenue["month"],
    df_revenue["growth_rate"],
    color="orange",
    marker="o")
ax2.axhline(y=0, color="gray", linestyle="--", linewidth=1)
ax2.set_ylabel("Growth Rate")

plt.title("Monthly Revenue & Growth Rate")
plt.tight_layout()
plt.savefig(
    BASE_DIR /"revenue_chart.png",
    dpi=300, 
    bbox_inches="tight", 
)
plt.show()
plt.close()
# endregion
# region 02、XXXX圖

# endregion
# region 03、XXXX圖

# endregion
# region 04、XXXX圖

# endregion
# region 05、XXXX圖

# endregion
# %%