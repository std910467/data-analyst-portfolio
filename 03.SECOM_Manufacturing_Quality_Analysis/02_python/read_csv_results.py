# %%
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
result_path = BASE_DIR / "03_output" / "model_results.csv"

df = pd.read_csv(result_path)

print(df)
# 刪除特定資料列使用
# df = df[
#     df["method"] != "random_tree_ALL"
# ].reset_index(drop=True)
# df.to_csv(result_path, index=False)

# %%
