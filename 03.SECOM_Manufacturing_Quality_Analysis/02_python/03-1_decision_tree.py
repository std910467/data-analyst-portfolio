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

# 使用一般決策樹，參數用預設
model_tree = DecisionTreeClassifier(
    random_state=42
)
model_tree.fit(x_train, y_train);


y_pred = model_tree.predict(x_test)
actual_fail = y_test == 1
pred_fail = y_pred == 1

TP = (pred_fail & actual_fail).sum()
FP = (pred_fail & ~actual_fail).sum()
FN = (~pred_fail & actual_fail).sum()
TN = (~pred_fail & ~actual_fail).sum()
recall = TP / (TP + FN)
precision = TP / (TP + FP)
accuracy = (TP + TN) / (TP + FP + FN + TN)
inspection_rate = (TP + FP) / (TP + FP + FN + TN)

print(f"depth：{model_tree.get_depth()}")
print(f"leaves：{model_tree.get_n_leaves()}")
print(f"TP：{TP}")
print(f"FP：{FP}")
print(f"FN：{FN}")
print(f"TN：{TN}")
print(f"Recall：{recall:.2%}")
print(f"Precision：{precision:.2%}")
print(f"accuracy：{accuracy:.2%}")
print(f"inspection_rate：{inspection_rate:.2%}")


# 使用balanced決策樹，因為資料的label種類數量極不平均
model_tree_balanced = DecisionTreeClassifier(
    class_weight="balanced",
    random_state=42
)
model_tree_balanced.fit(x_train, y_train);

y_pred = model_tree_balanced.predict(x_test)
actual_fail = y_test == 1
pred_fail = y_pred == 1

TP = (pred_fail & actual_fail).sum()
FP = (pred_fail & ~actual_fail).sum()
FN = (~pred_fail & actual_fail).sum()
TN = (~pred_fail & ~actual_fail).sum()
recall = TP / (TP + FN)
precision = TP / (TP + FP)
accuracy = (TP + TN) / (TP + FP + FN + TN)
inspection_rate = (TP + FP) / (TP + FP + FN + TN)

print(f"depth：{model_tree_balanced.get_depth()}")
print(f"leaves：{model_tree_balanced.get_n_leaves()}")
print(f"TP：{TP}")
print(f"FP：{FP}")
print(f"FN：{FN}")
print(f"TN：{TN}")
print(f"Recall：{recall:.2%}")
print(f"Precision：{precision:.2%}")
print(f"accuracy：{accuracy:.2%}")
print(f"inspection_rate：{inspection_rate:.2%}")

#測試各種深度的recall
result=[]
for depth in [2, 3, 5, 8, 10, 15, 20]:
    model = DecisionTreeClassifier(
        max_depth=depth,
        class_weight="balanced",
        random_state=42
    )
    model.fit(x_train,y_train);
    #用train資料計算一下
    y_pred = model.predict(x_train)
    actual_fail = y_train == 1
    pred_fail = y_pred == 1
    t_TP = (pred_fail & actual_fail).sum()
    t_FP = (pred_fail & ~actual_fail).sum()
    t_FN = (~pred_fail & actual_fail).sum()
    t_TN = (~pred_fail & ~actual_fail).sum()
    t_recall = t_TP / (t_TP + t_FN)
    t_precision = t_TP / (t_TP + t_FP)
    t_accuracy = (t_TP + t_TN) / (t_TP + t_FP + t_FN + t_TN)
    t_inspection_rate = (t_TP + t_FP) / (t_TP + t_FP + t_FN + t_TN)

    #用test資料測試
    y_pred = model.predict(x_test)
    actual_fail = y_test == 1
    pred_fail = y_pred == 1
    TP = (pred_fail & actual_fail).sum()
    FP = (pred_fail & ~actual_fail).sum()
    FN = (~pred_fail & actual_fail).sum()
    TN = (~pred_fail & ~actual_fail).sum()
    recall = TP / (TP + FN)
    precision = TP / (TP + FP)
    accuracy = (TP + TN) / (TP + FP + FN + TN)
    inspection_rate = (TP + FP) / (TP + FP + FN + TN)
    result.append({
            "max_depth": depth,
            "TP": TP,
            "FP": FP,
            "FN": FN,
            "TN": TN,
            "t_recall": t_recall,
            "recall": recall,
            "precision": precision,
            "accuracy":accuracy,
            "inspection_rate": inspection_rate
        })
