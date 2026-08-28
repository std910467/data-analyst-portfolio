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

# top20=df_machine_summary.head(20).copy()
# print(top20["model"].value_counts())

plot_df = df_machine_summary.head(20).copy()
model_colors = {
    "model1": "#3B6CBA",
    "model2": "#55A868",
    "model3": "#C44E52",
    "model4": "#8172B3",
}

colors = plot_df["model"].map(model_colors)

plt.figure(figsize=(10, 6))
bars = plt.barh(
    plot_df["machineID"].astype(str),
    plot_df["total_failures"],
    color=colors
)
plt.gca().invert_yaxis()  # 故障最多的在上面

plt.xlabel("total_failures")
plt.ylabel("machineID")
plt.title("Top 20 Machines by Failures (color = model)")

# 圖例：依 model 建 proxy
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor=model_colors[m], label=m)
    for m in model_colors
    if m in set(plot_df["model"])
]
plt.legend(handles=legend_elements, title="model")

plt.tight_layout()
plt.savefig(BASE_DIR.parent / "05_outputs/03_machine_overview.png",
    dpi=300, 
    bbox_inches="tight", 
)
plt.close()
# %%
