
def generate_recommendations(quality_report, drift_report):

    recommendations = []

    # 1. Check missing values
    if quality_report["Missing Percentage"] > 5:

        recommendations.append({
            "Issue": "Missing Values",
            "Recommendation": (
                "High missing values detected. "
                "Review the data cleaning process."
            ),
            "Priority": "High"
        })

    elif quality_report["Missing Values"] > 0:

        recommendations.append({
            "Issue": "Missing Values",
            "Recommendation": (
                "Some missing values exist. "
                "Review incomplete records."
            ),
            "Priority": "Medium"
        })

    # 2. Check duplicate records
    if quality_report["Duplicate Rows"] > 0:

        recommendations.append({
            "Issue": "Duplicate Records",
            "Recommendation": (
                "Remove duplicate records "
                "before further processing."
            ),
            "Priority": "Medium"
        })

    # 3. Check drifted columns
    drifted_columns = drift_report[
        drift_report["Drift Status"] == "Drift Detected"
    ]

    for _, row in drifted_columns.iterrows():

        column = row["Column"]

        recommendations.append({
            "Issue": f"Drift in {column}",
            "Recommendation": (
                f"Investigate the distribution changes "
                f"in the {column} column."
            ),
            "Priority": "High"
        })

    # 4. Default recommendation
    if not recommendations:

        recommendations.append({
            "Issue": "No Major Issues",
            "Recommendation": (
                "Data quality and drift checks look stable. "
                "Continue monitoring incoming data."
            ),
            "Priority": "Low"
        })

    return recommendations
