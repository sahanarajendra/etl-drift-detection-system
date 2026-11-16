
from src.extraction import extract_data

# Extract reference dataset
reference = extract_data(
    "data/reference/reference.csv"
)

print("\nFirst 5 records:")
print(reference.head())

# Extract current dataset
current = extract_data(
    "data/raw/current.csv"
)

print("\nCurrent dataset shape:")
print(current.shape)
