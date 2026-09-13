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

# 移除特徵無變化的欄位(有116欄)
constant_cols = [
    col for col in df.columns
    if df[col].nunique() <= 1]
len(constant_cols)
df = df.drop(columns=constant_cols)

# 依照rule-based，先只看差異最多的5筆特徵。
top5 = [59, 103, 510, 348, 431]
x = df[top5]
y = labels["label"]

X_train, X_test, y_train, y_test = train_test_split(
    x, y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

# 補值 將nan 改成 訓練模型的中位數。
imputer = SimpleImputer(strategy="median")
#下面指令，因為會有錯誤(系統衝突之類的)，後面加上；，可以避免某些衝突錯誤。
imputer.fit(X_train);
X_train_imputed = imputer.transform(X_train)
X_test_imputed = imputer.transform(X_test)

# 標準化
scaler = StandardScaler()
scaler.fit(X_train_imputed);
X_train_scaled = scaler.transform(X_train_imputed)
X_test_scaled = scaler.transform(X_test_imputed)

#logistic回歸
model = LogisticRegression()
model.fit(X_train_scaled, y_train);
# 看一下訓練出來的係數
print(model.coef_)
print(model.intercept_)

#測試
y_prob = model.predict_proba(X_test_scaled)
print(model.classes_)
fail_prob = y_prob[:, 1]

#目標是recall要9成以上，所以經手動計算門檻值大約小於0.1，用迴圈找最適合的
#用迴圈測試，
result=[]
for threshold in np.arange(0.01, 0.101, 0.001):

    pred_fail = fail_prob >= threshold

    TP = ((pred_fail == True)  & (y_test == 1)).sum()
    FP = ((pred_fail == True)  & (y_test == -1)).sum()
    FN = ((pred_fail == False) & (y_test == 1)).sum()
    TN = ((pred_fail == False) & (y_test == -1)).sum()

    recall = TP / (TP + FN)
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    inspection_rate = (TP + FP) / len(y_test)

    result.append({
        "threshold": threshold,
        "TP": TP,
        "FP": FP,
        "FN": FN,
        "TN": TN,
        "recall": recall,
        "precision": precision,
        "inspection_rate": inspection_rate
    })

logistic_result = pd.DataFrame(result)

# recall 90%以下，誰inspection_rate最低
target_result = logistic_result[
    logistic_result["recall"] >= 0.90
]

#後來以threshold =0.032為值，結束logistic_
threshold = 0.032
pred_fail = fail_prob >= threshold

TP = ((pred_fail == True)  & (y_test == 1)).sum()
FP = ((pred_fail == True)  & (y_test == -1)).sum()
FN = ((pred_fail == False) & (y_test == 1)).sum()
TN = ((pred_fail == False) & (y_test == -1)).sum()




save_result("logistic_top5", TP, FP, FN, TN)