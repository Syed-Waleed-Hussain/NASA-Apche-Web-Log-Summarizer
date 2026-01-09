import os
from pathlib import Path
from collections import Counter

import pandas as pd
import matplotlib.pyplot as plt

def ensure_dirs():
    Path("visuals").mkdir(exist_ok=True)
    Path("report").mkdir(exist_ok=True)

def build_dataframe_from_parsed(parsed_logs):
  
    df = pd.DataFrame(parsed_logs, columns=["ip", "timestamp", "request", "status"])
    # Parse the Apache/NASA timestamp explicitly (e.g. 01/Aug/1995:00:00:01 -0400)
    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        format="%d/%b/%Y:%H:%M:%S %z",
        errors="coerce"
    )
   
    df = df.dropna(subset=["timestamp", "ip"]).copy()

    # split request into method and url 
    def split_req(r):
        try:
            parts = str(r).split()
            method = parts[0] if len(parts) > 0 else None
            url = parts[1] if len(parts) > 1 else None
            return pd.Series([method, url])
        except Exception:
            return pd.Series([None, None])

    df[["method", "url"]] = df["request"].apply(split_req)
    # convert status to integer
    df["status"] = pd.to_numeric(df["status"], errors="coerce").astype("Int64")
    return df

# ---------------- Plots ----------------
def plot_traffic_per_hour(df, out="visuals/traffic_per_hour.png"):
    s = df["timestamp"].dt.hour.value_counts().reindex(range(24), fill_value=0).sort_index()
    plt.figure(figsize=(10,4))
    s.plot(kind="line", marker="o")
    plt.title("Traffic per Hour")
    plt.xlabel("Hour (0-23)")
    plt.ylabel("Requests")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out

def plot_traffic_per_day(df, out="visuals/traffic_per_day.png"):
    s = df["timestamp"].dt.date.value_counts().sort_index()
    if s.empty:
        return None
    plt.figure(figsize=(12,4))
    s.plot(kind="bar")
    plt.title("Traffic per Day")
    plt.xlabel("Date")
    plt.ylabel("Requests")
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out

def plot_error_spikes(df, out="visuals/error_spikes.png"):
    errs = df[df["status"] >= 400]
    if errs.empty:
        return None
    s = errs["timestamp"].dt.hour.value_counts().reindex(range(24), fill_value=0).sort_index()
    plt.figure(figsize=(10,4))
    s.plot(kind="bar")
    plt.title("Hourly Error Spikes (status >= 400)")
    plt.xlabel("Hour")
    plt.ylabel("Errors")
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out

def plot_top_urls(df, out="visuals/top_urls.png", top_n=15):
    s = df["url"].value_counts().head(top_n)
    if s.empty:
        return None
    plt.figure(figsize=(10, max(4, 0.35 * len(s))))
    s.plot(kind="barh")
    plt.gca().invert_yaxis()
    plt.title(f"Top {len(s)} Requested URLs")
    plt.xlabel("Requests")
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out

def plot_template_frequency(df, out="visuals/templates.png", top_n=20):
    df2 = df.copy()
    df2["template"] = df2["method"].fillna("-").astype(str) + "_" + df2["status"].astype(str)
    s = df2["template"].value_counts().head(top_n)
    if s.empty:
        return None
    plt.figure(figsize=(10, max(4, 0.35 * len(s))))
    s.plot(kind="bar")
    plt.title("Template Frequency (METHOD_STATUS)")
    plt.xlabel("Count")
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out

def plot_top_ip_errors(df, out="visuals/device_ip_errors.png", top_n=15):
    errs = df[df["status"] >= 400]
    s = errs["ip"].value_counts().head(top_n)
    if s.empty:
        return None
    plt.figure(figsize=(10, max(4, 0.35 * len(s))))
    s.plot(kind="barh")
    plt.gca().invert_yaxis()
    plt.title("Top IPs by Error Count")
    plt.xlabel("Error Count")
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out

# ---------------- HTML ----------------
def make_summary_tables_html(summary, top_n=15):
    html = ""
    html += "<h3>Status Code Counts</h3>\n"
    if "status_counts" in summary:
        html += "<ul>\n"
        for code, cnt in summary["status_counts"].items():
            html += f"<li>{code} : {cnt}</li>\n"
        html += "</ul>\n"
    # top urls
    html += "<h3>Top URLs</h3>\n"
    html += "<table border='1' cellpadding='4'><tr><th>URL</th><th>Hits</th></tr>"
    for url, cnt in summary.get("top_urls", [])[:top_n]:
        html += f"<tr><td>{url}</td><td>{cnt}</td></tr>"
    html += "</table>\n"
    # top ips
    html += "<h3>Top IPs</h3>\n"
    html += "<table border='1' cellpadding='4'><tr><th>IP</th><th>Hits</th></tr>"
    for ip, cnt in summary.get("top_ips", [])[:top_n]:
        html += f"<tr><td>{ip}</td><td>{cnt}</td></tr>"
    html += "</table>\n"
    return html

def generate_html_report(df, summary, images_map, out_html="report/summary_report.html"):
    ensure_dirs()
    title = "Network Log Summary Report"
    time_range = f"{df['timestamp'].min()} → {df['timestamp'].max()}" if not df.empty else "N/A"
    total_reqs = len(df)

    html = f"""<!doctype html>
<html>
<head><meta charset="utf-8"><title>{title}</title>
<style>body{{font-family: Arial, sans-serif; margin:20px}} img{{max-width:100%;height:auto;border:1px solid #ddd;padding:6px;background:#fff}} table{{border-collapse:collapse;margin-bottom:20px}} td, th{{padding:6px;border:1px solid #ccc}}</style>
</head>
<body>
<h1>{title}</h1>
<p><strong>Total requests:</strong> {total_reqs}</p>
<p><strong>Time range:</strong> {time_range}</p>
<hr/>
<h2>Charts</h2>
"""

    # embed charts with paths relative to report/ file location (report/summary_report.html)
    for label, path in images_map.items():
        if path:
            html += f"<h3>{label}</h3>\n<img src=\"../{path}\" alt=\"{label}\" />\n"

    html += "<hr/>\n<h2>Tables</h2>\n"
    html += make_summary_tables_html(summary)
    html += "\n</body></html>"

    Path(out_html).parent.mkdir(parents=True, exist_ok=True)
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html)
    return out_html

# ---------------- Master ----------------
def generate_full_report(parsed_logs, summary):
    ensure_dirs()
    df = build_dataframe_from_parsed(parsed_logs)

    images = {}
    images["Traffic per Hour"] = plot_traffic_per_hour(df, out="visuals/traffic_per_hour.png")
    images["Traffic per Day"] = plot_traffic_per_day(df, out="visuals/traffic_per_day.png")
    images["Error Spikes"] = plot_error_spikes(df, out="visuals/error_spikes.png")
    images["Top Requested URLs"] = plot_top_urls(df, out="visuals/top_urls.png")
    images["Template Frequency"] = plot_template_frequency(df, out="visuals/templates.png")
    images["Top IPs by Errors"] = plot_top_ip_errors(df, out="visuals/device_ip_errors.png")

    html_path = generate_html_report(df, summary, images, out_html="report/summary_report.html")
    print(f"HTML report generated: {html_path}")
    print("Charts saved to folder: visuals/")
    return html_path
