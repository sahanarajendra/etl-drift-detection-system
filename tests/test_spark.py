
from src.spark_processing import (
    read_data_with_spark,
    clean_data_with_spark,
    transform_data_with_spark
)

spark = None

try:
    # 1. Data Extraction
    print("\n========== DATA EXTRACTION ==========")

    spark, df = read_data_with_spark(
        "data/raw/spark_test.csv"
    )

    # 2. Data Cleaning
    print("\n========== DATA CLEANING ==========")

    cleaned_df = clean_data_with_spark(df)

    cleaned_df.show()

    # 3. Data Transformation
    print("\n========== DATA TRANSFORMATION ==========")

    transformed_df = transform_data_with_spark(
        cleaned_df
    )

    transformed_df.show()

    print("\nPySpark ETL Pipeline Completed Successfully!")

finally:
    if spark is not None:
        spark.stop()
        print("\nSpark Session Stopped Successfully!")
