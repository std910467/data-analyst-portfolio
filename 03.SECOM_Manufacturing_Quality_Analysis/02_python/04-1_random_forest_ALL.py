# %%
import pandas as pd
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from model_results import save_result
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

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

# 依照所有特徵都看。
x = df
y = labels["label"]

x_train, x_test, y_train, y_test = train_test_split(
    x, y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

# 補值 將nan 改成 訓練模型的中位數。
imputer = SimpleImputer(strategy="median")
x_train = pd.DataFrame(
    imputer.fit_transform(x_train),
    columns=x_train.columns,
    index=x_train.index
)

x_test = pd.DataFrame(
    imputer.transform(x_test),
    columns=x_test.columns,
    index=x_test.index
)

# 使用random_tree，先簡單創建100棵樹(n_estimators=100)
model_rf = RandomForestClassifier(
    n_estimators=100,
    # class_weight="balanced",
    max_depth=5,
    oob_score=True,
    random_state=42
)

model_rf.fit(x_train, y_train);
oob_prob = model_rf.oob_decision_function_[:, 1]
actual_fail = y_train == 1
pred_fail = oob_prob >= 0.5

TP = ( pred_fail &  actual_fail).sum()
FP = ( pred_fail & ~actual_fail).sum()
FN = (~pred_fail &  actual_fail).sum()
TN = (~pred_fail & ~actual_fail).sum()

recall = TP / (TP + FN)
precision = TP / (TP + FP)
inspection_rate = (TP + FP) / len(y_train)

print("TP:", TP, "FP:", FP, "FN:", FN, "TN:", TN)
print("Recall:", recall)
print("Precision:", precision)
print("Inspection Rate:", inspection_rate)

oob_result = pd.DataFrame({
    "actual": y_train.values,
    "prob": oob_prob
})

print(
    oob_result.groupby("actual")["prob"]
    .agg(["mean", "median", "min", "max"])
)
for threshold in np.arange(0.01, 0.051, 0.005):
    pred_fail = oob_prob >= threshold

    TP = ( pred_fail &  actual_fail).sum()
    FP = ( pred_fail & ~actual_fail).sum()
    FN = (~pred_fail &  actual_fail).sum()
    TN = (~pred_fail & ~actual_fail).sum()

    recall = TP / (TP + FN)
    inspection_rate = (TP + FP) / len(y_train)

    print(
        round(threshold, 2),
        round(recall, 3),
        round(inspection_rate, 3)
    )





y_prob = model_rf.predict_proba(x_train)
# 看一下模型訓練的對應y區分
# print(model_tree_final.classes_)
fail_prob = y_prob[:, 1]

threshold=0.5
actual_fail = y_train == 1
pred_fail = fail_prob >= threshold
TP = ( pred_fail  & actual_fail).sum()
FP = ( pred_fail  & ~actual_fail).sum()
FN = ( ~pred_fail & actual_fail).sum()
TN = ( ~pred_fail & ~actual_fail).sum()
recall = TP / (TP + FN)
precision = TP / (TP + FP) if (TP + FP) > 0 else 0
accuracy = (TP + TN) / (TP + FP + FN + TN)
inspection_rate = (TP + FP) / (TP + FP + FN + TN)
print(f"threshold：{threshold}")
print(f"TP：{TP}")
print(f"FP：{FP}")
print(f"FN：{FN}")
print(f"TN：{TN}")
print(f"Recall：{recall:.2%}")
print(f"Precision：{precision:.2%}")
print(f"accuracy：{accuracy:.2%}")
print(f"inspection_rate：{inspection_rate:.2%}")

train_result = pd.DataFrame({
    "actual": y_train,
    "fail_prob": fail_prob
})

print(
    train_result.groupby("actual")["fail_prob"]
    .agg(["mean", "median", "min", "max"])
)


y_prob = model_rf.predict_proba(x_test)
fail_prob = y_prob[:, 1]
threshold=0.5
actual_fail = y_test == 1
pred_fail = fail_prob >= threshold
TP = ( pred_fail  & actual_fail).sum()
FP = ( pred_fail  & ~actual_fail).sum()
FN = ( ~pred_fail & actual_fail).sum()
TN = ( ~pred_fail & ~actual_fail).sum()
recall = TP / (TP + FN)
precision = TP / (TP + FP) if (TP + FP) > 0 else 0
accuracy = (TP + TN) / (TP + FP + FN + TN)
inspection_rate = (TP + FP) / (TP + FP + FN + TN)
print(f"threshold：{threshold}")
print(f"TP：{TP}")
print(f"FP：{FP}")
print(f"FN：{FN}")
print(f"TN：{TN}")
print(f"Recall：{recall:.2%}")
print(f"Precision：{precision:.2%}")
print(f"accuracy：{accuracy:.2%}")
print(f"inspection_rate：{inspection_rate:.2%}")
print("max:", fail_prob.max())
print("min:", fail_prob.min())
print("mean:", fail_prob.mean())

save_result("random_forest_ALL", TP, FP, FN, TN)
# %%
