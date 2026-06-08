import pandas as pd


def ingest_data(filepath):
    """
    Load telecom outage data from a CSV file.

    Input:
        filepath (str): Path to raw CSV file

    Returns:
        pandas.DataFrame containing outage records
    """
    df = pd.read_csv(filepath)
    return df


def process_data(df):
    """
    Clean and transform telecom outage data.

    Input:
        pandas.DataFrame containing outage data

    Returns:
        pandas.DataFrame with duplicates removed
        and impact score calculated
    """

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Create impact score
    df["impact_score"] = (
        df["outage_alerts"] * 2
        + df["customer_complaints"] * 3
        + (df["usage_metric"] / 100)
    )

    return df


def output_results(df, output_path):
    """
    Save processed results to disk.
    """

    df.to_csv(output_path, index=False)

    print("Data successfully processed")
    print(f"Rows processed: {len(df)}")
    print(f"Output saved to {output_path}")


if __name__ == "__main__":
    data = ingest_data("data/raw/sample.csv")

    processed = process_data(data)

    output_results(processed, "output/processed.csv")