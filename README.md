# stocks_analyzer
Fetch, analyze, and save stock market data from Nasdaq and soon other stocks with an easy-to-use CLI

<p align="center"> <img src="https://img.shields.io/badge/Python-3.9%2B-blue.svg" /> <img src="https://img.shields.io/badge/CLI-Tool-orange.svg" /> <img src="https://img.shields.io/github/license/RachelitaSE/stocks_analyzer" /> <img src="https://img.shields.io/github/actions/workflow/status/RachelitaSE/stocks_analyzer/python-app.yml?label=CI" /> </p> <p align="center"> <strong>A lightweight, modular Python toolkit for downloading and storing real-time stock data from Nasdaq and other stocks.</strong><br/> Fetch the top stocks, save them as CSV or JSON, and build your own analytics pipeline on top. </p>

🚀 Features

✔ Fetch top stocks from Nasdaq’s public screener
✔ Save results as CSV or JSON
✔ Automatic format detection based on --out filename
✔ Built-in logging with --verbose and --quiet modes
✔ Optional throttling between requests (--throttle)
✔ Overwrite protection (--force)
✔ Highly modular architecture (clean separation of concerns)
✔ Retry logic for more reliable API calls
✔ 100% GitHub Pages-ready documentation

📦 Installation

Make sure you have Python 3.9+  installed.

Clone the repository:
```
git clone https://github.com/RachelitaSE/stocks_analyzer.git
cd stocks_analyzer
```

Install in editable mode:
```
pip install -e .
```
This gives you a global CLI command:
```
nasdaq-stocks
```

🌐 Website (GitHub Pages)

Once GitHub Pages is enabled:

➡️ https://rachelitase.github.io/stocks_analyzer/

This README becomes your website automatically.

🤝 Contributing

Contributions are welcome!
Feel free to submit issues, open PRs, or suggest new features.
