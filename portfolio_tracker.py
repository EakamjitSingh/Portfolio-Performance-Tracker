import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import os

# --- Configuration ---
PORTFOLIO_CSV_PATH = 'portfolio.csv'
REPORT_CSV_PATH = 'portfolio_performance_report.csv'
CHART_PNG_PATH = 'portfolio_distribution.png'

def load_portfolio(file_path):
    """
    Loads the portfolio data from a CSV file into a pandas DataFrame.
    
    Args:
        file_path (str): The path to the portfolio CSV file.
        
    Returns:
        pandas.DataFrame: A DataFrame containing portfolio data, or None if the file is not found.
    """
    if not os.path.exists(file_path):
        print(f"Error: Portfolio file not found at '{file_path}'")
        print("Please create it with columns: Ticker, Quantity, PurchasePrice")
        return None
    
    print(f"Loading portfolio from '{file_path}'...")
    portfolio_df = pd.read_csv(file_path)
    # Basic validation to ensure required columns exist
    required_columns = ['Ticker', 'Quantity', 'PurchasePrice']
    if not all(col in portfolio_df.columns for col in required_columns):
        print(f"Error: The CSV file must contain the columns: {', '.join(required_columns)}")
        return None
        
    return portfolio_df

def get_live_prices(tickers):
    """
    Retrieves the last closing price for a list of stock tickers.
    
    Args:
        tickers (list): A list of stock ticker symbols.
        
    Returns:
        dict: A dictionary mapping each ticker to its latest price.
    """
    print("Fetching live market data...")
    prices = {}
    for ticker_symbol in tickers:
        try:
            ticker_data = yf.Ticker(ticker_symbol)
            # Fetch the most recent closing price
            hist = ticker_data.history(period="1d")
            if not hist.empty:
                prices[ticker_symbol] = hist['Close'][0]
            else:
                print(f"Warning: Could not retrieve data for ticker '{ticker_symbol}'. It might be invalid.")
                prices[ticker_symbol] = 0.0
        except Exception as e:
            print(f"An error occurred while fetching data for {ticker_symbol}: {e}")
            prices[ticker_symbol] = 0.0
    return prices

def calculate_performance(portfolio_df):
    """
    Calculates performance metrics for the portfolio.
    
    Args:
        portfolio_df (pandas.DataFrame): The DataFrame with portfolio holdings.
        
    Returns:
        pandas.DataFrame: The DataFrame updated with performance metrics.
    """
    print("Calculating portfolio performance...")
    tickers = portfolio_df['Ticker'].unique().tolist()
    live_prices = get_live_prices(tickers)
    
    # Map live prices to the DataFrame
    portfolio_df['CurrentPrice'] = portfolio_df['Ticker'].map(live_prices)
    
    # Calculate performance metrics
    portfolio_df['PurchaseValue'] = portfolio_df['Quantity'] * portfolio_df['PurchasePrice']
    portfolio_df['CurrentValue'] = portfolio_df['Quantity'] * portfolio_df['CurrentPrice']
    portfolio_df['ProfitLoss'] = portfolio_df['CurrentValue'] - portfolio_df['PurchaseValue']
    
    # Calculate percentage return, handling potential division by zero
    portfolio_df['PercentageReturn'] = (portfolio_df['ProfitLoss'] / portfolio_df['PurchaseValue']) * 100
    portfolio_df['PercentageReturn'] = portfolio_df['PercentageReturn'].fillna(0) # Fill NaN for stocks with 0 purchase value
    
    return portfolio_df

def generate_summary_and_report(performance_df, file_path):
    """
    Prints a summary to the console and saves the detailed performance data to a CSV file.
    
    Args:
        performance_df (pandas.DataFrame): The DataFrame with performance data.
        file_path (str): The path to save the report CSV file.
    """
    # Calculate Totals
    total_purchase_value = performance_df['PurchaseValue'].sum()
    total_current_value = performance_df['CurrentValue'].sum()
    total_profit_loss = performance_df['ProfitLoss'].sum()
    
    # Avoid division by zero for total percentage return
    if total_purchase_value > 0:
        total_percentage_return = (total_profit_loss / total_purchase_value) * 100
    else:
        total_percentage_return = 0.0

    # Print Summary to Console
    print("\n" + "="*40)
    print("           PORTFOLIO SUMMARY")
    print("="*40)
    print(f"Total Portfolio Value: ${total_current_value:,.2f}")
    print(f"Total Profit/Loss: ${total_profit_loss:,.2f}")
    print(f"Total Portfolio Return: {total_percentage_return:.2f}%")
    print("="*40 + "\n")
    
    # Save detailed report to CSV
    print(f"Saving detailed performance report to '{file_path}'...")
    performance_df.to_csv(file_path, index=False)

def generate_visualization(performance_df, file_path):
    """
    Generates and saves a bar chart visualizing portfolio distribution.
    
    Args:
        performance_df (pandas.DataFrame): DataFrame with performance data.
        file_path (str): The path to save the chart image file.
    """
    print(f"Generating portfolio distribution chart to '{file_path}'...")
    
    # Group by ticker for a cleaner chart if there are multiple lots of the same stock
    chart_data = performance_df.groupby('Ticker')['CurrentValue'].sum().sort_values(ascending=False)
    
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 7))
    
    bars = ax.bar(chart_data.index, chart_data.values, color=plt.cm.viridis(chart_data.values / chart_data.values.max()))
    
    ax.set_ylabel('Current Market Value ($)', fontsize=12)
    ax.set_xlabel('Stock Ticker', fontsize=12)
    ax.set_title('Portfolio Distribution by Current Value', fontsize=16, fontweight='bold')
    
    # Format y-axis to display as currency
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Save the figure
    plt.savefig(file_path, dpi=300)
    plt.close() # Close the plot to free up memory

def main():
    """Main function to run the portfolio tracker."""
    print("--- Starting Portfolio Performance Tracker ---")
    
    # 1. Load Portfolio
    portfolio = load_portfolio(PORTFOLIO_CSV_PATH)
    if portfolio is None:
        print("--- Script execution failed. ---")
        return # Exit if portfolio loading failed

    # 2. Calculate Performance
    performance_data = calculate_performance(portfolio)

    # 3. Generate Report and Summary
    generate_summary_and_report(performance_data, REPORT_CSV_PATH)

    # 4. Generate Visualization
    generate_visualization(performance_data, CHART_PNG_PATH)
    
    print("\n--- Portfolio analysis complete. ---")
    print(f"Report: '{REPORT_CSV_PATH}'")
    print(f"Chart: '{CHART_PNG_PATH}'")

if __name__ == "__main__":
    # Ensure you have installed the required libraries:
    # pip install pandas yfinance matplotlib seaborn
    main()
