
from src.extraction import extract_data
from src.cleaning import clean_data
from src.transformation import transform_data

# Step 1: Extract reference dataset
reference = extract_data(
    "data/reference/reference.csv"
)

# Step 2: Extract current dataset
current = extract_data(
    "data/raw/current.csv"
)

# Step 3: Clean both datasets
reference_cleaned = clean_data(reference)
current_cleaned = clean_data(current)

# Step 4: Transform both datasets
reference_transformed, current_transformed, preprocessor = (
    transform_data(
        reference_cleaned,
        current_cleaned
    )
)

# Step 5: Display transformed data
print("\nReference transformed data:")
print(reference_transformed.head())

print("\nCurrent transformed data:")
print(current_transformed.head())

# Step 6: Save transformed datasets
reference_transformed.to_csv(
    "data/processed/transformed_reference.csv",
    index=False
)

current_transformed.to_csv(
    "data/processed/transformed_current.csv",
    index=False
)

print("\nBoth transformed datasets saved successfully!")
