# parser.py
import re
from processing.utils import clean_timestamp, safe_read_lines, log_error, print_progress

# ----------------------------------------------------
#                LOG PARSER FUNCTION
# ----------------------------------------------------
def parse_log_file(filepath):
    """
    Parses a NASA-style access log file.
    Extracts:
        - IP Address
        - Timestamp
        - Request String
        - Status Code
    Returns a list of tuples.
    """

    # Regex pattern for NASA access logs
    pattern = re.compile(r'(\d+\.\d+\.\d+\.\d+)\s-\s-\s\[(.*?)\]\s"(.*?)"\s(\d{3})')

    results = []

    # Read file safely (handles errors & encoding)
    lines = safe_read_lines(filepath)
    total = len(lines)

    if total == 0:
        log_error(f"Empty or unreadable file: {filepath}")
        return results

    print(f"Total lines to parse: {total}")

    # Loop through each log line
    for idx, line in enumerate(lines, start=1):
        match = pattern.search(line)
        if match:
            ip = match.group(1)
            timestamp = clean_timestamp(match.group(2))
            request = match.group(3)
            status = match.group(4)
            results.append((ip, timestamp, request, status))

        # Call new print_progress with percentage steps
        print_progress(idx, total)

    print("\nParsing completed!")

    return results
