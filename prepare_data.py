
import pandas as pd
from sklearn.model_selection import train_test_split
from pathlib import Path

# 1. Read the original dataset
print("Reading original dataset...")

df = pd.read_csv(
    "data/raw/bank-full.csv",
    sep=";"
)

print("Dataset loaded successfully!")

# 2. Display dataset information
print("\nOriginal Dataset Shape:", df.shape)

print("\nFirst 5 Records:")
print(df.head())

# 3. Split the dataset into reference and current
reference, current = train_test_split(
    df,
    test_size=0.30,
    random_state=42,
    stratify=df["y"]
)

# 4. Create folders if they don't exist
Path("data/reference").mkdir(
    parents=True, exist_ok=True
)

Path("data/raw").mkdir(
    parents=True, exist_ok=True
)

# 5. Save datasets
reference.to_csv(
    "data/reference/reference.csv",
    index=False
)

current.to_csv(
    "data/raw/current.csv",
    index=False
)

# 6. Display final results
print("\nReference Dataset Shape:", reference.shape)
print("Current Dataset Shape:", current.shape)

print("\nBoth datasets saved successfully!")
