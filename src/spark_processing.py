
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, lower


# -----------------------------------------
# 1. CREATE SPARK SESSION
# -----------------------------------------


def create_spark_session():
    spark = (
        SparkSession.builder
        .appName("ETL Pipeline and Drift Detection")
        .master("local[2]")
        .config("spark.driver.memory", "1g")
        .config("spark.sql.shuffle.partitions", "4")
        .config("spark.ui.enabled", "false")
        .config("spark.sql.execution.arrow.pyspark.enabled", "false")
        .config("spark.sql.adaptive.enabled", "false")
        .getOrCreate()
    )

    print("PySpark Session Created Successfully!")
    return spark


# -----------------------------------------
# 2. DATA EXTRACTION
# -----------------------------------------

def read_data_with_spark(file_path, spark=None):

    if spark is None:
        spark = create_spark_session()

    df = spark.read.csv(
        file_path,
        header=True,
        inferSchema=True
    )

    print("\nPySpark Data Extraction Completed!")

    print("Total Rows:", df.count())
    print("Total Columns:", len(df.columns))

    df.show(5)

    return spark, df


# -----------------------------------------
# 3. DATA CLEANING
# -----------------------------------------

def clean_data_with_spark(df):

    print("\nStarting PySpark Data Cleaning...")

    # Remove duplicate records
    df = df.dropDuplicates()

    # Remove columns that contain only null values
    non_empty_columns = [
        c for c in df.columns
        if df.filter(col(c).isNotNull()).limit(1).count() > 0
    ]

    df = df.select(*non_empty_columns)

    # Clean string columns
    for field in df.schema.fields:

        column_name = field.name

        if field.dataType.simpleString() == "string":

            df = df.withColumn(
                column_name,
                trim(col(column_name))
            )

            df = df.withColumn(
                column_name,
                lower(col(column_name))
            )

            df = df.fillna(
                {column_name: "unknown"}
            )

    # Fill missing numeric values using median
    for field in df.schema.fields:

        column_name = field.name

        if field.dataType.simpleString() in [
            "integer", "long", "double", "float"
        ]:

            median_value = df.approxQuantile(
                column_name, [0.5], 0.01
            )

            if median_value:
                df = df.fillna(
                    {column_name: median_value[0]}
                )

    print("PySpark Data Cleaning Completed!")

    print("Remaining Missing Values:")

    for column_name in df.columns:
        missing = df.filter(
            col(column_name).isNull()
        ).count()

        print(column_name, ":", missing)

    print("Final Rows:", df.count())

    return df


# -----------------------------------------
# 4. DATA TRANSFORMATION
# -----------------------------------------

def transform_data_with_spark(df):

    print("\nStarting PySpark Data Transformation...")

    # Standardize column names
    for column_name in df.columns:

        new_name = (
            column_name.strip()
            .lower()
            .replace(" ", "_")
        )

        if new_name != column_name:
            df = df.withColumnRenamed(
                column_name, new_name
            )

    # Remove unnecessary whitespace from string columns
    for field in df.schema.fields:

        if field.dataType.simpleString() == "string":

            df = df.withColumn(
                field.name,
                trim(col(field.name))
            )

    print("PySpark Data Transformation Completed!")

    print("Transformed Rows:", df.count())
    print("Transformed Columns:", len(df.columns))

    return df
