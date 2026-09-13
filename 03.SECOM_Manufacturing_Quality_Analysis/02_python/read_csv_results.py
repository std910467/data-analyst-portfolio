# %%
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
result_path = BASE_DIR / "03_output" / "model_results.csv"

df = pd.read_csv(result_path)
print(df)

