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

df_daily = read_table("int_daily_machine_summary")
df_daily.head()
df_daily["date"] = pd.to_datetime(df_daily["date"])

comp2_events = df_daily[df_daily["comp2_failure"] > 0][["machineID", "date"]].sort_values(["machineID", "date"])
comp2_events["prev_date"] = comp2_events.groupby("machineID")["date"].shift(1)
comp2_events["days_diff"] = (comp2_events["date"] - comp2_events["prev_date"]).dt.days
# comp2_events["days_diff"].min()

sensor_cols = ["d_volt", "d_rotate", "d_pressure", "d_vibration"] 
count_cols = ["error1_times", "error2_times", "error3_times", "error4_times", "error5_times"]     

exp_records = []
ctl_records = []
for _, row in comp2_events.iterrows():
    m_id = row["machineID"]
    f_date = row["date"]

    # 實驗組 (T-1 ~ T-3)
    exp_mask = (df_daily["machineID"] == m_id) & \
               (df_daily["date"] >= f_date - pd.Timedelta(days=3)) & \
               (df_daily["date"] <= f_date - pd.Timedelta(days=1))
    
    # 對照組 (T-4 ~ T-6)
    ctl_mask = (df_daily["machineID"] == m_id) & \
               (df_daily["date"] >= f_date - pd.Timedelta(days=6)) & \
               (df_daily["date"] <= f_date - pd.Timedelta(days=4))

    def summarize(df):
        sensors = df[sensor_cols].mean()
        counts = df[count_cols].sum()
        return pd.concat([sensors, counts])
    
    exp_records.append(summarize(df_daily[exp_mask]))
    ctl_records.append(summarize(df_daily[ctl_mask]))

df_exp = pd.DataFrame(exp_records)
df_ctl = pd.DataFrame(ctl_records)

df_exp.head()
df_ctl.head()

((df_exp[sensor_cols]- df_ctl[sensor_cols ]) / df_ctl[sensor_cols ]).mean()

# 計算變化幅度sensor用變化率、error用平均數的差異。
delta_sensor = ((df_exp[sensor_cols].mean() - df_ctl[sensor_cols ].mean()) / df_ctl[sensor_cols ].mean()) * 100
delta_error = (df_exp[count_cols].mean() - df_ctl[count_cols].mean())
delta_sensor.index = ["volt", "rotate", "pressure", "vibration"]
delta_error.index = ["error1", "error2", "error3", "error4", "error5"]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# --- Left Plot: Sensor Change Rate (%) ---
# Use crimson for drop/negative change, royalblue for increase
sensor_colors = [
    "crimson" if val < 0 else "royalblue" for val in delta_sensor.values
]
bars1 = ax1.bar(delta_sensor.index, delta_sensor.values, color=sensor_colors)
ax1.set_title("Sensors: Pre-Failure Change Rate (%)", fontsize=12, pad=10)
ax1.set_ylabel("Change (%)", fontsize=10)
max_abs_val = delta_sensor.abs().max()

ax1.set_ylim(-max_abs_val*1.2 ,max_abs_val*1.2)
ax1.axhline(0, color="black", linestyle="--", linewidth=0.8)  # 0% baseline
ax1.grid(axis="y", linestyle=":", alpha=0.5)

# Add numeric value labels on bars
for bar in bars1:
    yval = bar.get_height()
    va = "bottom" if yval >= 0 else "top"
    ax1.text(
        bar.get_x() + bar.get_width() / 2,
        yval,
        f"{yval:.1f}%",
        ha="center",
        va=va,
        fontsize=9,
    )

# --- Right Plot: Error Count Increase ---
bars2 = ax2.bar(delta_error.index, delta_error.values, color="darkorange")

ax2.set_title(
    "Errors: Pre-Failure Avg error Increase", fontsize=12, pad=10
)
ax2.set_ylabel("Avg error Increase", fontsize=10)
ax2.grid(axis="y", linestyle=":", alpha=0.5)

# Add numeric value labels on bars
for bar in bars2:
    yval = bar.get_height()
    ax2.text(
        bar.get_x() + bar.get_width() / 2,
        yval + 0.01,
        f"+{yval:.2f}",
        ha="center",
        va="bottom",
        fontsize=9,
    )

plt.tight_layout()
plt.savefig(
    BASE_DIR.parent / "05_outputs/05_pre_comp2_failure_Change.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()

# %%
