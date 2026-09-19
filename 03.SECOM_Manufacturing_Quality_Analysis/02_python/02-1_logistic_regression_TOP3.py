# %%
import pandas as pd
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from model_results import save_result
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
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

# 依照01-2_Rule-Based_Train_Test，先只看差異最多的3筆特徵59、103、510。
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
#下面指令，因為會有錯誤(系統衝突之類的)，後面加上；，可以避免某些衝突錯誤。
imputer.fit(x_train);
x_train_imputed = imputer.transform(x_train)
x_test_imputed = imputer.transform(x_test)

# 標準化
scaler = StandardScaler()
scaler.fit(x_train_imputed);
x_train_scaled = scaler.transform(x_train_imputed)
x_test_scaled = scaler.transform(x_test_imputed)

#logistic回歸
model = LogisticRegression()
model.fit(x_train_scaled, y_train);
# 看一下訓練出來的係數
# print(model.coef_)
# print(model.intercept_)

#看訓練模型狀況
y_prob = model.predict_proba(x_train_scaled)
fail_prob = y_prob[:, 1]
#用迴圈測試，
result=[]
for threshold in np.arange(0.01, 0.101, 0.001):

    pred_fail = fail_prob >= threshold

    TP = ((pred_fail == True)  & (y_train == 1)).sum()
    FP = ((pred_fail == True)  & (y_train == -1)).sum()
    FN = ((pred_fail == False) & (y_train == 1)).sum()
    TN = ((pred_fail == False) & (y_train == -1)).sum()

    recall = TP / (TP + FN)
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    accuracy = (TP + TN) / (TP + FP + FN + TN)
    inspection_rate = (TP + FP) / (TP + FP + FN + TN)


    result.append({
        "threshold": threshold,
        "TP": TP,
        "FP": FP,
        "FN": FN,
        "TN": TN,
        "recall": recall,
        "precision": precision,
        "accuracy":accuracy,
        "inspection_rate": inspection_rate
    })

logistic_result = pd.DataFrame(result)

# recall 90%以下，誰inspection_rate最低
target_result = logistic_result[
    logistic_result["recall"] >= 0.90
]

#後來以threshold =0.032為值，結束logistic_
threshold = target_result["threshold"].max()
y_test_prob = model.predict_proba(x_test_scaled)
fail_prob_test = y_test_prob[:, 1]
pred_fail_test = fail_prob_test >= threshold

TP = ((pred_fail_test == True)  & (y_test == 1)).sum()
FP = ((pred_fail_test == True)  & (y_test == -1)).sum()
FN = ((pred_fail_test == False) & (y_test == 1)).sum()
TN = ((pred_fail_test == False) & (y_test == -1)).sum()

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


save_result("logistic_top3", TP, FP, FN, TN)