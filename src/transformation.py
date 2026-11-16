
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def transform_data(reference_df, current_df):

    print("\nStarting Data Transformation...")

    # Create copies
    reference_df = reference_df.copy()
    current_df = current_df.copy()

    # Check whether both datasets have the same columns
    if set(reference_df.columns) != set(current_df.columns):
        raise ValueError(
            "Reference and current datasets have different columns."
        )

    # Keep the same column order
    current_df = current_df[reference_df.columns]

    # Identify numerical columns
    numeric_columns = reference_df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    # Identify categorical columns
    categorical_columns = reference_df.select_dtypes(
        include=["object", "category", "string"]
    ).columns.tolist()

    print("Numerical columns:", len(numeric_columns))
    print("Categorical columns:", len(categorical_columns))

    # Create preprocessing pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                StandardScaler(),
                numeric_columns
            ),
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore"),
                categorical_columns
            )
        ],
        remainder="drop"
    )

    # Fit only on reference data
    reference_transformed = preprocessor.fit_transform(
        reference_df
    )

    # Apply the same transformation to current data
    current_transformed = preprocessor.transform(
        current_df
    )

    # Get transformed feature names
    feature_names = preprocessor.get_feature_names_out()

    # Convert results into DataFrames
    reference_result = pd.DataFrame(
        reference_transformed,
        columns=feature_names,
        index=reference_df.index
    )

    current_result = pd.DataFrame(
        current_transformed,
        columns=feature_names,
        index=current_df.index
    )

    print("\nData Transformation Completed!")

    print("Reference transformed shape:",
          reference_result.shape)

    print("Current transformed shape:",
          current_result.shape)

    return reference_result, current_result, preprocessor
