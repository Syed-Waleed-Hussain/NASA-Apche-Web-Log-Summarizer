# NASA Apache Log Summarizer

## Project Aim
This project processes large NASA web server logs and converts raw text data into useful network insights. Manual review of millions of log entries is not practical, so this tool automates parsing, analysis, and report generation.

## Description
The project is written in Python. It reads Apache logs in Common Log Format, extracts fields like IP, time, request, and status, then performs traffic and error analysis. The results are shown through charts and a final HTML report.

The work focuses on practical learning of Regex, Pandas, and Matplotlib for real world network data analysis.

## Features
* Parsing of Apache log files using Regex
* Conversion of raw logs into structured records
* Traffic analysis using Pandas resample functions
* Error monitoring and detection of frequent failure IPs
* Charts for traffic trends and error activity
* Automatic HTML summary report

## System Architecture
The workflow follows a modular pipeline.

1. Ingestion and Parsing  
   File: parser.py  
   Extracts structured fields from each log entry.

2. Traffic Analysis  
   File: time_analysis.py  
   Computes hourly request trends.

3. Error Analysis  
   File: error_analysis.py  
   Identifies error spikes and top IPs.

4. Reporting  
   File: report_generator.py  
   Generates charts and creates the HTML report.

## Dataset
NASA Kennedy Space Center web server logs are used for analysis. The dataset contains hundreds of thousands of requests across multiple days.

## File Structure
```
NASA_Apache_Log_Summarizer
parser.py
time_analysis.py
error_analysis.py
report_generator.py
logs
nasa_log.txt
output
charts
report.html
README.md

```

## Installation
1. Install Python
2. Install required libraries
pip install pandas matplotlib


3. Place the log file inside the logs folder

## Usage
1. Run parser.py to extract structured data
2. Run analysis scripts to compute metrics
3. Run report_generator.py to create the HTML report
4. Open the report inside the output folder

## Sample Insights
* Total requests count
* Unique client IPs
* Success responses count
* Not Found errors
* Top requested resource
* Hourly traffic and error trends

## Future Scope
* Add bandwidth based analysis
* Add IP location mapping
* Add support for near real time log processing

## Authors
Syed Waleed Hussain  
Shayan Nemat  
Huzaifa Altaf
