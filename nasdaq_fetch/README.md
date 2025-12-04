# Day 04 — Nasdaq Stock Data Downloader

## 📄 Overview
This project downloads **stock-market data** from the public **Nasdaq** website and saves it locally as either **CSV** or **JSON**.  
It uses Nasdaq’s open **screener API endpoint** to retrieve stock listings with fields such as:
- `symbol`
- `name`
- `last sale`
- `percent change`
- `market cap`

👉 Data source: [https://www.nasdaq.com/market-activity/stocks](https://www.nasdaq.com/market-activity/stocks)  
👉 Public JSON endpoint: [https://api.nasdaq.com/api/screener/stocks](https://api.nasdaq.com/api/screener/stocks)

No authentication or API key is required.


## How it works

- `nasdaq_client.py` — **business logic**
  - Handles HTTP requests to Nasdaq API
  - Parses the JSON response

- `storage.py` - **Storage utilities**
  - Saves stock data results to CSV or JSON (the user has to chooose)

- `cli.py` — **user interface (CLI)**
    gives the following data for a list of the top stock:
    "symbol"
    "name"
    "lastsale"
    "netchange"
    "pctchange"
    "marketCap"
    "url"

- Data files are saved under `data/`  
  (this folder is ignored by Git)

- need to install `requests` if it is not already installed

## How to run
For example:
```
pip install -e .
nasdaq-stocks --top 100 --format json --out day04/data/top100.json
```

## Interaction with AI
I used ChatGPT (GPT-5) to:
design the structure separating UI and business logic
write clean, minimal Python code for Nasdaq data fetching
