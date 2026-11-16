
import streamlit as st
import pandas as pd
from pathlib import Path
import time

from src.cleaning import clean_data
from src.data_quality import calculate_quality
from src.drift_detection import compare_datasets
from src.recommendations import generate_recommendations

from src.spark_processing import (
    create_spark_session,
    clean_data_with_spark,
    transform_data_with_spark
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="ETL Pipeline and Drift Detection",
    page_icon="📊",
    layout="wide"
)


# --------------------------------------------------
# DASHBOARD TITLE
# --------------------------------------------------

st.title("Data ETL Pipeline and Drift Detection System")

st.write(
    "Monitor data quality, detect data drift, "
    "and view automated recommendations."
)


# --------------------------------------------------
# 1. DATA QUALITY REPORT
# --------------------------------------------------

st.header("1. Data Quality Report")

quality_file = Path("data/processed/column_quality_report.csv")

if quality_file.exists():
    quality_df = pd.read_csv(quality_file)
    st.dataframe(quality_df, use_container_width=True)
else:
    st.warning("Data quality report not found.")


# --------------------------------------------------
# 2. DRIFT DETECTION REPORT
# --------------------------------------------------

st.header("2. Drift Detection Report")

drift_file = Path("data/processed/drifted_drift_report.csv")

if drift_file.exists():

    drift_df = pd.read_csv(drift_file)

    st.dataframe(drift_df, use_container_width=True)

    st.subheader("Drift Summary")

    drifted_count = (
        drift_df["Drift Status"] == "Drift Detected"
    ).sum()

    stable_count = (
        drift_df["Drift Status"] == "No Drift Detected"
    ).sum()

    col1, col2 = st.columns(2)

    col1.metric("Drifted Columns", int(drifted_count))
    col2.metric("Stable Columns", int(stable_count))

else:
    st.warning("Drift report not found.")


# --------------------------------------------------
# 3. DRIFT VISUALIZATION
# --------------------------------------------------

st.header("3. Drift Visualization")

image_path = Path("data/processed/drift_summary.png")

if image_path.exists():

    st.image(
        str(image_path),
        caption="Data Drift Detection Summary",
        use_container_width=True
    )

else:
    st.warning("Drift visualization not found.")


# --------------------------------------------------
# 4. AUTOMATED RECOMMENDATIONS
# --------------------------------------------------

st.header("4. Automated Recommendations")

recommendation_file = Path(
    "data/processed/recommendations.csv"
)

if recommendation_file.exists():

    recommendations_df = pd.read_csv(recommendation_file)

    st.dataframe(
        recommendations_df,
        use_container_width=True
    )

    st.subheader("Recommendation Summary")

    high_priority = (
        recommendations_df["Priority"] == "High"
    ).sum()

    medium_priority = (
        recommendations_df["Priority"] == "Medium"
    ).sum()

    low_priority = (
        recommendations_df["Priority"] == "Low"
    ).sum()

    col1, col2, col3 = st.columns(3)

    col1.metric("High Priority", int(high_priority))
    col2.metric("Medium Priority", int(medium_priority))
    col3.metric("Low Priority", int(low_priority))

else:
    st.warning("Recommendations not found.")


# --------------------------------------------------
# 5. UPLOAD YOUR OWN DATASETS
# --------------------------------------------------

st.header("5. Upload Your Own Datasets")

st.subheader("Select ETL Processing Engine")

processing_engine = st.selectbox(
    "Choose your processing engine:",
    ["Pandas", "PySpark"]
)

if processing_engine == "Pandas":
    st.info("Pandas engine selected for ETL processing.")
else:
    st.info("PySpark engine selected for ETL processing.")


st.write(
    "Upload a reference CSV and a current CSV "
    "to perform data quality analysis and drift detection."
)

reference_file = st.file_uploader(
    "Upload Reference Dataset",
    type=["csv"],
    key="reference_upload"
)

current_file = st.file_uploader(
    "Upload Current Dataset",
    type=["csv"],
    key="current_upload"
)


# --------------------------------------------------
# INITIALIZE SESSION STATE
# --------------------------------------------------

if "upload_results" not in st.session_state:
    st.session_state.upload_results = None


# --------------------------------------------------
# 6. ANALYZE UPLOADED DATASETS
# --------------------------------------------------

