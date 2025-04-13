import requests
from bs4 import BeautifulSoup
import csv
import datetime

session = requests.Session()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Referer': 'https://www.ptt.cc/',
    'Origin': 'https://term.ptt.cc',  # 加這個就能成功
}

# 送出同意滿18歲的請求
#session.post("https://www.ptt.cc/ask/over18", headers=headers, data={'yes': 'yes'})

# 指定要爬的 PTT 看板
url = "https://www.ptt.cc/bbs/miHoYo/index.html"
response = session.get(url, headers=headers)

# 若非 200，直接結束（不用 else）
if response.status_code != 200:
    print(f"❌ 請求失敗，狀態碼：{response.status_code}")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f'response_debug_{timestamp}.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    exit()  # 提早結束

# 以下是成功處理流程
soup = BeautifulSoup(response.text, 'html.parser')
data_list = []

articles = soup.find_all('div', class_='r-ent')
if not articles:
    print("⚠️ 沒有找到文章，可能是網址不正確")

for article in articles:
    title_tag = article.find('div', class_='title').find('a')
    if title_tag:
        title = title_tag.text.strip()
        link = "https://www.ptt.cc" + title_tag['href']
        data_list.append({'title': title, 'url': link})

with open('api.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=['title', 'url'])
    writer.writeheader()
    writer.writerows(data_list)

print("✅ 已完成爬取，資料已儲存到 api.csv")
