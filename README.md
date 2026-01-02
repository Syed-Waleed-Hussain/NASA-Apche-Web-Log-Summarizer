# 🚀 NASA Apache Log Summarizer

## 🎯 Project Aim
This project processes large NASA web server logs and converts raw text data into useful network insights. Manual review of millions of log entries is not practical, so this tool automates parsing, analysis, and report generation.

## 📌 Description
This project is written in Python. It reads Apache logs in Common Log Format, extracts fields like IP, timestamp, request, and status code, then performs traffic and error analysis. The results are presented through charts and a final HTML report.

The project demonstrates practical use of Regex, Pandas, and Matplotlib for real world network data analysis.

## ✨ Features
* 🧩 Parsing of Apache log files using Regex  
* 📊 Conversion of raw logs into structured records  
* ⏱ Traffic analysis using Pandas resample functions  
* ⚠ Error monitoring and identification of frequent failure IPs  
* 🖼 Visual charts for traffic and error behaviour  
* 📑 Automatic HTML summary report  

## 🧱 System Architecture
The workflow follows a modular pipeline.

1. 🗂 Ingestion and Parsing  
   File: parser.py  
   Extracts structured fields from each log entry.

2. ⏰ Traffic Analysis  
   File: time_analysis.py  
   Computes hourly request trends.

3. 🔎 Error Analysis  
   File: error_analysis.py  
   Identifies error spikes and top IPs.

4. 📝 Reporting  
   File: report_generator.py  
   Generates charts and creates the HTML report.

## 🗃 Dataset
NASA Kennedy Space Center web server logs are used for analysis. The dataset contains hundreds of thousands of HTTP requests across multiple days.

## 📁 File Structure
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

## ⚙ Installation
1. Install Python  
2. Install required libraries  
pip install pandas matplotlib

3. Place the log file inside the logs folder

## ▶ Usage
1. Run parser.py to extract structured data  
2. Run analysis scripts to compute metrics  
3. Run report_generator.py to generate the HTML report  
4. Open the report inside the output folder  

## 📈 Sample Insights
* ✔ Total requests count  
* 👥 Unique client IPs  
* ✅ Success responses count  
* ❌ Not Found errors  
* 📌 Top requested resource  
* ⏳ Hourly traffic and error trends  

## 🔮 Future Scope
* 📡 Bandwidth based analysis  
* 🌍 IP location mapping  
* ⚡ Near real time log processing support  

## 👤 Authors
Syed Waleed Hussain  
Shayan Nemat  
Huzaifa Altaf
