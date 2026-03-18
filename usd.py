import requests
import csv
import os
from datetime import datetime

# 1.提取-抓取原始data
print('開始執行 提取:抓取最新匯率') 
url="https://api.exchangerate-api.com/v4/latest/USD"
response=requests.get(url)
raw_data=response.json()

#2.轉換-整理過濾需要的格式
print('開始執行:整理台幣匯率與時間')
twd_rate= raw_data['rates']['TWD']
current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
clean_data = [current_time, "USD/TWD", twd_rate]
print(f"   -> 整理完畢！目前匯率：{twd_rate}")

# Step 3: Load (載入) - 將整理好的資料存起來
# ==========================================
print("💾 開始執行 Load: 寫入 CSV 檔案...")
file_name = "usd_history.csv"
file_exists = os.path.isfile(file_name)

with open(file_name, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    if not file_exists:
        writer.writerow(["紀錄時間", "貨幣配對", "匯率"])
    writer.writerow(clean_data)

print(f"✅ ETL 流程執行成功！資料已存入 {file_name}")