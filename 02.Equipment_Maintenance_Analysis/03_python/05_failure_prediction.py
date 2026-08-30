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


comp1_events = df_daily[df_daily["comp1_failure"] > 0][["machineID", "date"]].sort_values(["machineID", "date"])
comp2_events = df_daily[df_daily["comp2_failure"] > 0][["machineID", "date"]].sort_values(["machineID", "date"])
comp3_events = df_daily[df_daily["comp3_failure"] > 0][["machineID", "date"]].sort_values(["machineID", "date"])
comp4_events = df_daily[df_daily["comp4_failure"] > 0][["machineID", "date"]].sort_values(["machineID", "date"])

# 測試同類型故障時間有沒有低於7天內再發生(因為我要分3天、3天兩組)，結論都沒有，最短的comp4也相差14天。
# df_test_diff = comp4_events 
# df_test_diff["prev_date"] = df_test_diff.groupby("machineID")["date"].shift(1)
# df_test_diff["days_diff"] = (df_test_diff["date"] - df_test_diff["prev_date"]).dt.days
# df_test_diff["days_diff"].min()

# 設定要計算的欄位，sensor_cols是取平均，count_cols是用總和。 
sensor_cols = ["d_volt", "d_rotate", "d_pressure", "d_vibration"] 
count_cols = ["error1_times", "error2_times", "error3_times", "error4_times", "error5_times"]     

def get_exp_ctl_dfs(
    df_daily, 
    event_df,
    sensor_cols,
    count_cols,
    ):
    exp_records = []
    ctl_records = []

    def summarize(df):
        sensors = df[sensor_cols].mean()
        counts = df[count_cols].sum()
        return pd.concat([sensors, counts])

    for _, row in event_df.iterrows():
        m_id = row["machineID"]
        f_date = row["date"]

        # 實驗組 (T-1 ~ T-3)
        exp_mask = (
            (df_daily["machineID"] == m_id)
            & (df_daily["date"] >= f_date - pd.Timedelta(days=3))
            & (df_daily["date"] <= f_date - pd.Timedelta(days=1))
        )

        # 對照組 (T-4 ~ T-6)
        ctl_mask = (
            (df_daily["machineID"] == m_id)
            & (df_daily["date"] >= f_date - pd.Timedelta(days=6))
            & (df_daily["date"] <= f_date - pd.Timedelta(days=4))
        )

        exp_records.append(summarize(df_daily[exp_mask]))
        ctl_records.append(summarize(df_daily[ctl_mask]))

    df_exp = pd.DataFrame(exp_records).reset_index(drop=True)
    df_ctl = pd.DataFrame(ctl_records).reset_index(drop=True)

    return df_exp, df_ctl



comp1_exp , comp1_ctl = get_exp_ctl_dfs(df_daily,comp1_events,sensor_cols,count_cols)
comp2_exp, comp2_ctl = get_exp_ctl_dfs(df_daily, comp2_events, sensor_cols, count_cols)
comp3_exp, comp3_ctl = get_exp_ctl_dfs(df_daily, comp3_events, sensor_cols, count_cols)
comp4_exp, comp4_ctl = get_exp_ctl_dfs(df_daily, comp4_events, sensor_cols, count_cols)

# 計算所有comp1~4故障前變化幅度，sensor用變化率、error使用所有差異的平均。
comp1_sensor_diff = ((comp1_exp[sensor_cols].mean() - comp1_ctl[sensor_cols].mean()) 
                     / comp1_ctl[sensor_cols].mean()) * 100
comp1_error_diff = (comp1_exp[count_cols] - comp1_ctl[count_cols]).mean()

comp2_sensor_diff = ((comp2_exp[sensor_cols].mean() - comp2_ctl[sensor_cols].mean())
                     / comp2_ctl[sensor_cols].mean()) * 100
comp2_error_diff = (comp2_exp[count_cols] - comp2_ctl[count_cols]).mean()

