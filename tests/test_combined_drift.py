
from src.extraction import extract_data
from src.drift_detection import compare_datasets

# Step 1: Load reference dataset
reference = extract_data(
    "data/reference/reference.csv"
)

# Step 2: Load normal current dataset
current = extract_data(
    "data/raw/current.csv"
)

# Step 3: Load artificially drifted dataset
drifted = extract_data(
    "data/raw/drifted_current.csv"
)

# Step 4: Compare normal data
print("\n========== NORMAL DATA ==========")

normal_report = compare_datasets(
    reference,
    current
)

# Step 5: Compare drifted data
print("\n========== DRIFTED DATA ==========")

drifted_report = compare_datasets(
    reference,
    drifted
)

# Step 6: Save reports
normal_report.to_csv(
    "data/processed/normal_drift_report.csv",
    index=False
)

drifted_report.to_csv(
    "data/processed/drifted_drift_report.csv",
    index=False
)

print("\nBoth drift reports saved successfully!")
