
from src.extraction import extract_data
from src.drift_detection import compare_datasets
from src.visualization import plot_drift_report

# Load datasets
reference = extract_data("data/reference/reference.csv")
drifted = extract_data("data/raw/drifted_current.csv")

# Detect drift
drift_report = compare_datasets(reference, drifted)

# Generate visualization
plot_drift_report(drift_report)
