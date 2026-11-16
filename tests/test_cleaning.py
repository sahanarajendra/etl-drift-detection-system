
from src.extraction import extract_data
from src.cleaning import clean_data

# Extract reference dataset
df = extract_data(
    "data/reference/reference.csv"
)

print("\nBefore Cleaning:")
print("Shape:", df.shape)
print("Missing Values:", df.isnull().sum().sum())
print("Duplicate Rows:", df.duplicated().sum())

# Perform cleaning
cleaned_df = clean_data(df)

print("\nAfter Cleaning:")
print("Shape:", cleaned_df.shape)
print("Missing Values:", cleaned_df.isnull().sum().sum())
print("Duplicate Rows:", cleaned_df.duplicated().sum())

# Save cleaned dataset
cleaned_df.to_csv(
    "data/processed/cleaned_reference.csv",
    index=False
)

print("\nCleaned dataset saved successfully!")