comp3_sensor_diff = ((comp3_exp[sensor_cols].mean() - comp3_ctl[sensor_cols].mean())
                     / comp3_ctl[sensor_cols].mean()) * 100
comp3_error_diff = (comp3_exp[count_cols] - comp3_ctl[count_cols]).mean()

comp4_sensor_diff = ((comp4_exp[sensor_cols].mean() - comp4_ctl[sensor_cols].mean())
                     / comp4_ctl[sensor_cols].mean()) * 100
comp4_error_diff = (comp4_exp[count_cols] - comp4_ctl[count_cols]).mean()

sensor_labels = ["volt", "rotate", "pressure", "vibration"]
error_labels = ["error1", "error2", "error3", "error4", "error5"]
comp1_sensor_diff.index = sensor_labels
comp1_error_diff.index = error_labels
comp2_sensor_diff.index = sensor_labels
comp2_error_diff.index = error_labels
comp3_sensor_diff.index = sensor_labels
comp3_error_diff.index = error_labels
comp4_sensor_diff.index = sensor_labels
comp4_error_diff.index = error_labels

# 畫圖用
fig, axes = plt.subplots(4, 2, figsize=(12, 16) ,sharey="col")

# --- Comp1 ---
axes[0, 0].bar(
    comp1_sensor_diff.index, comp1_sensor_diff.values, color="skyblue"
)
axes[0, 0].axhline(0, color="red", linestyle="--")
axes[0, 0].set_title("Comp1 - Sensor Diff (%)")
axes[0, 0].tick_params(axis="x", rotation=15)

axes[0, 1].bar(
    comp1_error_diff.index, comp1_error_diff.values, color="orange"
)
axes[0, 1].axhline(0, color="red", linestyle="--")
axes[0, 1].set_title("Comp1 - Error Diff (Mean Count)")
axes[0, 1].tick_params(axis="x", rotation=15)

# --- Comp2 ---
axes[1, 0].bar(
    comp2_sensor_diff.index, comp2_sensor_diff.values, color="skyblue"
)
axes[1, 0].axhline(0, color="red", linestyle="--")
axes[1, 0].set_title("Comp2 - Sensor Diff (%)")
axes[1, 0].tick_params(axis="x", rotation=15)

axes[1, 1].bar(
    comp2_error_diff.index, comp2_error_diff.values, color="orange"
)
axes[1, 1].axhline(0, color="red", linestyle="--")
axes[1, 1].set_title("Comp2 - Error Diff (Mean Count)")
axes[1, 1].tick_params(axis="x", rotation=15)

# --- Comp3 ---
axes[2, 0].bar(
    comp3_sensor_diff.index, comp3_sensor_diff.values, color="skyblue"
)
axes[2, 0].axhline(0, color="red", linestyle="--")
axes[2, 0].set_title("Comp3 - Sensor Diff (%)")
axes[2, 0].tick_params(axis="x", rotation=15)

axes[2, 1].bar(
    comp3_error_diff.index, comp3_error_diff.values, color="orange"
)
axes[2, 1].axhline(0, color="red", linestyle="--")
axes[2, 1].set_title("Comp3 - Error Diff (Mean Count)")
axes[2, 1].tick_params(axis="x", rotation=15)

# --- Comp4 ---
axes[3, 0].bar(
    comp4_sensor_diff.index, comp4_sensor_diff.values, color="skyblue"
)
axes[3, 0].axhline(0, color="red", linestyle="--")
axes[3, 0].set_title("Comp4 - Sensor Diff (%)")
axes[3, 0].tick_params(axis="x", rotation=15)

axes[3, 1].bar(
    comp4_error_diff.index, comp4_error_diff.values, color="orange"
)
axes[3, 1].axhline(0, color="red", linestyle="--")
axes[3, 1].set_title("Comp4 - Error Diff (Mean Count)")
axes[3, 1].tick_params(axis="x", rotation=15)

plt.tight_layout()
plt.savefig(
    BASE_DIR.parent / "05_outputs/05_pre_failure_Change.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()

# %%
