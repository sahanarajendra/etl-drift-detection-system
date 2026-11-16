
import pandas as pd


def clean_data(df):

    # Create a copy of the original dataset
    df = df.copy()

    print("\nStarting Data Cleaning...")

    # 1. Remove completely empty columns
    df = df.dropna(axis=1, how="all")

    # 2. Remove duplicate records
    duplicates = df.duplicated().sum()

    df = df.drop_duplicates()

    print("Duplicates removed:", duplicates)

    # 3. Remove unwanted spaces from text columns
    text_columns = df.select_dtypes(
        include=["object", "string"]
    ).columns

    for col in text_columns:
        df[col] = df[col].str.strip()

    # 4. Handle missing numerical values
    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    for col in numeric_columns:

        median_value = df[col].median()

        df[col] = df[col].fillna(median_value)

    # 5. Handle missing categorical values
    categorical_columns = df.select_dtypes(
        include=["object", "string"]
    ).columns

    for col in categorical_columns:

        mode_value = df[col].mode()

        if not mode_value.empty:
            df[col] = df[col].fillna(mode_value[0])
        else:
            df[col] = df[col].fillna("Unknown")

    # 6. Display final information
    print("Remaining missing values:", df.isnull().sum().sum())

    print("Final dataset shape:", df.shape)

    print("Data Cleaning Completed!")

    return df
