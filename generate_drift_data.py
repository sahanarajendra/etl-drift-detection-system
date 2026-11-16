
import pandas as pd

# Load current dataset
df = pd.read_csv("data/raw/current.csv")

# Create a copy
drifted_df = df.copy()

# Introduce numerical drift
drifted_df["age"] = drifted_df["age"] + 15

drifted_df["balance"] = (
    drifted_df["balance"] + 10000
)

# Introduce categorical drift
drifted_df["job"] = "technician"

# Save drifted dataset
drifted_df.to_csv(
    "data/raw/drifted_current.csv",
    index=False
)

print("Drifted dataset created successfully!")

print("\nOriginal current dataset:")
print(df.head())

print("\nDrifted dataset:")
print(drifted_df.head())
