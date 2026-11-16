
import pandas as pd


def calculate_quality(df):

    print("\nStarting Data Quality Analysis...")

    # Total rows and columns
    total_rows = len(df)
    total_columns = len(df.columns)

    # Calculate missing values
    missing_values = df.isnull().sum().sum()

    total_cells = df.size

    missing_percentage = (
        (missing_values / total_cells) * 100
        if total_cells > 0 else 0
    )

    # Calculate duplicate records
    duplicate_rows = df.duplicated().sum()

    duplicate_percentage = (
        (duplicate_rows / total_rows) * 100
        if total_rows > 0 else 0
    )

    # Calculate data quality score
    quality_score = 100 - (
        missing_percentage + duplicate_percentage
    )

    quality_score = max(0, round(quality_score, 2))

    # Column information
    column_info = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values,
        "Missing Values": df.isnull().sum().values,
        "Unique Values": df.nunique().values
    })

    # Generate quality report
    report = {
        "Total Rows": total_rows,
        "Total Columns": total_columns,
        "Missing Values": int(missing_values),
        "Missing Percentage": round(
            missing_percentage, 2
        ),
        "Duplicate Rows": int(duplicate_rows),
        "Duplicate Percentage": round(
            duplicate_percentage, 2
        ),
        "Data Quality Score": quality_score
    }

    print("\nDATA QUALITY REPORT")

    for key, value in report.items():
        print(f"{key}: {value}")

    print("\nCOLUMN INFORMATION")
    print(column_info.to_string(index=False))

    print("\nData Quality Analysis Completed!")

    return report, column_info
