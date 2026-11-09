import json
import urllib.request
import os

# 臺灣證券交易所 OpenAPI
url = "https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL"

# 向 API 取得 JSON 資料
with urllib.request.urlopen(url, timeout=20) as response:
    data = json.load(response)

# 建立 data 資料夾
os.makedirs("data", exist_ok=True)

# 保存 API 原始 JSON 資料
with open("data/twse_stock_day_all_raw.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=2)

print("API 資料儲存成功！")

# 指定要查詢的 ETF
etf_codes = ["0050", "0056", "00878", "00919", "00929"]

# 記錄找到的 ETF
found_codes = []

# 找出指定 ETF
for etf in data:
    if etf.get("Code") in etf_codes:
        print("--------------------")
        print("ETF 代號：", etf["Code"])
        print("ETF 名稱：", etf["Name"])
        print("資料日期：", etf.get("Date", "API 未提供"))
        print("收盤價：", etf["ClosingPrice"])
        print("成交股數：", etf["TradeVolume"])

        found_codes.append(etf["Code"])

# 顯示查詢結果
print("--------------------")
print("找到 ETF 數量：", len(found_codes))

# 顯示沒有找到的 ETF
for code in etf_codes:
    if code not in found_codes:
        print("找不到 ETF：", code)