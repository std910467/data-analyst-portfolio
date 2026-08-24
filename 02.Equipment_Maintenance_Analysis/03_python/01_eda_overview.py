#%%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.colors as colors
from matplotlib.ticker import PercentFormatter
from pathlib import Path
from sqlalchemy import create_engine

import seaborn as sns



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

df_machine_summary = read_table("mart_machine_summary", order_by="machineID")

df_machine_summary["total_maint"] = (
    df_machine_summary["comp1_times"] + 
    df_machine_summary["comp2_times"] + 
    df_machine_summary["comp3_times"] + 
    df_machine_summary["comp4_times"]
)

model_summary = (
    df_machine_summary.groupby("model", as_index=False)
    .agg(
        machine_cnt=("machineID", "count"),
        avg_age=("age", "mean"),
        avg_failures=("total_failures", "mean"),
        avg_maint=("total_maint", "mean"),
        avg_errors=("total_errors", "mean"),
        avg_volt=("y_volt", "mean"),
        avg_rotate=("y_rotate", "mean"),
        avg_pressure=("y_pressure", "mean"),
        avg_vibration=("y_vibration", "mean"),
        sum_failures=("total_failures", "sum"),
        sum_maint=("total_maint", "sum"),
        sum_errors=("total_errors", "sum"),
    )
    .sort_values("model", ascending=True)
)


fig, axes = plt.subplots(1, 3, figsize=(14, 4))

# 1) 故障 / 维修 / 错误
x = model_summary["model"]
w = 0.25
idx = range(len(x))

axes[0].bar([i - w for i in idx], model_summary["avg_failures"], width=w, label="avg_failures")
axes[0].bar(idx, model_summary["avg_maint"], width=w, label="avg_maint")
axes[0].bar([i + w for i in idx], model_summary["avg_errors"], width=w, label="avg_errors")
axes[0].set_xticks(list(idx))
axes[0].set_xticklabels(x)
axes[0].set_title("Avg Failures / Maint / Errors by Model")
axes[0].legend()

# 2) 感测均值
axes[1].plot(x, model_summary["avg_volt"], marker="o", label="volt")
axes[1].plot(x, model_summary["avg_rotate"], marker="o", label="rotate")
axes[1].plot(x, model_summary["avg_pressure"], marker="o", label="pressure")
axes[1].plot(x, model_summary["avg_vibration"], marker="o", label="vibration")
axes[1].set_title("Avg Sensors by Model")
axes[1].legend()

# 3) 机台数、机龄
axes[2].bar(x, model_summary["machine_cnt"], alpha=0.7, label="machine_cnt")
axes[2].set_ylabel("machine_cnt")
ax2 = axes[2].twinx()
ax2.plot(x, model_summary["avg_age"], color="orange", marker="o", label="avg_age")
ax2.set_ylabel("avg_age")
axes[2].set_title("Machine Count & Avg Age")

plt.tight_layout()
plt.show()
plt.close()