if st.button("Analyze Uploaded Datasets"):

    if reference_file is None or current_file is None:

        st.warning(
            "Please upload both reference and current CSV files."
        )

    else:

        spark = None

        try:

            # Read uploaded CSV files
            reference_df = pd.read_csv(reference_file)
            current_df = pd.read_csv(current_file)

            # Check columns
            if set(reference_df.columns) != set(current_df.columns):

                st.error(
                    "Both datasets must contain the same columns."
                )

            else:

                # Match column order
                current_df = current_df[reference_df.columns]

                # --------------------------------------------------
                # START ETL PERFORMANCE TIMER
                # --------------------------------------------------

                start_time = time.perf_counter()

                # --------------------------------------------------
                # PANDAS ETL PROCESSING
                # --------------------------------------------------

                if processing_engine == "Pandas":

                    st.info("Processing data using Pandas...")

                    cleaned_reference = clean_data(reference_df)

                    cleaned_current = clean_data(current_df)

                # --------------------------------------------------
                # PYSPARK ETL PROCESSING
                # --------------------------------------------------

                else:

                    st.info("Processing data using PySpark...")

                    spark = create_spark_session()

                    try:

                        # Convert Pandas DataFrames to Spark DataFrames
                        reference_spark = spark.createDataFrame(
                            reference_df
                        )

                        current_spark = spark.createDataFrame(
                            current_df
                        )

                        # Data cleaning
                        cleaned_reference_spark = clean_data_with_spark(
                            reference_spark
                        )

                        cleaned_current_spark = clean_data_with_spark(
                            current_spark
                        )

                        # Data transformation
                        transformed_reference_spark = transform_data_with_spark(
                            cleaned_reference_spark
                        )

                        transformed_current_spark = transform_data_with_spark(
                            cleaned_current_spark
                        )

                        # Convert Spark DataFrames to Pandas
                        # for existing quality and drift functions
                        cleaned_reference = (
                            transformed_reference_spark.toPandas()
                        )

                        cleaned_current = (
                            transformed_current_spark.toPandas()
                        )

                    finally:

                        # Stop Spark session
                        spark.stop()
                        spark = None

                # --------------------------------------------------
                # CALCULATE ETL PROCESSING TIME
                # --------------------------------------------------

                processing_time = (
                    time.perf_counter() - start_time
                )

                st.success(
                    f"{processing_engine} ETL processing completed!"
                )

                # --------------------------------------------------
                # DATA QUALITY ANALYSIS
                # --------------------------------------------------

                st.info("Calculating data quality...")

                quality_report, column_info = calculate_quality(
                    cleaned_reference
                )

                # --------------------------------------------------
                # DRIFT DETECTION
                # --------------------------------------------------

                st.info("Detecting data drift...")

                drift_report = compare_datasets(
                    cleaned_reference,
                    cleaned_current
                )

                # --------------------------------------------------
                # AUTOMATED RECOMMENDATIONS
                # --------------------------------------------------

                recommendations = generate_recommendations(
                    quality_report,
                    drift_report
                )

                recommendations_df = pd.DataFrame(
                    recommendations
                )

                # --------------------------------------------------
                # STORE RESULTS
                # --------------------------------------------------

                st.session_state.upload_results = {

                    "quality_report": quality_report,

                    "column_info": column_info,

                    "drift_report": drift_report,

                    "recommendations_df": recommendations_df,

                    "processing_engine": processing_engine,

                    "processing_time": processing_time
                }

                st.success(
                    f"{processing_engine} analysis completed successfully!"
                )

        except Exception as e:

            st.error(f"Analysis failed: {e}")

        finally:

            # Ensure Spark is stopped even if an error occurs
            if spark is not None:
                spark.stop()


# --------------------------------------------------
# 7. DISPLAY UPLOADED DATASET RESULTS
# --------------------------------------------------

if st.session_state.upload_results is not None:

    results = st.session_state.upload_results

    quality_report = results["quality_report"]

    column_info = results["column_info"]

    drift_report = results["drift_report"]

    recommendations_df = results["recommendations_df"]

    selected_engine = results["processing_engine"]

    processing_time = results["processing_time"]


    # --------------------------------------------------
    # PERFORMANCE REPORT
    # --------------------------------------------------

    st.header("7. ETL Performance Report")

    st.write(
        f"**Processing Engine Used:** {selected_engine}"
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "ETL Processing Time",
        f"{processing_time:.4f} seconds"
    )

    col2.metric(
        "Processing Engine",
        selected_engine
    )


    # --------------------------------------------------
    # QUALITY REPORT
    # --------------------------------------------------

    st.subheader("Uploaded Dataset Quality Report")

    st.json(quality_report)

    st.dataframe(
        column_info,
        use_container_width=True
    )


    # --------------------------------------------------
    # DRIFT REPORT
    # --------------------------------------------------

    st.subheader("Uploaded Dataset Drift Report")

    st.dataframe(
        drift_report,
        use_container_width=True
    )


    # --------------------------------------------------
    # DRIFT SUMMARY
    # --------------------------------------------------

    st.subheader("Uploaded Dataset Drift Summary")

    drifted_count = (
        drift_report["Drift Status"] == "Drift Detected"
    ).sum()

    stable_count = (
        drift_report["Drift Status"] == "No Drift Detected"
    ).sum()

    col1, col2 = st.columns(2)

    col1.metric(
        "Drifted Columns",
        int(drifted_count)
    )

    col2.metric(
        "Stable Columns",
        int(stable_count)
    )


    # --------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------

    st.subheader("Uploaded Dataset Recommendations")

    st.dataframe(
        recommendations_df,
        use_container_width=True
    )


    # --------------------------------------------------
    # 8. DOWNLOAD REPORTS
    # --------------------------------------------------

    st.header("8. Download Analysis Reports")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.download_button(
            label="Download Quality Report",
            data=column_info.to_csv(index=False),
            file_name="data_quality_report.csv",
            mime="text/csv"
        )

    with col2:

        st.download_button(
            label="Download Drift Report",
            data=drift_report.to_csv(index=False),
            file_name="drift_detection_report.csv",
            mime="text/csv"
        )

    with col3:

        st.download_button(
            label="Download Recommendations",
            data=recommendations_df.to_csv(index=False),
            file_name="recommendations.csv",
            mime="text/csv"
        )

    st.success(
        "Uploaded Dataset Analysis Completed Successfully!"
    )


# --------------------------------------------------
# DASHBOARD COMPLETION MESSAGE
# --------------------------------------------------

st.success("Dashboard loaded successfully!")
