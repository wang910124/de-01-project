import pymysql
import getpass

# 安全輸入 MySQL 密碼
password = getpass.getpass("請輸入 MySQL 密碼：")

try:
    # 連接 Windows 上的 MySQL
    connection = pymysql.connect(
        host="172.18.224.1",
        port=3306,
        user="etf_user",
        password=password,
        database="etf_analysis",
        charset="utf8mb4",
        connect_timeout=5
    )

    print("MySQL 連線成功！")

    # 確認目前連接的資料庫
    with connection.cursor() as cursor:
        cursor.execute("SELECT DATABASE()")
        print("目前資料庫：", cursor.fetchone()[0])

    connection.close()

except pymysql.MySQLError as error:
    print("MySQL 連線失敗：", error)