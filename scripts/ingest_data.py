import pandas as pd


def ingest_csv(filepath, delimiter=",", encoding="utf-8", dtype_dict=None):
    try:
        df = pd.read_csv(
            filepath,
            delimiter=delimiter,
            encoding=encoding,
            dtype=dtype_dict
        )

        print(f"CSV loaded: {filepath}")
        print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")
        print(f"Columns: {list(df.columns)}")

        return df

    except FileNotFoundError:
        print(f"Error: File not found - {filepath}")
        raise

    except UnicodeDecodeError:
        print(f"Encoding error while reading {filepath}")
        raise


def ingest_json(filepath, is_nested=False):
    try:
        df = pd.read_json(filepath)

        if is_nested:
            df = pd.json_normalize(df.to_dict("records"))
            print("Nested JSON flattened")

        print(f"JSON loaded: {filepath}")
        print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")

        return df

    except FileNotFoundError:
        print(f"Error: File not found - {filepath}")
        raise


def ingest_csv_with_fallback(
    filepath,
    delimiters=None,
    fallback_encodings=None
):
    if delimiters is None:
        delimiters = [","]

    if fallback_encodings is None:
        fallback_encodings = [
            "utf-8",
            "latin-1",
            "iso-8859-1",
            "cp1252"
        ]

    for delimiter in delimiters:
        for encoding in fallback_encodings:
            try:
                df = pd.read_csv(
                    filepath,
                    delimiter=delimiter,
                    encoding=encoding
                )

                print(
                    f"Loaded with delimiter='{delimiter}' "
                    f"and encoding='{encoding}'"
                )

                return df

            except (
                UnicodeDecodeError,
                pd.errors.ParserError
            ):
                continue

    raise ValueError(f"Could not load {filepath}")


def document_ingestion(df, source_file):
    print("\n" + "=" * 60)
    print(f"INGESTION REPORT: {source_file}")
    print("=" * 60)

    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print("\nColumn Names & Data Types:")
    print(df.dtypes)

    print("\nNull Values Per Column:")
    print(df.isnull().sum())

    print("\nFirst 3 Rows:")
    print(df.head(3).to_string())

    print("=" * 60)

    return df


if __name__ == "__main__":

    print("Starting multi-format ingestion...\n")

    csv_df = ingest_csv(
        "data/raw/customers.csv",
        delimiter=",",
        encoding="utf-8"
    )

    document_ingestion(
        csv_df,
        "customers.csv"
    )

    json_df = ingest_json(
        "data/raw/transactions.json",
        is_nested=False
    )

    document_ingestion(
        json_df,
        "transactions.json"
    )

    csv_df.to_csv(
        "data/processed/customers_ingested.csv",
        index=False
    )

    json_df.to_csv(
        "data/processed/transactions_ingested.csv",
        index=False
    )

    print("\nAll data ingested and saved to processed/")