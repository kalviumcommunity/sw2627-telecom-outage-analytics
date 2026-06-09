import pandas as pd
import numpy as np
import json
import os


def profile_nulls_and_duplicates(df):
    """
    Compute null percentage and duplicate counts per column.
    """
    profile = {
        "null_counts": {},
        "null_percentages": {},
        "exact_duplicate_count": 0,
    }

    for col in df.columns:
        null_count = df[col].isna().sum()
        null_pct = (null_count / len(df)) * 100

        profile["null_counts"][col] = int(null_count)
        profile["null_percentages"][col] = round(null_pct, 2)

    duplicate_count = df.duplicated().sum()

    profile["exact_duplicate_count"] = int(duplicate_count)
    profile["duplicate_percentage"] = round(
        (duplicate_count / len(df)) * 100, 2
    )

    return profile


def profile_numerical_columns(df):
    """
    Summarise numerical columns with statistical measures.
    """
    numerical_cols = df.select_dtypes(include=[np.number]).columns

    stats = {}

    for col in numerical_cols:
        stats[col] = {
            "min": round(df[col].min(), 2)
            if not pd.isna(df[col].min())
            else None,
            "max": round(df[col].max(), 2)
            if not pd.isna(df[col].max())
            else None,
            "mean": round(df[col].mean(), 2)
            if not pd.isna(df[col].mean())
            else None,
            "median": round(df[col].median(), 2)
            if not pd.isna(df[col].median())
            else None,
            "std": round(df[col].std(), 2)
            if not pd.isna(df[col].std())
            else None,
            "null_count": int(df[col].isnull().sum()),
        }

    return pd.DataFrame(stats).T


def profile_categorical_columns(df, top_n=5):
    """
    Summarise categorical columns with value distributions.
    """
    categorical_cols = df.select_dtypes(include=["object"]).columns

    profile = {}

    for col in categorical_cols:
        profile[col] = {
            "unique_count": int(df[col].nunique()),
            "top_values": df[col].value_counts().head(top_n).to_dict(),
            "null_count": int(df[col].isnull().sum()),
        }

    return profile


def identify_quality_issues(
    df,
    null_threshold=30,
    duplicate_threshold=5,
):
    """
    Identify data quality problems based on thresholds.
    """
    issues = []

    # Null checks
    null_pcts = (df.isnull().sum() / len(df)) * 100

    for col, pct in null_pcts.items():
        if pct > null_threshold:
            issues.append(
                {
                    "type": "High nulls",
                    "column": col,
                    "severity": "HIGH",
                    "value": f"{pct:.1f}% missing",
                    "recommendation":
                        "Consider imputation or column exclusion",
                }
            )

    # Duplicate checks
    dup_count = df.duplicated().sum()
    dup_pct = (dup_count / len(df)) * 100

    if dup_pct > duplicate_threshold:
        issues.append(
            {
                "type": "High duplicates",
                "column": "Full row",
                "severity": "HIGH",
                "value": f"{dup_pct:.1f}% duplicated",
                "recommendation":
                    "Deduplication required before analysis",
            }
        )

    # Invalid range checks
    for col in df.select_dtypes(include=[np.number]).columns:
        if "amount" in col.lower():
            if (df[col] < 0).any():
                issues.append(
                    {
                        "type": "Invalid range",
                        "column": col,
                        "severity": "MEDIUM",
                        "value": "Contains negative values",
                        "recommendation":
                            "Investigate negative entries",
                    }
                )

    return issues


def generate_profile_report(df, filepath):
    """
    Generate complete data quality report and save to JSON.
    """

    report = {
        "dataset": filepath,
        "record_count": len(df),
        "column_count": len(df.columns),
        "nulls_and_duplicates":
            profile_nulls_and_duplicates(df),
        "numerical_stats":
            profile_numerical_columns(df).to_dict(),
        "categorical_stats":
            profile_categorical_columns(df),
        "quality_issues":
            identify_quality_issues(df),
    }

    os.makedirs("output", exist_ok=True)

    with open(
        "output/profile_report.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(report, f, indent=2, default=str)

    print("\n" + "=" * 60)
    print(f"DATA QUALITY PROFILE: {filepath}")
    print("=" * 60)
    print(f"Records: {report['record_count']}")
    print(f"Columns: {report['column_count']}")
    print(
        f"\nQuality Issues Found: "
        f"{len(report['quality_issues'])}"
    )

    for issue in report["quality_issues"]:
        print(
            f"  [{issue['severity']}] "
            f"{issue['type']} in {issue['column']}"
        )
        print(
            f"    Value: {issue['value']} "
            f"→ {issue['recommendation']}"
        )

    print("=" * 60 + "\n")

    return report


def main():
    filepath = "data/raw/quality_test.csv"

    try:
        df = pd.read_csv(filepath)

        print("Dataset Loaded Successfully")
        print(f"Shape: {df.shape}")

        generate_profile_report(df, filepath)

        print(
            "Profile report saved to "
            "output/profile_report.json"
        )

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()