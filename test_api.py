import json
import urllib.request

# 臺灣證券交易所 OpenAPI
url = "https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL"

# 向 API 取得 JSON 資料
with urllib.request.urlopen(url, timeout=20) as response:
    data = json.load(response)
# 保存 API 原始 JSON 資料
with open("data/twse_stock_day_all_raw.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=2)

print("API 資料儲存成功！")
# 找出 ETF 0050
for etf in data:
    if etf.get("Code") == "0050":
        print("ETF 代號：", etf["Code"])
        print("ETF 名稱：", etf["Name"])
        print("資料日期：", etf["Date"])
        print("收盤價：", etf["ClosingPrice"])
        print("成交股數：", etf["TradeVolume"])
        break
else:
    print("這次 API 回傳資料中找不到 0050")