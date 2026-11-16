
import pandas as pd

from src.extraction import extract_data
from src.cleaning import clean_data
from src.data_quality import calculate_quality
from src.drift_detection import compare_datasets
from src.recommendations import generate_recommendations

# Load datasets
reference = extract_data("data/reference/reference.csv")
drifted = extract_data("data/raw/drifted_current.csv")

# Perform data cleaning
cleaned_reference = clean_data(reference)

# Calculate data quality
quality_report, column_info = calculate_quality(cleaned_reference)

# Detect data drift
drift_report = compare_datasets(reference, drifted)

# Generate recommendations
recommendations = generate_recommendations(
    quality_report,
    drift_report
)

# Convert recommendations into a DataFrame
recommendations_df = pd.DataFrame(recommendations)

# Save recommendations
recommendations_df.to_csv(
    "data/processed/recommendations.csv",
    index=False
)

print("\n========== ETL RECOMMENDATIONS ==========")

print(recommendations_df.to_string(index=False))

print("\nRecommendations saved successfully!")
