import requests
from bs4 import BeautifulSoup
import csv
import datetime

# 要爬的 PTT 看板
url = "https://www.ptt.cc/bbs/miHoYo/index.html"

# 基本 headers（保持 UA 模擬正常瀏覽器）
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    'origin'='https://term.ptt.cc'
}

response = requests.get(url, headers=headers)

# 若非 200，存下 HTML 結束程式
if response.status_code != 200:
    print(f"❌ 請求失敗，狀態碼：{response.status_code}")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f'response_debug_{timestamp}.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    exit()

# 成功進入後，開始解析
soup = BeautifulSoup(response.text, 'html.parser')
data_list = []

articles = soup.find_all('div', class_='r-ent')
if not articles:
    print("⚠️ 沒有找到文章，可能是網址錯誤或格式變動")

for article in articles:
    title_tag = article.find('div', class_='title').find('a')
    if title_tag:
        title = title_tag.text.strip()
        link = "https://www.ptt.cc" + title_tag['href']
        data_list.append({'title': title, 'url': link})

# 儲存為 CSV
with open('api.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=['title', 'url'])
    writer.writeheader()
    writer.writerows(data_list)

print("✅ 已完成爬取，資料已儲存到 api.csv")
