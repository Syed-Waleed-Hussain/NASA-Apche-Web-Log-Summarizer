# utils.py
import os
import time

# ----------------------------------------------------
#                UTILITY HELPER FUNCTIONS
# ----------------------------------------------------

def safe_int(value, default=0):
    """Safely converts a value to integer. Returns default on failure."""
    try:
        return int(value)
    except:
        return default

def safe_float(value, default=0.0):
    """Safely converts a value to float. Returns default on failure."""
    try:
        return float(value)
    except:
        return default

def clean_timestamp(ts):
    """Removes square brackets from timestamps"""
    return ts.replace("[", "").replace("]", "")

def file_size(path):
    """Returns human-readable file size"""
    if not os.path.exists(path):
        return "File not found"
    size = os.path.getsize(path)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"

def print_progress(current, total, step_percent=5):
    """
    Shows progress in terminal in steps of step_percent (default 5%).
    Avoids printing for every single line.
    """
    percent = (current / total) * 100
    # only print when current percent crosses next multiple of step_percent
    if percent >= print_progress.last_print + step_percent or current == total:
        print_progress.last_print = int(percent // step_percent) * step_percent
        print(f"\rProcessing: {percent:.1f}%", end="")
        if current == total:
            print()  # newline at the end

# Initialize static variable
print_progress.last_print = -5

def safe_read_lines(filepath):
    """Safely reads a file and returns lines."""
    if not os.path.exists(filepath):
        print(f"Error: File not found → {filepath}")
        return []
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            return f.readlines()
    except Exception as e:
        print(f"Failed to read file: {e}")
        return []

def log_error(message, logfile="reports/error_log.txt"):
    """Saves error messages to a separate log file."""
    os.makedirs(os.path.dirname(logfile), exist_ok=True)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(logfile, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
