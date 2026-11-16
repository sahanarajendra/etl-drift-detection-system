
import pandas as pd
from scipy.stats import ks_2samp


def detect_numeric_drift(reference, current):

    # Remove missing values
    reference = reference.dropna()
    current = current.dropna()

    # Check whether sufficient data is available
    if len(reference) == 0 or len(current) == 0:

        return {
            "KS Statistic": None,
            "P Value": None,
            "Drift Status": "Insufficient Data"
        }

    # Perform KS test
    ks_statistic, p_value = ks_2samp(
        reference,
        current
    )

    # Determine drift status
    if p_value < 0.05:
        drift_status = "Drift Detected"
    else:
        drift_status = "No Drift Detected"

    # Store results
    result = {
        "KS Statistic": round(float(ks_statistic), 4),
        "P Value": round(float(p_value), 6),
        "Drift Status": drift_status
    }

    return result

import numpy as np
from scipy.stats import chi2_contingency


def detect_categorical_drift(reference, current):

    # Handle missing values
    reference = reference.fillna(
        "Missing"
    ).astype(str)

    current = current.fillna(
        "Missing"
    ).astype(str)

    # Get all unique categories
    categories = sorted(
        set(reference.unique()) |
        set(current.unique())
    )

    # Count category frequencies
    reference_counts = (
        reference.value_counts()
        .reindex(categories, fill_value=0)
    )

    current_counts = (
        current.value_counts()
        .reindex(categories, fill_value=0)
    )

    # Create contingency table
    contingency_table = np.array([
        reference_counts.values,
        current_counts.values
    ])

    # Check sufficient categories
    if len(categories) < 2:
        return {
            "Chi-Square Statistic": None,
            "P Value": None,
            "Drift Status": "Insufficient Categories"
        }

    # Perform Chi-Square test
    chi_stat, p_value, dof, expected = (
        chi2_contingency(contingency_table)
    )

    # Determine drift
    if p_value < 0.05:
        status = "Drift Detected"
    else:
        status = "No Drift Detected"

    return {
        "Chi-Square Statistic": round(
            float(chi_stat), 4
        ),
        "P Value": round(float(p_value), 6),
        "Drift Status": status
    }

import numpy as np


def calculate_psi(reference, current, bins=10):

    # Convert values to numeric arrays
    reference = np.asarray(
        reference.dropna(), dtype=float
    )

    current = np.asarray(
        current.dropna(), dtype=float
    )

    # Check available data
    if len(reference) == 0 or len(current) == 0:
        return None

    # Create bin boundaries using reference data
    breakpoints = np.unique(
        np.quantile(
            reference,
            np.linspace(0, 1, bins + 1)
        )
    )

    # Check whether enough unique boundaries exist
    if len(breakpoints) < 3:
        return None

    # Include all possible values
    breakpoints[0] = -np.inf
    breakpoints[-1] = np.inf

    # Calculate frequencies
    ref_counts, _ = np.histogram(
        reference,
        bins=breakpoints
    )

    cur_counts, _ = np.histogram(
        current,
        bins=breakpoints
    )

    # Convert frequencies to percentages
    epsilon = 0.000001

    ref_pct = (
        ref_counts + epsilon
    ) / (len(reference) + epsilon * len(ref_counts))

    cur_pct = (
        cur_counts + epsilon
    ) / (len(current) + epsilon * len(cur_counts))

    # Calculate PSI
    psi = np.sum(
        (cur_pct - ref_pct) *
        np.log(cur_pct / ref_pct)
    )

    return round(float(psi), 4)

from scipy.stats import wasserstein_distance


def calculate_wasserstein(reference, current):

    # Remove missing values
    reference = reference.dropna()
    current = current.dropna()

    # Check data availability
    if len(reference) == 0 or len(current) == 0:
        return None

    # Calculate Wasserstein distance
    distance = wasserstein_distance(
        reference,
        current
    )

    return round(float(distance), 4)

def compare_datasets(reference, current):

    import pandas as pd
    from pandas.api.types import is_numeric_dtype

    print("\nStarting Complete Drift Detection...")

    # Check dataset columns
    if set(reference.columns) != set(current.columns):
        raise ValueError(
            "Reference and current datasets have different columns."
        )

    results = []

    # Process every column
    for column in reference.columns:

        ref_col = reference[column]
        cur_col = current[column]

        # Numerical column detection
        if is_numeric_dtype(ref_col):

            # KS Test
            ks_result = detect_numeric_drift(
                ref_col,
                cur_col
            )

            # PSI
            psi_value = calculate_psi(
                ref_col,
                cur_col
            )

            # Wasserstein Distance
            wasserstein_value = calculate_wasserstein(
                ref_col,
                cur_col
            )

            # Overall numerical drift decision
            drift_detected = (
                ks_result["Drift Status"] == "Drift Detected"
                or (
                    psi_value is not None
                    and psi_value > 0.25
                )
            )

            results.append({
                "Column": column,
                "Data Type": "Numerical",
                "KS Statistic": ks_result["KS Statistic"],
                "P Value": ks_result["P Value"],
                "PSI": psi_value,
                "Wasserstein Distance": wasserstein_value,
                "Drift Status": (
                    "Drift Detected"
                    if drift_detected
                    else "No Drift Detected"
                )
            })

        else:

            # Chi-Square Test
            chi_result = detect_categorical_drift(
                ref_col,
                cur_col
            )

            results.append({
                "Column": column,
                "Data Type": "Categorical",
                "KS Statistic": None,
                "P Value": chi_result["P Value"],
                "PSI": None,
                "Wasserstein Distance": None,
                "Drift Status": chi_result["Drift Status"]
            })

    # Convert results into DataFrame
    report = pd.DataFrame(results)

    print("\nDRIFT DETECTION REPORT")
    print(report.to_string(index=False))

    # Calculate summary
    total_columns = len(report)

    drifted_columns = (
        report["Drift Status"] == "Drift Detected"
    ).sum()

    print("\nDRIFT SUMMARY")
    print("Total Columns:", total_columns)
    print("Drifted Columns:", drifted_columns)
    print(
        "Stable Columns:",
        total_columns - drifted_columns
    )

    print("\nComplete Drift Detection Finished!")

    return report
