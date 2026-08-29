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
df_machine_TOP20 = df_machine_summary.head(20).copy()

cols_maint = ["comp1_times","comp2_times","comp3_times","comp4_times"]
cols_fail = ["comp1_failure","comp2_failure","comp3_failure","comp4_failure"]

maint_sum = df_machine_summary[cols_maint].sum()
fail_sum = df_machine_summary[cols_fail].sum()
Top20_maint_sum = df_machine_TOP20[cols_maint].sum()
Top20_fail_sum = df_machine_TOP20[cols_fail].sum()

result = pd.DataFrame({
    "maint": maint_sum.values,
    "failure": fail_sum.values
}, index=["comp1","comp2","comp3","comp4"])
Top20_result = pd.DataFrame({
    "maint": Top20_maint_sum.values,
    "failure": Top20_fail_sum.values
}, index=["comp1","comp2","comp3","comp4"])

result["failure_per_maint"] = result["failure"] / result["maint"]
Top20_result["failure_per_maint"] = Top20_result["failure"] / Top20_result["maint"]
max_val = max(result["failure_per_maint"].max(), 
              Top20_result["failure_per_maint"].max())

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# --- 左上：全廠comp1~4 的維保數與故障數 ---
result[["maint", "failure"]].plot(kind="bar", ax=axes[0, 0], rot=0)
axes[0, 0].set_title("Total: Maint & Failure by Component")
axes[0, 0].set_ylabel("Count")

# --- 右上：全廠 comp1~4 的故障/維保比例 ---
result["failure_per_maint"].plot(kind="bar", ax=axes[0, 1], color="orange", rot=0)
axes[0, 1].set_title("Total: Failure / Maint Ratio")
axes[0, 1].set_ylabel("Ratio")
axes[0, 1].set_ylim(0, max_val*1.2)

# --- 左下：TOP20 機器 comp1~4 的維保數與故障數 ---
Top20_result[["maint", "failure"]].plot(kind="bar", ax=axes[1, 0], rot=0)
axes[1, 0].set_title("Top 20: Maint & Failure by Component")
axes[1, 0].set_ylabel("Count")

# --- 右下：TOP20 機器 comp1~4 的故障/維保比例 ---
Top20_result["failure_per_maint"].plot(kind="bar", ax=axes[1, 1], color="orange", rot=0)
axes[1, 1].set_title("Top 20: Failure / Maint Ratio")
axes[1, 1].set_ylabel("Ratio")
axes[1, 1].set_ylim(0, max_val*1.2)

plt.tight_layout()
plt.savefig(
    BASE_DIR.parent / "05_outputs/04_comp_overview.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()



# %%
