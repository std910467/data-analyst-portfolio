# %%
import pandas as pd
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from model_results import save_result
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

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

# 只看TOP3的特徵。
top3 = [59, 103, 510]
x = df[top3]
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

# 直接參考3-1_decision_tree，使用balanced，depth=3、leaf=40。
model_tree_final = DecisionTreeClassifier(
    min_samples_leaf=40,
    max_depth=3,
    class_weight="balanced",
    random_state=42
)

model_tree_final.fit(x_train, y_train);
y_prob = model_tree_final.predict_proba(x_train)

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

#Top3 Decision Tree 在預設 threshold 0.5 下，無法達到 90% Recall；
# 降低 threshold 雖可提高 Recall，但 Inspection Rate 大幅增加，因此不再進一步調整 threshold。


y_prob = model_tree_final.predict_proba(x_test)
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


save_result("decision_tree_TOP3", TP, FP, FN, TN)
# %%
