import cloudscraper
from bs4 import BeautifulSoup
import csv

# 建立 CloudScraper 物件
scraper = cloudscraper.create_scraper()

# 目標 URL
url = 'https://www.ptt.cc/bbs/miHoYo/index.html'

# 發送請求並處理
response = scraper.get(url)

# 設定正確的編碼方式
response.encoding = 'utf-8'  # 或者你可以嘗試 'big5' 這是 PTT 頁面可能的編碼格式

# 解析頁面
soup = BeautifulSoup(response.text, 'html.parser')

# 假設我們要抓取所有文章的標題
titles = soup.find_all('div', class_='title')

# 打開 CSV 檔案，準備寫入數據
with open('api.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # 寫入表頭
    writer.writerow(['Title'])

    # 寫入每個標題
    for title in titles:
        writer.writerow([title.text.strip()])

print("Data has been written to api.csv.")
