from flask import Flask, jsonify, render_template # Import render_template
from sqlalchemy import create_engine, text
import pandas as pd
import os
app = Flask(__name__)

DB_CONNECTION_STRING = os.environ.get("DB_CONNECTION_STRING")
db_engine = create_engine(DB_CONNECTION_STRING)

# --- Page Route ---

@app.route("/dashboard")
def dashboard():
    """Serves the main dashboard HTML page."""
    return render_template('index.html')

# --- API Endpoints (No changes below this line) ---

@app.route("/")
def home():
    return "Welcome to the FinFlow Analytics API!"

@app.route("/api/stocks")
def get_all_stocks():
    try:
        with db_engine.connect() as connection:
            query = "SELECT DISTINCT ticker FROM stock_data ORDER BY ticker;"
            result = connection.execute(text(query))
            tickers = [row[0] for row in result.fetchall()]
        return jsonify(tickers)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/stock/<string:ticker>")
def get_stock_data(ticker):
    try:
        query = f"SELECT * FROM stock_data WHERE ticker = '{ticker.upper()}' ORDER BY trade_date DESC LIMIT 30;"
        df = pd.read_sql(query, db_engine)
        df['trade_date'] = df['trade_date'].astype(str)
        if df.empty:
            return jsonify({"error": f"No data found for ticker {ticker}"}), 404
        data = df.to_dict(orient='records')
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)