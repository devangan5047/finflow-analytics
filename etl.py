import pandas as pd
import yfinance as yf
from sqlalchemy import create_engine

# --- 1. EXTRACT ---
def extract_stock_data(ticker):
    """Fetches historical stock data for the given ticker."""
    print(f"Fetching data for {ticker}...")
    stock = yf.Ticker(ticker)
    df = stock.history(period="3mo")
    df['ticker'] = ticker
    return df

# --- 2. TRANSFORM ---
def transform_data(df):
    print("Calculating 50-day moving average...")
    df['moving_average_50'] = df['Close'].rolling(window=50).mean()
    df_transformed = df[['ticker', 'Close', 'moving_average_50']].copy()
    df_transformed.rename(columns={'Close': 'price'}, inplace=True)
    return df_transformed.dropna()

# --- 3. LOAD ---
def load_data_to_db(df, db_engine):
    print("Loading data into the database...")
    df.to_sql(
        'stock_data',
        con=db_engine,
        if_exists='append',
        index=True,
        index_label='trade_date'
    )
    print("Data loaded successfully!")


# --- Main Execution ---
if __name__ == "__main__":
    TICKERS_TO_PROCESS = ['AAPL', 'MSFT', 'GOOGL']

    # Read the connection string from an environment variable
    DB_CONNECTION_STRING = os.environ.get("DB_CONNECTION_STRING")

    if not DB_CONNECTION_STRING:
        raise ValueError("DB_CONNECTION_STRING environment variable not set.")

    db_engine = create_engine(DB_CONNECTION_STRING)

    for ticker in TICKERS_TO_PROCESS:
        try:
            data = extract_stock_data(ticker)
            transformed_data = transform_data(data)
            load_data_to_db(transformed_data, db_engine)
        except Exception as e:
            print(f"Failed to process {ticker}. Error: {e}")