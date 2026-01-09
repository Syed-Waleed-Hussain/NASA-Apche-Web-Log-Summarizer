# processing/time_analysis.py
import pandas as pd
import os

def run_time_analysis(parsed_logs, output_dir="datasets/cleaned"):
    """
    Analyzes traffic over time and exports structured CSVs.
    """
    print(f"Running Time Analysis...")
    os.makedirs(output_dir, exist_ok=True)

    # Convert list of tuples to DataFrame
    df = pd.DataFrame(parsed_logs, columns=["ip", "timestamp", "request", "status"])

    # Convert timestamp to datetime objects
    # Format matches standard Apache: 01/Aug/1995:00:00:01 -0400
    df['timestamp'] = pd.to_datetime(
        df['timestamp'], 
        format="%d/%b/%Y:%H:%M:%S %z", 
        errors='coerce'
    )

    # Drop rows where timestamp parsing failed
    df = df.dropna(subset=['timestamp'])

    # 1. Hourly Analysis
    hourly_counts = df.set_index('timestamp').resample('H').size()
    hourly_counts.name = "request_count"
    hourly_csv = os.path.join(output_dir, "temporal_analysis_hourly.csv")
    hourly_counts.to_csv(hourly_csv)
    print(f"   -> Exported: {hourly_csv}")

    # 2. Daily Analysis
    daily_counts = df.set_index('timestamp').resample('D').size()
    daily_counts.name = "request_count"
    daily_csv = os.path.join(output_dir, "temporal_analysis_daily.csv")
    daily_counts.to_csv(daily_csv)
    print(f"   -> Exported: {daily_csv}")

    return df  # Return cleaned DF in case other modules need it