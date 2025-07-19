# Portfolio Performance Tracker

A simple yet powerful Python script to track the performance of your stock portfolio. This tool automates the retrieval of live stock prices, calculates key performance metrics, and generates a visual report of your portfolio's distribution.

---

## Features

- **Live Data:** Fetches the latest stock prices using the `yfinance` library.
- **Key Metrics:** Automatically calculates the current market value, total profit/loss, and percentage return for each stock and for the overall portfolio.
- **Detailed Reporting:** Generates a `portfolio_performance_report.csv` file with a detailed breakdown of each holding.
- **Data Visualization:** Creates a bar chart (`portfolio_distribution.png`) to visually represent the value distribution across your assets.
- **User-Friendly:** Packaged into a single, easy-to-run script that requires minimal setup.

---

## Prerequisites

Before you begin, ensure you have Python installed on your system. You will also need to install the following libraries:

```bash
pip install pandas yfinance matplotlib seaborn
```

---

## How to Use

1.  **Create Your Portfolio File:**
    * Create a file named `portfolio.csv` in the same directory as the script.
    * This file must have three columns: `Ticker`, `Quantity`, and `PurchasePrice`.
    * Populate it with your stock holdings. For example:

    ```csv
    Ticker,Quantity,PurchasePrice
    AAPL,15,170.50
    MSFT,10,305.20
    GOOGL,7,135.80
    NVDA,25,450.75
    ```

2.  **Run the Script:**
    * Open a terminal or command prompt.
    * Navigate to the directory where you saved the `portfolio_tracker.py` and `portfolio.csv` files.
    * Execute the script using the following command:

    ```bash
    python portfolio_tracker.py
    ```

---

## Output

After the script runs successfully, it will produce two new files in your project directory:

1.  **`portfolio_performance_report.csv`**: A detailed CSV report containing the following columns for each stock:
    * `Ticker`
    * `Quantity`
    * `PurchasePrice`
    * `CurrentPrice`
    * `PurchaseValue`
    * `CurrentValue`
    * `ProfitLoss`
    * `PercentageReturn`

2.  **`portfolio_distribution.png`**: A bar chart image that visually displays the current market value of each stock in your portfolio, helping you quickly see your largest holdings.

A summary of your portfolio's total value and performance will also be printed directly to the console.
