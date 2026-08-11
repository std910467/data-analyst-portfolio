#%%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import PercentFormatter
import seaborn as sns
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

df_customer_segment.head()

df_revenue.head()
# region 01、營收x成長率圖
df_revenue["revenue_ma3"]=df_revenue["revenue"].rolling(window=3).mean()
fig,ax1 = plt.subplots(figsize=(10, 6))
ax1.bar(
    df_revenue["month"],
    df_revenue["revenue"],
    width=20,
    color="steelblue")

line_ma3 = ax1.plot(
    df_revenue["month"],
    df_revenue["revenue_ma3"],
    color="darkred",
    linewidth=2,
    linestyle="--",
    label="3M Rolling Avg",
)

ax1.set_xlabel("Month")
ax1.set_ylabel("Revenue", color="steelblue")
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
ax2.set_ylabel("Growth Rate", color="orange")

ax2.set_ylim(top=ax2.get_ylim()[1] * 1.2)
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc="upper left")

plt.title("Monthly Revenue & Growth Rate")
plt.tight_layout()
plt.savefig(BASE_DIR.parent / "05_outputs/01_monthly_revenue_chart.png",
    dpi=300, 
    bbox_inches="tight", 
)
plt.close()
# endregion
# region 02、Cohort Retention 熱力圖、柱狀圖

m_cols=["new_customers","repeat_1m_customers","repeat_2m_customers","repeat_3m_customers"]
retention_pct = df_retention.copy()
retention_pct[m_cols] = retention_pct[m_cols].div(
    retention_pct["new_customers"], axis=0
)
retention_pct = retention_pct.set_index("month")[m_cols]
retention_pct.columns = ["M+0", "M+1", "M+2", "M+3"]
retention_pct = retention_pct.drop(columns="M+0")
retention_pct.index = pd.to_datetime(retention_pct.index).strftime("%Y-%m")
plt.figure(figsize=(10, 6))
sns.heatmap(
    retention_pct,
    annot=True, 
    fmt=".1%",  
    cmap="YlGnBu",  
    vmin=0,
    vmax=0.01,  #
)

plt.title("Monthly Customer Cohort Retention Rate (%)")
plt.xlabel("Cohort Period (Months)")
plt.ylabel("First Order Month")
plt.tight_layout()
plt.savefig(BASE_DIR.parent / "05_outputs/02a_cohort_retention_heatmap.png", dpi=300)
plt.close()

retention_pct.head()
df_m1 = retention_pct[["M+1"]].copy()
avg_m1 = df_m1["M+1"].mean()

plt.figure(figsize=(12, 6))
bars = plt.bar(
    df_m1.index,
    df_m1["M+1"],
    color="#3498db",
    alpha=0.85,
    width=0.6,
    label="M+1 Retention Rate",
)

plt.axhline(
    y=avg_m1,
    color="#e74c3c",
    linestyle="--",
    linewidth=2,
    label=f"Average ({avg_m1:.2%})",
)

for bar in bars:
    height = bar.get_height()
    if height > 0: 
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 0.0003, 
            f"{height:.2%}",
            ha="center",
            va="bottom",
            fontsize=8.5,
            rotation=0,
        )
plt.title(
    "Olist M+1 Customer Retention Rate by Cohort Month", fontsize=14, pad=15
)
plt.xlabel("Cohort Month", fontsize=11, labelpad=10)
plt.ylabel("M+1 Retention Rate (%)", fontsize=11)

plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.xticks(rotation=45, ha="right", fontsize=9.5)
plt.yticks(fontsize=9.5)
plt.ylim(0, df_m1["M+1"].max() * 1.25)

plt.legend(loc="upper right", frameon=True)
plt.grid(axis="y", linestyle=":", alpha=0.6)
plt.tight_layout()
plt.savefig(BASE_DIR.parent / "05_outputs/02b_m1_retention_bar_chart.png", dpi=300)
plt.close()


# endregion
# region 03、XXXXX圖


# endregion
# region 04、XXXX圖

# endregion
# region 05、XXXX圖

# endregion
# %%