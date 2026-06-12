import pandas as pd


# -------------------------------------------------
# Create Sample Dataset
# -------------------------------------------------

data = {
    "product_name": [
        " Electronics ",
        "electronics",
        "ELECTRONICS",
        "  Product_C  ",
        "Home Appliances"
    ],
    "customer_segment": [
        "B2B",
        "b2b",
        "B 2 B",
        "business-to-business",
        "SME"
    ],
    "location": [
        "São Paulo",
        "Montréal",
        " New York ",
        "München",
        "Bengaluru"
    ],
    "customer_name": [
        " JOHN ",
        "john",
        "John",
        "Alice",
        None
    ]
}

df = pd.DataFrame(data)

print("=" * 50)
print("ORIGINAL DATASET")
print("=" * 50)
print(df)


# -------------------------------------------------
# Task 1
# Strip Whitespace
# -------------------------------------------------

def strip_all_strings(df):
    """Strip whitespace from all object columns."""

    string_cols = df.select_dtypes(include=["object"]).columns

    total_changes = 0

    for col in string_cols:

        print(f"\nColumn: {col}")

        print("\nBefore:")
        print(df[col].value_counts(dropna=False))

        before_unique = df[col].nunique(dropna=True)

        # count values containing whitespace
        whitespace_count = (
            df[col]
            .fillna("")
            .str.startswith(" ")
            | df[col].fillna("").str.endswith(" ")
        ).sum()

        total_changes += whitespace_count

        df[col] = df[col].str.strip()

        after_unique = df[col].nunique(dropna=True)

        print("\nAfter:")
        print(df[col].value_counts(dropna=False))

        print(
            f"Unique values: {before_unique} -> {after_unique}"
        )

        print(
            f"Whitespace issues fixed: {whitespace_count}"
        )

    print("\nTotal whitespace issues fixed:", total_changes)

    return df


df = strip_all_strings(df)


# -------------------------------------------------
# Task 2
# Normalize Casing
# -------------------------------------------------

print("\n" + "=" * 50)
print("BEFORE LOWERCASE")
print("=" * 50)
print(df.head())


def normalize_casing(df, columns):

    for col in columns:
        df[col] = df[col].str.lower()
        print(f"{col} converted to lowercase")

    return df


columns_to_lower = [
    "product_name",
    "customer_segment",
    "customer_name"
]

df = normalize_casing(df, columns_to_lower)

print("\n" + "=" * 50)
print("AFTER LOWERCASE")
print("=" * 50)
print(df.head())


# -------------------------------------------------
# Task 3
# Remove Special Characters
# -------------------------------------------------

print("\n" + "=" * 50)
print("BEFORE SPECIAL CHARACTER REMOVAL")
print("=" * 50)
print(df[["location"]])


def remove_special_characters(df, columns):

    for col in columns:
        df[col] = df[col].str.replace(
            "[^a-zA-Z0-9 ]",
            "",
            regex=True
        )

        print(f"Removed special characters from {col}")

    return df


df = remove_special_characters(
    df,
    ["location", "product_name"]
)

print("\n" + "=" * 50)
print("AFTER SPECIAL CHARACTER REMOVAL")
print("=" * 50)
print(df[["location"]])


# -------------------------------------------------
# Task 4
# Mapping Dictionary
# -------------------------------------------------

print("\n" + "=" * 50)
print("BEFORE MAPPING")
print("=" * 50)
print(df["customer_segment"].value_counts())


segment_map = {

    "b2b": "B2B",
    "b 2 b": "B2B",
    "business-to-business": "B2B",

    "sme": "SMB",
    "small medium enterprise": "SMB",
    "small-medium-enterprise": "SMB",

    "enterprise": "Enterprise",
    "corp": "Enterprise",
    "corporate": "Enterprise"
}

df["customer_segment"] = (
    df["customer_segment"]
    .replace(segment_map)
)

print("\n" + "=" * 50)
print("AFTER MAPPING")
print("=" * 50)
print(df["customer_segment"].value_counts())


# -------------------------------------------------
# Task 5
# Reusable Cleaning Function
# -------------------------------------------------

def clean_text_column(
    series,
    lowercase=True,
    strip=True,
    remove_special=False,
    mapping=None
):
    """
    Reusable text cleaning function.
    """

    result = series.copy()

    if result.isna().any():
        print(
            f"Warning: {result.isna().sum()} null values found."
        )

    if strip:
        result = result.str.strip()

    if lowercase:
        result = result.str.lower()

    if remove_special:
        result = result.str.replace(
            "[^a-zA-Z0-9 ]",
            "",
            regex=True
        )

    if mapping is not None:
        result = result.replace(mapping)

    return result


# Apply reusable function

df["customer_name"] = clean_text_column(
    df["customer_name"],
    lowercase=True,
    strip=True
)

df["product_name"] = clean_text_column(
    df["product_name"],
    lowercase=True,
    strip=True,
    remove_special=True
)

df["customer_segment"] = clean_text_column(
    df["customer_segment"],
    lowercase=False,
    strip=True,
    mapping=segment_map
)


# -------------------------------------------------
# Edge Case Testing
# -------------------------------------------------

print("\n" + "=" * 50)
print("EDGE CASE TESTING")
print("=" * 50)

test_cases = [
    "  Product A  ",
    "PRODUCT B",
    "Product_C",
    None,
    ""
]

test_series = pd.Series(test_cases)

result = clean_text_column(
    test_series,
    lowercase=True,
    strip=True,
    remove_special=True
)

print(result)


# -------------------------------------------------
# Final Cleaned Data
# -------------------------------------------------

print("\n" + "=" * 50)
print("FINAL CLEANED DATASET")
print("=" * 50)
print(df)