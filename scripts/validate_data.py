import pandas as pd
import json

df = pd.read_csv("data/customer_data.csv")

df["valid_age"] = (df["age"] >= 0) & (df["age"] <= 120)

df["valid_customer_id"] = df["customer_id"].notna()

df["valid_email"] = df["email"].notna()

df["valid_email_format"] = df["email"].str.contains("@", na=False)

df["valid_phone"] = (
    df["phone"]
    .astype(str)
    .str.match(r'^\d{10}$', na=False)
)

df["start_date"] = pd.to_datetime(df["start_date"])
df["end_date"] = pd.to_datetime(df["end_date"])

df["valid_date_order"] = (
    df["end_date"] >= df["start_date"]
)

validation_cols = [
    "valid_age",
    "valid_customer_id",
    "valid_email",
    "valid_email_format",
    "valid_phone",
    "valid_date_order"
]

df["passes_all_checks"] = (
    df[validation_cols].all(axis=1)
)

failures = df[
    ~df["passes_all_checks"]
]

clean_data = df[
    df["passes_all_checks"]
]

failures.to_csv(
    "output/validation_failures.csv",
    index=False
)

clean_data.to_csv(
    "output/clean_data.csv",
    index=False
)

report = {
    "total_records": len(df),
    "passed_records":
        int(df["passes_all_checks"].sum()),
    "failed_records":
        int((~df["passes_all_checks"]).sum())
}

for col in validation_cols:
    report[col] = {
        "passed": int(df[col].sum()),
        "failed": int((~df[col]).sum())
    }

with open(
    "output/validation_report.json",
    "w"
) as f:
    json.dump(report, f, indent=4)

print("\nVALIDATION REPORT")
print("-" * 30)
print(f"Total Records : {len(df)}")
print(f"Passed        : {report['passed_records']}")
print(f"Failed        : {report['failed_records']}")