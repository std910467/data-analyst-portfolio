# %%
import pandas as pd
from pathlib import Path
import numpy as np
from model_results import save_result
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
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

# Random Forest 參數選定：
# 使用 OOB 作為內部驗證，以 Recall >= 90% 為條件，比較不同參數下的 Inspection Rate。
# 測試 max_depth、min_samples_leaf、max_features 後，
# 最終採用 min_samples_leaf=10、max_features="sqrt"；
# n_estimators 提高至 500 以增加模型穩定性。
# OOB threshold 掃描後選定 0.045（Recall=92.8%、Inspection Rate=71.1%），
# 固定模型參數與 threshold 後，再進行最終 Test 評估。
model_rf = RandomForestClassifier(
    n_estimators=500,
    min_samples_leaf=10,
    max_features="sqrt",
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
precision = TP / (TP + FP) if (TP + FP) > 0 else 0
inspection_rate = (TP + FP) / (TP + FP + FN + TN)

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
    inspection_rate = (TP + FP) / (TP + FP + FN + TN)

    print(
        round(threshold, 3),
        round(recall, 3),
        round(inspection_rate, 3)
    )

y_prob = model_rf.predict_proba(x_test)
fail_prob = y_prob[:, 1]
threshold=0.045
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


save_result("random_forest_all", TP, FP, FN, TN)
# %%