depth_result = pd.DataFrame(result)

#測試各種節點(leaf)的recall
result=[]
for leaf_list  in [1, 2, 5, 10, 20, 30, 50]:
    model = DecisionTreeClassifier(
        min_samples_leaf=leaf_list,
        class_weight="balanced",
        random_state=42
    )
    model.fit(x_train,y_train);
    #用train資料計算一下
    y_pred = model.predict(x_train)
    actual_fail = y_train == 1
    pred_fail = y_pred == 1
    t_TP = (pred_fail & actual_fail).sum()
    t_FP = (pred_fail & ~actual_fail).sum()
    t_FN = (~pred_fail & actual_fail).sum()
    t_TN = (~pred_fail & ~actual_fail).sum()
    t_recall = t_TP / (t_TP + t_FN)
    t_precision = t_TP / (t_TP + t_FP)
    t_accuracy = (t_TP + t_TN) / (t_TP + t_FP + t_FN + t_TN)
    t_inspection_rate = (t_TP + t_FP) / (t_TP + t_FP + t_FN + t_TN)

    #用test資料測試
    y_pred = model.predict(x_test)
    actual_fail = y_test == 1
    pred_fail = y_pred == 1
    TP = (pred_fail & actual_fail).sum()
    FP = (pred_fail & ~actual_fail).sum()
    FN = (~pred_fail & actual_fail).sum()
    TN = (~pred_fail & ~actual_fail).sum()
    recall = TP / (TP + FN)
    precision = TP / (TP + FP)
    accuracy = (TP + TN) / (TP + FP + FN + TN)
    inspection_rate = (TP + FP) / (TP + FP + FN + TN)
    result.append({
            "min_leaf": leaf_list,
            "TP": TP,
            "FP": FP,
            "FN": FN,
            "TN": TN,
            "t_recall": t_recall,
            "recall": recall,
            "precision": precision,
            "accuracy":accuracy,
            "inspection_rate": inspection_rate
        })
leaf_result = pd.DataFrame(result)



model_tree_leaf20 = DecisionTreeClassifier(
    class_weight="balanced",
    min_samples_leaf=20,
    random_state=42
)
model_tree_leaf20.fit(x_train, y_train);

y_pred = model_tree_leaf20.predict(x_test)
actual_fail = y_test == 1
pred_fail = y_pred == 1

TP = (pred_fail & actual_fail).sum()
FP = (pred_fail & ~actual_fail).sum()
FN = (~pred_fail & actual_fail).sum()
TN = (~pred_fail & ~actual_fail).sum()
recall = TP / (TP + FN)
precision = TP / (TP + FP)
accuracy = (TP + TN) / (TP + FP + FN + TN)
inspection_rate = (TP + FP) / (TP + FP + FN + TN)

print(f"depth：{model_tree_leaf20.get_depth()}")
print(f"leaves：{model_tree_leaf20.get_n_leaves()}")
print(f"TP：{TP}")
print(f"FP：{FP}")
print(f"FN：{FN}")
print(f"TN：{TN}")
print(f"Recall：{recall:.2%}")
print(f"Precision：{precision:.2%}")
print(f"accuracy：{accuracy:.2%}")
print(f"inspection_rate：{inspection_rate:.2%}")

fail_prob = model_tree_leaf20.predict_proba(x_test)[:, 1]

np.quantile(
    fail_prob,
    [0, .1, .25, .5, .75, .9, 1]
)


# save_result("decision_tree", TP, FP, FN, TN)