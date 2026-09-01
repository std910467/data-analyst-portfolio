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
   

# 計算近 3 天 (當天與前兩天) 的感測器平均值與 Error 累積總和。
df_daily[[f"{col}_roll3_mean" for col in sensor_cols]
         ] = df_daily.groupby("machineID")[sensor_cols].transform(
             lambda x: x.rolling(window=3, min_periods=1).mean())
df_daily[[f"{col}_roll3_sum"  for col in count_cols]
         ]  = df_daily.groupby("machineID")[count_cols].transform(
             lambda x: x.rolling(window=3, min_periods=1).sum())

# 將滾動統計值平移3天(Lag 3)，作為歷史對照組基準。
for col in sensor_cols:
    roll_col = f"{col}_roll3_mean"
    df_daily[f"{roll_col}_lag3"] = df_daily.groupby("machineID")[
        roll_col
    ].shift(3)
for col in count_cols:
    roll_col = f"{col}_roll3_sum"
    df_daily[f"{roll_col}_lag3"] = df_daily.groupby("machineID")[
        roll_col
    ].shift(3)



# 計算差異_sensor用增加比例
df_daily["volt_change"] = (
    df_daily["d_volt_roll3_mean"] - df_daily["d_volt_roll3_mean_lag3"]
    ) / df_daily["d_volt_roll3_mean_lag3"]
df_daily["rotate_change"] = (
    df_daily["d_rotate_roll3_mean"] - df_daily["d_rotate_roll3_mean_lag3"]
    ) / df_daily["d_rotate_roll3_mean_lag3"]
df_daily["pressure_change"] = (
    df_daily["d_pressure_roll3_mean"] - df_daily["d_pressure_roll3_mean_lag3"]
    ) / df_daily["d_pressure_roll3_mean_lag3"]
df_daily["vibration_change"] = (
    df_daily["d_vibration_roll3_mean"]- df_daily["d_vibration_roll3_mean_lag3"]
    ) / df_daily["d_vibration_roll3_mean_lag3"]

# 計算差異_error用增加數量
df_daily["error1_change"] = (
    df_daily["error1_times_roll3_sum"] - df_daily["error1_times_roll3_sum_lag3"])
df_daily["error2_change"] = (
    df_daily["error2_times_roll3_sum"] - df_daily["error2_times_roll3_sum_lag3"])
df_daily["error3_change"] = (
    df_daily["error3_times_roll3_sum"] - df_daily["error3_times_roll3_sum_lag3"])
df_daily["error4_change"] = (
    df_daily["error4_times_roll3_sum"] - df_daily["error4_times_roll3_sum_lag3"])
df_daily["error5_change"] = (
    df_daily["error5_times_roll3_sum"] - df_daily["error5_times_roll3_sum_lag3"])

#手動運算區：檢查 標準差、平均值、中位數
if False:
    text_target = "volt_change"
    mean_val = df_daily[text_target].mean()
    std_val = df_daily[text_target].std()
    median_val = df_daily[text_target].median()
    print(f"平均值: {mean_val:.4f}")
    print(f"標準差: {std_val:.4f}")
    print(f"中位數: {median_val:.4f}")


# 設定預警條件
# comp1
df_daily["warning_comp1"] = (df_daily["volt_change"] > 0.04
                             ) & (df_daily["error1_change"]>0.5)
# comp2
df_daily["warning_comp2"] = (df_daily["rotate_change"] < -0.044
                             ) & ((df_daily["error2_change"]>0.5) | (df_daily["error3_change"]>0.5))
# comp3
df_daily["warning_comp3"] = (df_daily["pressure_change"] > 0.055
                             ) & (df_daily["error4_change"]>0.5)
# comp4
df_daily["warning_comp4"] = (df_daily["vibration_change"] > 0.05
                             ) & (df_daily["error5_change"]>0.5)

# 預警結果統計
results = []
for comp in ["comp1", "comp2", "comp3", "comp4"]:
    warning_col = f"warning_{comp}"
    failure_col = f"{comp}_failure"

    # 計算統計指標
    total_warnings = df_daily[warning_col].sum()
    total_failures = df_daily[failure_col].sum()

    # 有發出預警後未來 2 天內確實有故障產生 (1)
    fail_next_1 = df_daily.groupby("machineID")[failure_col].shift(-1).fillna(0) >0
    fail_next_2 = df_daily.groupby("machineID")[failure_col].shift(-2).fillna(0) >0
    df_daily["future_failure"] = fail_next_1| fail_next_2    
    hits = df_daily[df_daily[warning_col] & df_daily["future_failure"]
                    ].shape[0]
    precision = (hits / total_warnings * 100) if total_warnings > 0 else 0

    # 故障前兩天是否有告警
    warn_prev_1 = df_daily.groupby("machineID")[warning_col].shift(1).fillna(False)
    warn_prev_2 = df_daily.groupby("machineID")[warning_col].shift(2).fillna(False)
    has_prior_warning = warn_prev_1 | warn_prev_2
    recall_hits = df_daily[(df_daily[failure_col]>0) & has_prior_warning
                           ].shape[0]
    recall = (recall_hits / total_failures * 100) if total_failures > 0 else 0

    f1_score = ((2 * precision * recall) / (precision + recall)
                if (precision + recall) > 0
                else 0
                )

    results.append(
        {
            "component": comp,
            "warnings": total_warnings,
            "warnings_hits": hits,
            "precision": round(precision, 2),
            "failure": total_failures,
            "failure_hits": recall_hits,
            "recall": round(recall, 2),
            "f1_score": round(f1_score, 2),
        }
    )

result_df = pd.DataFrame(results)

# 輸出CSV檔案 給BI使用
result_df.to_csv(
    BASE_DIR.parent / "05_outputs/06_comp_warning_performance.csv",
    index=False,
    encoding="utf-8-sig"
)

df_plot = result_df.set_index("component")[["precision", "recall", "f1_score"]]
plt.figure(figsize=(10, 6))
ax = df_plot.plot(
    kind="bar",
    width=0.8  
)
plt.title("Failure Prediction Performance by Component", fontsize=14)
plt.xlabel("Component")
plt.ylabel("Score (%)")
plt.ylim(0,120)
plt.xticks(rotation=0)
for container in ax.containers:
    ax.bar_label(container, fmt="%.1f%%", padding=2)
plt.tight_layout()
plt.savefig(
    BASE_DIR.parent / "05_outputs/06_failure_prediction_performance_by_component.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()


# %%
