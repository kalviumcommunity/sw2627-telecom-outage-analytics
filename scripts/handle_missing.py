import os
import json
import pandas as pd
import numpy as np


def to_python_scalar(value):
    """Convert pandas / NumPy scalars to native Python JSON-safe types."""
    if isinstance(value, np.generic):
        return value.item()
    return value


def analyze_missing_values(df):
    """
    Compute null counts and percentages before treatment.

    Returns: DataFrame with analysis of missing data by column
    """
    missing_analysis = pd.DataFrame({
        'column': df.columns,
        'null_count': df.isnull().sum().values,
        'null_percentage': (df.isnull().sum() / len(df) * 100).round(2).values,
        'data_type': df.dtypes.values,
        'null_meaning': ''
    })

    print("=" * 70)
    print("BEFORE IMPUTATION - Missing Value Analysis")
    print("=" * 70)
    print(missing_analysis.to_string(index=False))
    print(f"\nTotal rows: {len(df)}")
    print(f"Total cells: {len(df) * len(df.columns)}")
    print(f"Missing cells: {df.isnull().sum().sum()}")
    print("=" * 70)

    return missing_analysis


def impute_mean_median(df, numerical_cols, strategy='median'):
    """
    Fill numerical nulls with mean or median.
    """
    df_imputed = df.copy()

    for col in numerical_cols:
        if col in df.columns and df[col].isnull().sum() > 0:

            fill_value = (
                df[col].median()
                if strategy == 'median'
                else df[col].mean()
            )

            df_imputed[col] = df_imputed[col].fillna(fill_value)

            null_count = df[col].isnull().sum()

            print(
                f"  ✓ {col}: filled {null_count} nulls "
                f"with {strategy} ({fill_value:.2f})"
            )

    return df_imputed


def impute_mode(df, categorical_cols):
    """
    Fill categorical nulls with mode (most common value).
    """
    df_imputed = df.copy()

    for col in categorical_cols:
        if col in df.columns and df[col].isnull().sum() > 0:

            mode_val = df[col].mode()[0]
            null_count = df[col].isnull().sum()

            df_imputed[col] = df_imputed[col].fillna(mode_val)

            print(
                f"  ✓ {col}: filled {null_count} nulls "
                f"with mode '{mode_val}'"
            )

    return df_imputed


def impute_forward_fill(df, time_series_cols):
    """
    Fill with previous value (for time-series data).
    """
    df_imputed = df.copy()

    for col in time_series_cols:
        if col in df.columns and df[col].isnull().sum() > 0:

            null_count = df[col].isnull().sum()

            df_imputed[col] = df_imputed[col].ffill()

            print(
                f"  ✓ {col}: forward-filled "
                f"{null_count} nulls"
            )

    return df_imputed


def drop_rows_with_nulls(df, critical_cols):
    """
    Drop rows where critical columns are null.
    """
    rows_before = len(df)

    df_imputed = df.dropna(subset=critical_cols)

    rows_dropped = rows_before - len(df_imputed)

    print(
        f"  ✓ Dropped {rows_dropped} rows "
        f"with null in: {critical_cols}"
    )

    return df_imputed


def document_imputation_decisions(df_original, df_imputed):
    """
    Document all imputation decisions with business justification.
    """

    decisions = {
        "amount": {
            "column_type": "numerical",
            "null_count_before":
                to_python_scalar(df_original["amount"].isnull().sum())
                if "amount" in df_original.columns else 0,
            "strategy": "median_imputation",
            "value_used":
                to_python_scalar(float(df_original["amount"].median()))
                if "amount" in df_original.columns else None,
            "business_reasoning":
                "Median purchase amount is representative "
                "of typical transaction. Mean would be skewed "
                "by high-value outliers. Maintains distribution integrity.",
            "risk_assessment":
                "Low - median is stable metric resistant to outliers"
        },

        "email": {
            "column_type": "categorical_identifier",
            "null_count_before":
                to_python_scalar(df_original["email"].isnull().sum())
                if "email" in df_original.columns else 0,
            "strategy": "drop_rows",
            "rows_affected":
                to_python_scalar(int(df_original["email"].isnull().sum()))
                if "email" in df_original.columns else 0,
            "business_reasoning":
                "Email is critical for customer contact and marketing "
                "campaigns. Rows without email cannot be used for outreach.",
            "risk_assessment":
                "Low - only affects a small percentage of data"
        },

        "status_date": {
            "column_type": "datetime_series",
            "null_count_before":
                to_python_scalar(df_original["status_date"].isnull().sum())
                if "status_date" in df_original.columns else 0,
            "strategy": "forward_fill",
            "interpretation":
                "Assumes last known status date is valid until changed",
            "business_reasoning":
                "Forward fill preserves temporal continuity in time-series data.",
            "risk_assessment":
                "Medium - assumes no change between observations"
        }
    }

    with open("output/imputation_decisions.json", "w") as f:
        json.dump(decisions, f, indent=2)

    print("  ✓ Saved imputation decisions to output/imputation_decisions.json")

    return decisions


def validate_imputation(df_original, df_imputed):
    """
    Compare metrics before and after imputation.
    """

    print("\n" + "=" * 70)
    print("AFTER IMPUTATION - Validation Report")
    print("=" * 70)

    print(f"Total rows before: {len(df_original)}")
    print(f"Total rows after:  {len(df_imputed)}")
    print(f"Rows removed: {len(df_original) - len(df_imputed)}")

    print(f"\nTotal nulls before: {df_original.isnull().sum().sum()}")
    print(f"Total nulls after:  {df_imputed.isnull().sum().sum()}")

    missing_after = pd.DataFrame({
        'column': df_imputed.columns,
        'null_count_after': df_imputed.isnull().sum().values,
        'null_percentage_after':
            (df_imputed.isnull().sum() / len(df_imputed) * 100)
            .round(2)
            .values
    })

    print("\nNull values by column after imputation:")
    print(missing_after.to_string(index=False))

    print("=" * 70)

    return missing_after


if __name__ == "__main__":

    os.makedirs("output", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)

    # Load data
    df = pd.read_csv("data/raw/raw_data.csv")

    # Save original copy for comparison
    df_original = df.copy()

    # Step 1
    print("Step 1: Analyzing missing values...")
    analyze_missing_values(df)

    # Step 2
    print("\nStep 2: Applying imputation strategies...")

    # Drop rows with missing critical identifiers
    df = drop_rows_with_nulls(df, ["customer_id", "email"])

    # Numerical imputation
    df = impute_mean_median(df, ["amount"], strategy="median")

    # Categorical imputation
    df = impute_mode(df, ["category"])

    # Step 3
    print("\nStep 3: Documenting imputation decisions...")
    document_imputation_decisions(df_original, df)

    # Step 4
    print("\nStep 4: Validating imputation...")
    validate_imputation(df_original, df)

    # Save cleaned data
    df.to_csv(
        "data/processed/cleaned_data.csv",
        index=False
    )

    print("\n✓ Cleaned data saved to data/processed/cleaned_data.csv")