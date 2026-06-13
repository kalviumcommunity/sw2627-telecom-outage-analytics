import pandas as pd
import numpy as np
from scipy import stats

# --------------------------------------
# Create Sample Dataset
# --------------------------------------

data = {
    "customer_id": [
        1,2,3,4,5,6,7,8,9,10
    ],
    "revenue": [
        120,
        150,
        180,
        200,
        175,
        210,
        190,
        170,
        5000,
        160
    ],
    "age": [
        24,
        30,
        28,
        35,
        42,
        29,
        31,
        27,
        150,
        26
    ]
}

df = pd.DataFrame(data)

print(df)

# --------------------------------------
# Task 1
# Z Score Detection
# --------------------------------------

df["revenue_zscore"] = np.abs(
    stats.zscore(df["revenue"])
)

z_outliers = df[
    df["revenue_zscore"] > 3
]

print()

print("Z Score Outliers")

print(z_outliers)

print("Count:", len(z_outliers))

# --------------------------------------
# Task 2
# IQR Detection
# --------------------------------------

Q1 = df["revenue"].quantile(0.25)

Q3 = df["revenue"].quantile(0.75)

IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR

upper = Q3 + 1.5 * IQR

df["is_outlier_iqr"] = (
    (df["revenue"] < lower)
    |
    (df["revenue"] > upper)
)

print()

print("IQR Outliers")

print(df[df["is_outlier_iqr"]])

# --------------------------------------
# Task 3
# Cap Outliers
# --------------------------------------

df["revenue_capped"] = df["revenue"].clip(
    lower=lower,
    upper=upper
)

print()

print("Before Capping")

print(
    "Min:",
    df["revenue"].min(),
    "Max:",
    df["revenue"].max()
)

print()

print("After Capping")

print(
    "Min:",
    df["revenue_capped"].min(),
    "Max:",
    df["revenue_capped"].max()
)

# --------------------------------------
# Task 4
# Binary Flag
# --------------------------------------

df["is_outlier"] = (
    df["is_outlier_iqr"]
) | (
    df["revenue_zscore"] > 3
)

normal = df[
    ~df["is_outlier"]
]

anomalies = df[
    df["is_outlier"]
]

print()

print("Normal Records:", len(normal))

print("Anomalies:", len(anomalies))

# --------------------------------------
# Task 5
# Cleaning Log
# --------------------------------------

cleaning_log = [

    {

        "column": "revenue",

        "method": "IQR",

        "action": "cap",

        "threshold_lower": lower,

        "threshold_upper": upper,

        "affected_rows":
        df["is_outlier_iqr"].sum(),

        "date":
        pd.Timestamp.now()

    }

]

log_df = pd.DataFrame(
    cleaning_log
)

log_df.to_csv(
    "output/cleaning_log.csv",
    index=False
)

print()

print("Cleaning Log Saved")

print(log_df)

print()

print(df)