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

df_machine_summary = read_table("mart_machine_summary", order_by="machineID")


model_summary = (
    df_machine_summary.groupby("model", as_index=False)
    .agg(
        machine_cnt=("machineID", "count"),
        avg_age=("age", "mean"),
        avg_failures=("total_failures", "mean"),
        avg_maint=("total_maint", "mean"),
        avg_errors=("total_errors", "mean"),
        avg_volt=("avg_volt", "mean"),
        avg_rotate=("avg_rotate", "mean"),
        avg_pressure=("avg_pressure", "mean"),
        avg_vibration=("avg_vibration", "mean"),
        sum_failures=("total_failures", "sum"),
        sum_maint=("total_maint", "sum"),
        sum_errors=("total_errors", "sum"),
    )
    .sort_values("model", ascending=True)
)


fig, axes = plt.subplots(1, 3, figsize=(14, 4))

# 1) 故障 / 維修 / 錯誤
x = model_summary["model"]
w = 0.25
idx = range(len(x))

axes[0].bar([i - w for i in idx], model_summary["avg_failures"], width=w, label="avg_failures")
axes[0].bar(idx, model_summary["avg_maint"], width=w, label="avg_maint")
axes[0].bar([i + w for i in idx], model_summary["avg_errors"], width=w, label="avg_errors")
axes[0].set_xticks(list(idx))
axes[0].set_xticklabels(x)
# 拉高Y軸
max_val = max(model_summary[["avg_errors","avg_maint","avg_failures"]].max())
axes[0].set_ylim(0, max_val * 1.25)

axes[0].set_title("Avg Failures / Maint / Errors by Model")
axes[0].legend()

# 2) 感測器均值
axes[1].plot(x, model_summary["avg_volt"], marker="o", label="volt")
axes[1].plot(x, model_summary["avg_pressure"], marker="o", label="pressure")
axes[1].plot(x, model_summary["avg_vibration"], marker="o", label="vibration")
axes[1].set_title("Avg Sensors by Model")
axes[1].legend()
axes[1].set_ylabel("Volt / Pressure / Vibration") 
# 拉高Y軸
max_val = max(model_summary[["avg_volt","avg_pressure","avg_vibration"]].max())
axes[1].set_ylim(0, max_val * 1.5)


ax_rotate = axes[1].twinx()
ax_rotate.plot(x, model_summary["avg_rotate"], marker="o", label="rotate", color="tab:red")
ax_rotate.set_ylabel("Rotate (RPM)")
lines_left, labels_left = axes[1].get_legend_handles_labels()
lines_right, labels_right = ax_rotate.get_legend_handles_labels()
axes[1].legend(lines_left + lines_right, labels_left + labels_right, loc="upper right")


# 3) 機台數、機齡
axes[2].bar(x, model_summary["machine_cnt"], alpha=0.7, label="machine_cnt")
axes[2].set_ylabel("machine_cnt")
ax2 = axes[2].twinx()
ax2.plot(x, model_summary["avg_age"], color="orange", marker="o", label="avg_age")
ax2.set_ylabel("avg_age")
axes[2].set_title("Machine Count & Avg Age")

plt.tight_layout()
plt.savefig(BASE_DIR.parent / "05_outputs/01_models_overview.png",
    dpi=300, 
    bbox_inches="tight", 
)
plt.close()



# fig, ax = plt.subplots(figsize=(8, 5))

# # 1. 主軸（左側）：繪製 volt, pressure, vibration
# # ax.plot(x, model_summary["avg_volt"], marker="o", label="volt")
# # ax.plot(x, model_summary["avg_pressure"], marker="o", label="pressure")
# ax.plot(x, model_summary["avg_vibration"], marker="o", label="vibration")
# ax.set_title("Avg Sensors by Model")
# ax.set_ylabel("Volt / Pressure / Vibration")

# # 2. 副軸（右側）：繪製 rotate
# ax_rotate = ax.twinx()
# ax_rotate.plot(x, model_summary["avg_rotate"], marker="o", label="rotate", color="tab:red")
# ax_rotate.set_ylabel("Rotate (RPM)")

# # 3. 合併圖例並顯示
# lines_left, labels_left = ax.get_legend_handles_labels()
# lines_right, labels_right = ax_rotate.get_legend_handles_labels()
# ax.legend(lines_left + lines_right, labels_left + labels_right, loc="upper right")

# plt.tight_layout()
# plt.show()
# plt.close()
# %%
