# %%
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
result_path = BASE_DIR / "03_output" / "model_results.csv"

columns = [
    "method",
    "TP", "FP", "FN", "TN",
    "recall", "precision",
    "accuracy", "inspection_rate"
]

if not result_path.exists():
    pd.DataFrame(columns=columns).to_csv(
        result_path,
        index=False
    )

def save_result(method, TP, FP, FN, TN):

    df = pd.read_csv(result_path)
    # 同名方法先移除
    df = df[df["method"] != method]

    recall = TP / (TP + FN)
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    accuracy = (TP + TN) / (TP + FP + FN + TN)
    inspection_rate = (TP + FP) / (TP + FP + FN + TN)

    new_result = pd.DataFrame([{
        "method": method,
        "TP": TP,
        "FP": FP,
        "FN": FN,
        "TN": TN,
        "recall": recall,
        "precision": precision,
        "accuracy": accuracy,
        "inspection_rate": inspection_rate
    }])

    df = pd.concat(
        [df, new_result],
        ignore_index=True
    )

    df.to_csv(result_path, index=False)