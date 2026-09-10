# %%
import pandas as pd
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from model_results import save_result

# 檔案路徑
BASE_DIR = Path(__file__).resolve().parent
df = pd.read_csv(
    BASE_DIR.parent / "01_raw_data/secom.data",
    sep=r"\s+",
    header=None
)

labels = pd.read_csv(
    BASE_DIR.parent /"01_raw_data/secom_labels.data",
    sep=r"\s+",
    header=None)

labels.columns = ["label","timestamp"]

# 移除特徵無變化的欄位(有116欄)
constant_cols = [
    col for col in df.columns
    if df[col].nunique() <= 1]
len(constant_cols)
df = df.drop(columns=constant_cols)




# save_result("Rule-Based", TP, FP, FN, TN)