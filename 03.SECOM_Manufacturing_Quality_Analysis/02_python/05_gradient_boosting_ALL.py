# %%
import pandas as pd
from pathlib import Path
import numpy as np
from model_results import save_result
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.ensemble import GradientBoostingClassifier

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
# 從原 Train 再切出 20% 作為 Validation，用於參數與 threshold 選擇
x_train, x_val, y_train, y_val = train_test_split(
    x_train, y_train,
    test_size=0.2,
    stratify=y_train,
    random_state=42
)


# 補值 將nan 改成 訓練模型的中位數。
imputer = SimpleImputer(strategy="median")
x_train = pd.DataFrame(
    imputer.fit_transform(x_train),
    columns=x_train.columns,
    index=x_train.index
)
x_val = pd.DataFrame(
    imputer.transform(x_val),
    columns=x_val.columns,
    index=x_val.index
)

x_test = pd.DataFrame(
    imputer.transform(x_test),
    columns=x_test.columns,
    index=x_test.index
)

# Gradient Boosting 參數選定：
# 將原 Train 再切分 Training / Validation，使用 Validation 進行參數與 threshold 選擇，
# 並以 Recall >= 90% 為條件，比較不同設定下的 Inspection Rate。
# 測試 max_depth=1、2、3 後，max_depth=2 的高 Recall / Inspection Rate 表現較佳；
# 再比較 learning_rate=0.05、0.1、0.2，以 0.05 表現較佳；
# 最後比較 n_estimators=50、100、200，以 100 棵的結果較佳。
# 最終採用 max_depth=2、learning_rate=0.05、n_estimators=100。
# Validation threshold 掃描後選定 0.035（Recall=94.1%、Inspection Rate=70.1%），
# 固定模型參數與 threshold 後，再進行最終 Test 評估。
model_gb = GradientBoostingClassifier(
    n_estimators=100,
    learning_rate=0.05,
    max_depth=2,
    random_state=42
)

model_gb.fit(x_train, y_train);

val_prob = model_gb.predict_proba(x_val)
fail_prob = val_prob[:, 1]
actual_fail = y_val == 1
pred_fail = fail_prob >= 0.5

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


threshold_list = np.arange(0.01, 0.101, 0.005)

for threshold in threshold_list:
    pred_fail = fail_prob >= threshold
    actual_fail = y_val == 1

    TP = (pred_fail & actual_fail).sum()
    FP = (pred_fail & ~actual_fail).sum()
    FN = (~pred_fail & actual_fail).sum()
    TN = (~pred_fail & ~actual_fail).sum()

    recall = TP / (TP + FN)
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    inspection_rate = (TP + FP) / len(y_val)

    print(
        round(threshold, 3),
        "Recall:", round(recall, 3),
        "Precision:", round(precision, 3),
        "Inspection:", round(inspection_rate, 3)
    )


y_prob = model_gb.predict_proba(x_test)
fail_prob = y_prob[:, 1]
threshold=0.035
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


save_result("gradient_boosting_all", TP, FP, FN, TN)
# %%
