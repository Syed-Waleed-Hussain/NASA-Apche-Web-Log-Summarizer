# summarizer.py
from collections import Counter
import os
import matplotlib.pyplot as plt

# ----------------------------------------------------
#             LOG SUMMARIZER FUNCTIONS
# ----------------------------------------------------
def summarize_logs(parsed_logs, top_n=15):
    """
    Takes parsed logs from parser.py and returns a summary dictionary
    containing key analytics like status code counts, top URLs, top IPs, etc.
    """
    summary = {}

    # Total number of requests
    summary["total_requests"] = len(parsed_logs)

    # List of all client IPs
    ips = [entry[0] for entry in parsed_logs]
    summary["unique_ips"] = len(set(ips))

    # Status code distribution
    status_codes = [entry[3] for entry in parsed_logs]
    summary["status_counts"] = dict(Counter(status_codes))

    # Requested URLs (extracted from the request field)
    urls = []
    for entry in parsed_logs:
        parts = entry[2].split(" ")
        if len(parts) > 1:
            urls.append(parts[1])
    summary["top_urls"] = Counter(urls).most_common(top_n)

    # Top N most active IPs
    summary["top_ips"] = Counter(ips).most_common(top_n)

    return summary

# ----------------------------------------------------
#              SAVE SUMMARY TO TEXT FILE
# ----------------------------------------------------
def save_summary(summary, output_file="reports/summary_output.txt"):
    """
    Saves the summary into a readable text file.
    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w") as f:
        f.write("========== Network Log Summary ==========\n\n")
        f.write(f"Total Requests: {summary['total_requests']}\n")
        f.write(f"Unique IPs: {summary['unique_ips']}\n\n")

        f.write("---- Status Code Counts ----\n")
        for code, count in summary["status_counts"].items():
            f.write(f"  {code} : {count}\n")

        f.write("\n---- Top 15 Requested URLs ----\n")
        for url, count in summary["top_urls"]:
            f.write(f"  {url} : {count}\n")

        f.write("\n---- Top 15 Active IPs ----\n")
        for ip, count in summary["top_ips"]:
            f.write(f"  {ip} : {count}\n")

# ----------------------------------------------------
#              GENERATE VISUAL CHARTS
# ----------------------------------------------------
def plot_summary(summary, output_dir="reports/charts/"):
    """
    Generates visual charts for:
    - Status code distribution (pie chart with legend)
    - Top URLs (horizontal bar graph)
    - Top IPs (horizontal bar graph)
    """
    os.makedirs(output_dir, exist_ok=True)

    # ---------------- Pie Chart: Status Codes ----------------
    plt.figure(figsize=(8, 8))
    labels = list(summary["status_counts"].keys())
    values = list(summary["status_counts"].values())
    colors = plt.get_cmap("Set3").colors[:len(labels)]

    wedges, _, autotexts = plt.pie(
        values,
        autopct="%1.1f%%",
        startangle=140,
        colors=colors,
        textprops={"fontsize": 12}
    )

    plt.title("HTTP Status Code Distribution", fontsize=16, fontweight="bold")

    plt.legend(
        wedges,
        [f"{labels[i]} ({values[i]} requests)" for i in range(len(labels))],
        title="Status Codes",
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        fontsize=12
    )

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "status_codes.png"), dpi=300)
    plt.close()

    # ---------------- Bar Chart: Top URLs ----------------
    if summary["top_urls"]:
        urls, counts = zip(*summary["top_urls"])
        plt.figure(figsize=(10, 6))
        plt.barh(urls, counts, color="skyblue")
        plt.xlabel("Number of Requests")
        plt.title(f"Top {len(urls)} Requested URLs", fontsize=14, fontweight="bold")
        plt.gca().invert_yaxis()  # largest at top
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "top_urls.png"), dpi=300)
        plt.close()

    # ---------------- Bar Chart: Top IPs ----------------
    if summary["top_ips"]:
        ips, counts = zip(*summary["top_ips"])
        plt.figure(figsize=(10, 6))
        plt.barh(ips, counts, color="lightgreen")
        plt.xlabel("Number of Requests")
        plt.title(f"Top {len(ips)} Active IPs", fontsize=14, fontweight="bold")
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "top_ips.png"), dpi=300)
        plt.close()
