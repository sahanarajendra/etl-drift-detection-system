
from src.extraction import extract_data
from src.drift_detection import detect_numeric_drift

# Step 1: Load reference dataset
reference = extract_data(
    "data/reference/reference.csv"
)

# Step 2: Load normal current dataset
current = extract_data(
    "data/raw/current.csv"
)

# Step 3: Load drifted dataset
drifted = extract_data(
    "data/raw/drifted_current.csv"
)

# Step 4: Test numerical columns
numeric_columns = reference.select_dtypes(
    include="number"
).columns

print("\n========== NORMAL DATA COMPARISON ==========")

for column in numeric_columns:

    result = detect_numeric_drift(
        reference[column],
        current[column]
    )

    print(f"\nColumn: {column}")
    print(result)


print("\n========== DRIFTED DATA COMPARISON ==========")

for column in numeric_columns:

    result = detect_numeric_drift(
        reference[column],
        drifted[column]
    )

    print(f"\nColumn: {column}")
    print(result)

from src.drift_detection import detect_categorical_drift

# Categorical columns
categorical_columns = reference.select_dtypes(
    include=["object", "string", "category"]
).columns

print("\n========== CATEGORICAL DRIFT COMPARISON ==========")

for column in categorical_columns:

    print(f"\nColumn: {column}")

    # Normal comparison
    normal_result = detect_categorical_drift(
        reference[column],
        current[column]
    )

    print("Normal Dataset:", normal_result)

    # Drifted comparison
    drift_result = detect_categorical_drift(
        reference[column],
        drifted[column]
    )

    print("Drifted Dataset:", drift_result)

from src.drift_detection import calculate_psi

print("\n========== PSI DRIFT COMPARISON ==========")

for column in numeric_columns:

    # Compare reference with normal current data
    normal_psi = calculate_psi(
        reference[column],
        current[column]
    )

    # Compare reference with drifted data
    drifted_psi = calculate_psi(
        reference[column],
        drifted[column]
    )

    print(f"\nColumn: {column}")

    print("Normal PSI:", normal_psi)

    print("Drifted PSI:", drifted_psi)

    if drifted_psi is not None:

        if drifted_psi < 0.10:
            print("Interpretation: Small Change")

        elif drifted_psi < 0.25:
            print("Interpretation: Moderate Change")

        else:
            print("Interpretation: Significant Change")

from src.drift_detection import calculate_wasserstein

print("\n========== WASSERSTEIN DISTANCE ==========")

for column in numeric_columns:

    # Normal comparison
    normal_distance = calculate_wasserstein(
        reference[column],
        current[column]
    )

    # Drifted comparison
    drifted_distance = calculate_wasserstein(
        reference[column],
        drifted[column]
    )

    print(f"\nColumn: {column}")

    print("Normal Distance:", normal_distance)

    print("Drifted Distance:", drifted_distance)
