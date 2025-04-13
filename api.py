import requests
from bs4 import BeautifulSoup
import csv

session = requests.Session()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Origin': 'https://term.ptt.cc',
    'Referer': 'https://www.ptt.cc/bbs/miHoYo/index.html',
}

# 加入 cookies 確保突破成人內容頁面
cookies = {
    'over18': '1',  # 避免成人頁面彈出
}

# 嘗試進行請求
response = session.get("https://www.ptt.cc/bbs/miHoYo/index.html", headers=headers, cookies=cookies)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    data_list = []
    articles = soup.find_all('div', class_='r-ent')

    for article in articles:
        title_tag = article.find('div', class_='title').find('a')
        if title_tag:
            title = title_tag.text.strip()
            link = "https://www.ptt.cc" + title_tag['href']
            data_list.append({'title': title, 'url': link})

    # 儲存結果到 CSV 檔案
    with open('api.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'url'])
        writer.writeheader()
        writer.writerows(data_list)

    print("✅ 爬蟲成功，資料已儲存在 api.csv")
else:
    print(f"❌ 失敗，狀態碼：{response.status_code}")
