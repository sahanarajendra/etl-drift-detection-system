
import pandas as pd
from pathlib import Path


def extract_data(file_path):

    """
    Extract data from a CSV file.

    Parameters:
        file_path: Path of the CSV file

    Returns:
        Pandas DataFrame
    """

    try:

        # Check whether file exists
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        # Read CSV file
        df = pd.read_csv(file_path)

        # Display extraction information
        print("Data extracted successfully!")
        print("File:", file_path)
        print("Rows:", df.shape[0])
        print("Columns:", df.shape[1])

        return df

    except Exception as e:

        print("Extraction failed:", e)

        raise
