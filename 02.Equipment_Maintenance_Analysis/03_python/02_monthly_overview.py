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

df_monthly_model_failure = read_table("mart_monthly_model_failure", order_by="month")


df_monthly_model_failure.head()
df_monthly_model_failure.dtypes

month_summary = (
    df_monthly_model_failure.groupby("month", as_index=False)
    .agg(
        sum_failures=("total_failures", "sum"),
        sum_maint=("total_maint", "sum"),
        sum_errors=("total_errors", "sum"),
    )
    .sort_values("month", ascending=True)
)


fig, ax = plt.subplots(figsize=(10, 5))

# 設定 X 軸與柱狀圖寬度
x = month_summary["month"]
w = 0.25
idx = list(range(len(x)))

# 繪製並列柱狀圖 (修正為 ax，並讀取正確的 sum_ 欄位)
b1 = ax.bar([i - w for i in idx], month_summary["sum_failures"], width=w, label="sum_failures")
b2 = ax.bar(idx, month_summary["sum_maint"], width=w, label="sum_maint")
b3 = ax.bar([i + w for i in idx], month_summary["sum_errors"], width=w, label="sum_errors")

# 計算平均、並畫上對應的虛線
mean_fail = month_summary["sum_failures"].mean()
mean_maint = month_summary["sum_maint"].mean()
mean_err = month_summary["sum_errors"].mean()
ax.axhline(mean_fail, color=b1[0].get_facecolor(), linestyle="--", linewidth=1.5, alpha=0.7, label="_nolegend_")
ax.axhline(mean_maint, color=b2[0].get_facecolor(), linestyle="--", linewidth=1.5, alpha=0.7, label="_nolegend_")
ax.axhline(mean_err, color=b3[0].get_facecolor(), linestyle="--", linewidth=1.5, alpha=0.7, label="_nolegend_")

# 拉高Y軸
max_val = max(month_summary[["sum_failures", "sum_maint", "sum_errors"]].max())
ax.set_ylim(0, max_val * 1.25)

# 設定 X 軸刻度與標籤
ax.set_xticks(idx)
ax.set_xticklabels([str(i)[:7] for i in x], rotation=45)  # 加 rotation=45 可防止月份文字重疊
ax.set_title("Total Failures / Maint / Errors by Month")
ax.set_ylabel("Count")
ax.legend()

plt.tight_layout()
plt.savefig(BASE_DIR.parent / "05_outputs/02_monthly_overview.png",
    dpi=300, 
    bbox_inches="tight", 
)
plt.close()




# %%
