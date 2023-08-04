import yfinance as yf
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def update_config(action, ticker):
    with open('config.txt', 'r') as f:
        tickers = f.read().splitlines()
    if action == 'add':
        if ticker not in tickers:
            tickers.append(ticker)
    elif action == 'remove':
        if ticker in tickers:
            tickers.remove(ticker)
    with open('config.txt', 'w') as f:
        f.write('\n'.join(tickers))


def download_finance_data(company):  # downloading data by company name
    data = yf.download(company, period="max")
    return data


def load_data_to_db(company, data, db_path):  # loding data into database
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS finance_data (company text, date text, open real, high real, low real, 
    close real, adj_close real, volume integer,PRIMARY KEY (company, date))''')
    for index, row in data.iterrows():
        open_price = round(row['Open'], 4)
        high_price = round(row['High'], 4)
        low_price = round(row['Low'], 4)
        close_price = round(row['Close'], 4)
        adj_close_price = round(row['Adj Close'], 4)
        c.execute("INSERT OR REPLACE INTO finance_data VALUES (?,?, ?, ?, ?, ?, ?, ?)", (
            company, index.strftime('%Y-%m-%d'), row['Open'], row['High'], row['Low'], row['Close'], row['Adj Close'],
            row['Volume']))
    conn.commit()
    conn.close()


# getting stock data by company name
@app.route('/stocks_of/<company>', methods=['GET'])
def get_stock_data_by_company_name(company):
    conn = sqlite3.connect('finance_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM finance_data WHERE company=?", (company,))
    rows = c.fetchall()
    conn.close()
    return jsonify(rows)


# getting stock data by company date
@app.route('/stocks_on/<date>', methods=['GET'])
def get_stock_data_by_date(date):
    conn = sqlite3.connect('finance_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM finance_data WHERE date=?", (date,))
    rows = c.fetchall()
    conn.close()
    return jsonify(rows)


# getting stock data by company name and date
@app.route('/stocks_of_on/<company>/<date>', methods=['GET'])
def get_stock_data_by_company_name_date(company, date):
    conn = sqlite3.connect('finance_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM finance_data WHERE company=? and date=?", (company, date))
    rows = c.fetchall()
    conn.close()
    return jsonify(rows)


# updating stock data by company name and date
@app.route('/stocks_update/<company>/<date>', methods=['POST', 'PATCH'])
def update_company_stock_data(company, date):
    body_data = request.get_json()
    open_price1 = body_data['open_price']
    high_price1 = body_data['high_price']
    low_price1 = body_data['low_price']
    adj_close1 = body_data['adj_close']
    close_price1 = body_data['close_price']
    volume1 = body_data['volume']

    conn = sqlite3.connect('finance_data.db')
    c = conn.cursor()
    c.execute(
        "UPDATE finance_data SET open=?, high=?, low=?, close=?, adj_close=?, volume=? WHERE company=? AND date=?",
        (open_price1, high_price1, low_price1, close_price1, adj_close1, volume1, company, date))
    conn.commit()
    conn.close()
    return "success"
    
@app.route('/')
def index():
    return render_template('index.html')

def main():
    # opening config.txt in read mode
    with open('config.txt', 'r') as file:
        companies = file.read().splitlines()
    db_path = 'finance_data.db'
    for company in companies:
        data = download_finance_data(company)
        load_data_to_db(company, data, db_path)
    app.run()


main()
