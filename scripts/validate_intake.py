import os
import json
from datetime import datetime

import pandas as pd
import chardet


def validate_file_exists(filepath):
    if not os.path.exists(filepath):
        return False, f"File does not exist: {filepath}"

    if os.path.getsize(filepath) == 0:
        return False, f"File is empty: {filepath}"

    return True, "File exists and has content"


def validate_file_format(filepath, allowed_formats=["csv", "json", "xlsx"]):
    extension = filepath.split(".")[-1].lower()

    if extension not in allowed_formats:
        return False, f"Unsupported format: {extension}"

    return True, f"Format valid: {extension}"


def validate_schema(df, expected_columns):
    missing = set(expected_columns) - set(df.columns)
    extra = set(df.columns) - set(expected_columns)

    issues = []

    if missing:
        issues.append(f"Missing columns: {missing}")

    if extra:
        issues.append(f"Unexpected columns: {extra}")

    if not issues:
        return True, f"Schema valid: {len(df.columns)} columns present"

    return False, " | ".join(issues)


def detect_encoding(filepath):
    with open(filepath, "rb") as file:
        result = chardet.detect(file.read(10000))

    encoding = result.get("encoding", "utf-8")
    confidence = result.get("confidence", 0)

    return encoding, f"Detected: {encoding} (confidence: {confidence:.1%})"


def capture_dataset_stats(filepath, df):
    file_size_mb = os.path.getsize(filepath) / (1024 * 1024)

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "file_size_mb": round(file_size_mb, 4),
        "bytes": os.path.getsize(filepath),
    }


def generate_intake_report(filepath, expected_columns):
    report = {
        "timestamp": datetime.now().isoformat(),
        "filepath": filepath,
        "validations": {},
    }

    file_exists, message = validate_file_exists(filepath)
    report["validations"]["file_exists"] = message

    if not file_exists:
        return report

    format_valid, message = validate_file_format(filepath)
    report["validations"]["format"] = message

    df = pd.read_csv(filepath)

    schema_valid, message = validate_schema(df, expected_columns)
    report["validations"]["schema"] = message

    encoding, message = detect_encoding(filepath)
    report["validations"]["encoding"] = message

    report["statistics"] = capture_dataset_stats(filepath, df)

    with open("output/intake_report.json", "w") as file:
        json.dump(report, file, indent=2)

    return report


if __name__ == "__main__":
    expected_columns = [
        "customer_id",
        "customer_name",
        "transaction_amount",
        "transaction_date",
    ]

    report = generate_intake_report(
        "data/raw/sample.csv",
        expected_columns,
    )

    print("Dataset intake validation completed.")
    print("Report saved to output/intake_report.json")