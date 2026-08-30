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
df_daily["date"] = pd.to_datetime(df_daily["date"])
# df_daily.dtypes
# df_daily.head()

df_daily = df_daily.sort_values(["machineID", "date"]).reset_index(drop=True)
sensor_cols = ["d_volt", "d_rotate", "d_pressure", "d_vibration"] 
count_cols = ["error1_times", "error2_times", "error3_times", "error4_times", "error5_times"]     
   


df_daily[[f"{col}_roll3_mean" for col in sensor_cols]
         ] = df_daily.groupby("machineID")[sensor_cols].transform(
             lambda x: x.rolling(window=3, min_periods=1).mean())
df_daily[[f"{col}_roll3_sum"  for col in count_cols]
         ]  = df_daily.groupby("machineID")[count_cols].transform(
             lambda x: x.rolling(window=3, min_periods=1).sum())

df_daily["d_rotate_roll3_lag3"] = df_daily.groupby("machineID")[
    "d_rotate_roll3_mean"].shift(3)
df_daily["error2_times_roll3_lag3"] = df_daily.groupby("machineID")[
    "error2_times_roll3_sum"].shift(3)
df_daily["error3_times_roll3_lag3"] = df_daily.groupby("machineID")[
    "error3_times_roll3_sum"].shift(3)


# 設定預警條件
cond_rotate = (df_daily["d_rotate_roll3_mean"]-df_daily["d_rotate_roll3_lag3"]
               )/df_daily["d_rotate_roll3_lag3"] < -0.05
cond_error2 = df_daily["error2_times_roll3_sum"]-df_daily["error2_times_roll3_lag3"] > 0
cond_error3 = df_daily["error3_times_roll3_sum"]-df_daily["error3_times_roll3_lag3"] > 0
# df_daily["warning_signal"] = cond_rotate & cond_error2 & cond_error3
# 另一種只要error2或3有告警就警示。
df_daily["warning_signal"] = cond_rotate & (cond_error2 | cond_error3)

#載入後2天comp2_fail的狀況
df_daily["comp2_fail_next1"] = df_daily.groupby("machineID")[
    "comp2_failure"
].shift(-1)
df_daily["comp2_fail_next2"] = df_daily.groupby("machineID")[
    "comp2_failure"
].shift(-2)

# 未來2天內只要有任何一天故障就算 True
df_daily["comp2_fail_in_next_2days"] = (df_daily["comp2_fail_next1"] > 0) | (
    df_daily["comp2_fail_next2"] > 0)

#  前2天內只要有任何一天警告就算True
df_daily["warn_in_past_2days"] = (
    df_daily.groupby("machineID")["warning_signal"].shift(1) == True) | (
        df_daily.groupby("machineID")["warning_signal"].shift(2) == True)

# 3. 所有觸發警報的列進行統計
warnings = df_daily[df_daily["warning_signal"] == True]
failures = df_daily[df_daily["comp2_failure"] > 0]
total_failures = failures["comp2_failure"].count()
caught = failures["warn_in_past_2days"].sum()


total_warnings = len(warnings)
hits = warnings["comp2_fail_in_next_2days"].sum()
precision = (hits / total_warnings) * 100 if total_warnings > 0 else 0
recall = (
    (caught/ total_failures) * 100 if total_failures > 0 else 0
)

# print(f"總警報次數 (Total Warnings) : {total_warnings}")
# print(f"成功預測到故障次數 (Hits)   : {hits}")
# print(f"預警精準度 (Precision)      : {precision:.2f}%")
# print(f"覆蓋率(recall)      : {recall:.2f}%")

metrics = ["Precision", "Recall"]
values = [precision, recall]

# 畫圖
plt.figure()
plt.bar(metrics, values)

plt.title("Failure Prediction Performance (comp2)")
for i, v in enumerate(values):
    plt.text(i, v + 1, f"{v:.2f}%", ha='center')

plt.ylabel("Percentage (%)")
plt.ylim(0, 100)
plt.savefig(
    BASE_DIR.parent / "05_outputs/06_comp2_warning_performance.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()


# %%
