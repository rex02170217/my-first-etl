import requests
import sqlite3
from datetime import datetime

# Step 1: Extract  
print(" Extract: 抓取比特幣最新價格...")
# 公開 API：指定要看 BTC 對 USDT 的價格
url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
response = requests.get(url)
raw_data = response.json()


# Step 2: Transform 

print(" Transform: 整理價格與時間...")
# CoinGecko 回傳的格式：{"bitcoin": {"usd": 65432.10}}
symbol = "BTC/USD"
btc_price = float(raw_data['bitcoin']['usd']) 
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print(f"   -> 整理完畢！目前 {symbol} 價格：${btc_price}")

# Step 3: Load 

print(" Load: 寫入 SQLite 資料庫...")

# 建立一個新的資料庫檔案來放幣圈數據
conn = sqlite3.connect('crypto_history.db')
cursor = conn.cursor()

# 建立專屬的資料表
cursor.execute('''
    CREATE TABLE IF NOT EXISTS btc_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        record_time TEXT,
        symbol TEXT,
        price REAL
    )
''')

# 將剛才抓到的時間、幣種、價格寫入資料庫
cursor.execute('''
    INSERT INTO btc_prices (record_time, symbol, price)
    VALUES (?, ?, ?)
''', (current_time, symbol, btc_price))

# 儲存並關閉
conn.commit()
conn.close()

print("BTC 價格已存入 crypto_history.db")
