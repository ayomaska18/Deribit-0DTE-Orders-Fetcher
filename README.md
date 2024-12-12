# Daily Trades Summary

This repository fetches and processes data for options that expire within a day. It includes tracking four types of orders: **buy calls**, **sell calls**, **buy puts**, and **sell puts**. The processed data is stored in an Excel file and updated to a Google Sheet.

---

## Features
1. **Data Fetching Scripts**:
   - Fetch latest trades data for SOL, ETH, and BTC options.
2. **Data Processing**:
   - Summarizes fetched data and uploads to a Google Sheet.
3. **Orchestration**:
   - Runs the fetching scripts in parallel and processes the summary after completion.

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/daily-trades-summary.git
   cd daily-trades-summary
   ```

2. **Set up the environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate        # Linux/Mac
   .\venv\Scripts\activate         # Windows
   ```

3. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage
1. Set up service_account.json for google sheet updating.

2. Run the orchestration script to execute all steps:
```bash
python main.py
```

## Practical Usage

Deploy the Script into your server, and set up scheduling tools such as Windows Task Scheduler or Cron for Linux at 8:00 AM UTC for precise data fetching.

---
