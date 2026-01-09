# processing/error_analysis.py
import pandas as pd
import os

def run_error_analysis(parsed_logs, output_dir="datasets/cleaned"):
    """
    Analyzes 4xx and 5xx errors and exports structured CSVs.
    """
    print(f"Running Error Analytics...")
    os.makedirs(output_dir, exist_ok=True)

    # Convert to DataFrame
    df = pd.DataFrame(parsed_logs, columns=["ip", "timestamp", "request", "status"])
    
    # Ensure status is numeric
    df["status"] = pd.to_numeric(df["status"], errors="coerce")

    # Filter for Errors (4xx Client Errors and 5xx Server Errors)
    error_df = df[df["status"] >= 400].copy()

    if error_df.empty:
        print("   -> No errors found in logs.")
        return

    # 1. Errors per IP
    ip_errors = error_df["ip"].value_counts().reset_index()
    ip_errors.columns = ["IP_Address", "Error_Count"]
    
    # Save to CSV
    error_csv = os.path.join(output_dir, "device_errors.csv")
    ip_errors.to_csv(error_csv, index=False)
    print(f"   -> Exported: {error_csv}")

    # 2. (Optional) Detailed Error Log
    # saves a detailed CSV with just the error rows
    detailed_csv = os.path.join(output_dir, "full_error_log.csv")
    error_df.to_csv(detailed_csv, index=False)
    print(f"   -> Exported: {detailed_csv}")