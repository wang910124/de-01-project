import json
import urllib.request
import pymysql
import getpass

from datetime import date
from decimal import Decimal
from pathlib import Path

# MySQL 設定
DB_HOST = "172.18.224.1"
DB_USER = "etf_user"
DB_NAME = "etf_analysis"

# 第一批 ETF
ETF_CODES = {"0050", "0056", "006208", "00878", "00919"}

# TWSE OpenAPI
URL = "https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL"

# 取得 API 資料
with urllib.request.urlopen(URL, timeout=20) as response:
    data = json.load(response)

# 保留原始資料
data_dir = Path(__file__).resolve().parent / "data"
data_dir.mkdir(exist_ok=True)

raw_date = str(data[0]["Date"])
file_path = data_dir / f"twse_raw_{raw_date}.json"

with open(file_path, "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=2)

print("原始 JSON 儲存成功！")

# 整理 ETF 資料
records = []

for item in data:
    code = item.get("Code")

    if code not in ETF_CODES:
        continue

    try:
        raw_date = str(item["Date"]).strip()
        digits = raw_date.replace("/", "").replace("-", "")

        if len(digits) == 7:
            year = int(digits[:3]) + 1911
            month = int(digits[3:5])
            day = int(digits[5:7])
        elif len(digits) == 8:
            year = int(digits[:4])
            month = int(digits[4:6])
            day = int(digits[6:8])
        else:
            raise ValueError("日期格式錯誤")

        trade_date = date(year, month, day)

        close_price = Decimal(
            str(item["ClosingPrice"]).replace(",", "").strip()
        )

        trade_volume = int(
            str(item["TradeVolume"]).replace(",", "").strip()
        )

        if close_price <= 0 or trade_volume < 0:
            raise ValueError("行情數值不合理")

        records.append((
            code,
            trade_date,
            close_price,
            trade_volume
        ))

    except (ValueError, KeyError, ArithmeticError) as error:
        print(f"略過 {code}：{error}")

if not records:
    raise RuntimeError("找不到可匯入的 ETF 行情")

# 登入 MySQL
password = getpass.getpass("請輸入 MySQL 密碼：")

connection = pymysql.connect(
    host=DB_HOST,
    port=3306,
    user=DB_USER,
    password=password,
    database=DB_NAME,
    charset="utf8mb4"
)

try:
    sql = """
    INSERT INTO etf_daily_prices
        (etf_code, trade_date, close_price, trade_volume)
    VALUES (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        close_price = VALUES(close_price),
        trade_volume = VALUES(trade_volume)
    """

    with connection.cursor() as cursor:
        cursor.executemany(sql, records)

    connection.commit()
    print("MySQL 資料寫入成功！")
    print(f"本次處理 {len(records)} 筆 ETF 行情")

except Exception:
    connection.rollback()
    raise

finally:
    connection.close()