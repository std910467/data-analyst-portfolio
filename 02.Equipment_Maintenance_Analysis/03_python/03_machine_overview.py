#%%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.colors as colors
import numpy as np
from matplotlib.patches import Patch
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

# region  前20名故障數機器橫條圖，以及故障零件堆疊橫條圖
plot_df = df_machine_summary.head(20).copy()
plot_df["machineID"] = plot_df["machineID"].astype(str)
plot_df = plot_df.sort_values("total_failures", ascending=True)
model_colors = {
    "model1": "#1f77b4",  
    "model2": "#ff7f0e",  
    "model3": "#2ca02c",  
    "model4": "#9467bd",  
}
model_bar_colors = plot_df["model"].map(model_colors)
comp_colors = {
    "comp1": "#8c564b",  # 棕
    "comp2": "#e377c2",  # 粉
    "comp3": "#7f7f7f",  # 灰
    "comp4": "#bcbd22",  # 橄欖
}

comps = ["comp1_failure", "comp2_failure", "comp3_failure", "comp4_failure"]
comp_labels = ["comp1", "comp2", "comp3", "comp4"]
comp_colors = [comp_colors["comp1"],comp_colors["comp2"],comp_colors["comp3"],comp_colors["comp4"]]

fig, axes = plt.subplots(1, 2, figsize=(14, 7), sharey=True)

# 左：總故障（顏色 = model）
axes[0].barh(plot_df["machineID"], plot_df["total_failures"], color=model_bar_colors)
axes[0].set_xlabel("total_failures")
axes[0].set_title("Top 20 by Total Failures")
axes[0].legend(
    handles=[Patch(facecolor=model_colors[m], label=m)
             for m in model_colors if m in set(plot_df["model"])],
    title="model",
    loc="lower right",
)

# 右：零件堆疊
left = np.zeros(len(plot_df))
for col, lab, c in zip(comps, comp_labels, comp_colors):
    axes[1].barh(plot_df["machineID"], plot_df[col], left=left, color=c, label=lab)
    left += plot_df[col].values

axes[1].set_xlabel("failures")
axes[1].set_title("Failure Breakdown by Component")
axes[1].legend(title="component", loc="lower right")

plt.tight_layout()
plt.savefig(BASE_DIR.parent / "05_outputs/03_machine_overview.png",
    dpi=300, 
    bbox_inches="tight", 
)
plt.close()
# endregion

# %%
