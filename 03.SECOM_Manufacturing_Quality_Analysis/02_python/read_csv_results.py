# %%
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
result_path = BASE_DIR / "03_output" / "model_results.csv"

df = pd.read_csv(result_path)

print(df)


# Model 名稱調整，讓圖表比較好閱讀
name_map = {
    "rule_based_top3": "Rule-Based Top3",
    "logistic_regression_top3": "Logistic Top3",
    "logistic_balance_top3": "Logistic Balanced Top3",
    "logistic_balance_all": "Logistic Balanced All",
    "decision_tree_all": "Decision Tree All",
    "decision_tree_top3": "Decision Tree Top3",
    "random_forest_all": "Random Forest All",
    "gradient_boosting_all": "Gradient Boosting All"
}

df["model_name"] = df["method"].map(name_map)
# 轉成百分比
df["recall_pct"] = df["recall"] * 100
df["inspection_pct"] = df["inspection_rate"] * 100


# 畫圖
fig, ax = plt.subplots(figsize=(10, 7))

ax.scatter(
    df["inspection_pct"],
    df["recall_pct"],
    s=80
)
label_offsets = {
    "Rule-Based Top3": (8, 0),
    "Logistic Top3": (8, -2),
    "Logistic Balanced Top3": (8, 0),
    "Logistic Balanced All": (8, 5),
    "Decision Tree All": (8, 5),
    "Decision Tree Top3": (8, 5),
    "Random Forest All": (8, 6),
    "Gradient Boosting All": (8, 5)
}

for _, row in df.iterrows():

    offset = label_offsets[row["model_name"]]

    ax.annotate(
        row["model_name"],
        (row["inspection_pct"], row["recall_pct"]),
        xytext=offset,
        textcoords="offset points",
        fontsize=9
    )


ax.set_xlabel("Inspection Rate (%)")
ax.set_ylabel("Recall (%)")
ax.set_title("Model Comparison: Recall vs Inspection Rate")

ax.set_xlim(0, 100)
ax.set_ylim(0, 105)

ax.grid(alpha=0.3)

plt.tight_layout()


# 儲存圖片
output_path = BASE_DIR / "03_output" / "model_comparison.png"
plt.savefig(output_path, dpi=300, bbox_inches="tight")

plt.show()
# 刪除特定資料列使用
# df = df[
#     df["method"] != "random_tree_ALL"
# ].reset_index(drop=True)
# df.to_csv(result_path, index=False)

# %%
