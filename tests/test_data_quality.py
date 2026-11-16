
from src.extraction import extract_data
from src.cleaning import clean_data
from src.data_quality import calculate_quality

# Step 1: Extract reference dataset
df = extract_data(
    "data/reference/reference.csv"
)

# Step 2: Clean dataset
cleaned_df = clean_data(df)

# Step 3: Calculate data quality
report, column_info = calculate_quality(
    cleaned_df
)

# Step 4: Display final report
print("\nFINAL QUALITY SCORE")

print(
    report["Data Quality Score"],
    "%"
)

# Step 5: Save column information
column_info.to_csv(
    "data/processed/column_quality_report.csv",
    index=False
)

print("\nQuality report saved successfully!")