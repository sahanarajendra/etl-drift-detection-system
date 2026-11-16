import matplotlib.pyplot as plt
import seaborn as sns


def plot_drift_report(drift_report):
    print("\nGenerating Drift Visualization...")

    # Count drifted and stable columns
    drift_counts = drift_report["Drift Status"].value_counts()

    plt.figure(figsize=(8, 5))

    sns.barplot(
        x=drift_counts.index,
        y=drift_counts.values
    )

    plt.title("Data Drift Detection Summary")
    plt.xlabel("Drift Status")
    plt.ylabel("Number of Columns")

    plt.tight_layout()
    plt.savefig("data/processed/drift_summary.png")

    plt.show()

    print("Drift visualization saved successfully!")