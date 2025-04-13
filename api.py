import requests
from bs4 import BeautifulSoup
import csv

# 用 session 保持 cookie
session = requests.Session()

# headers 模擬瀏覽器
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36',
    'Referer': 'https://www.google.com/',
    'Accept-Language': 'zh-TW,zh;q=0.9'
}

# 模擬按下「我已滿18歲」
over18_url = "https://www.ptt.cc/ask/over18"
session.post(over18_url, headers=headers, data={'yes': 'yes'})

# 然後才進入版面
url = "https://www.ptt.cc/bbs/index.html"
response = session.get(url, headers=headers)

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

    with open('api.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'url'])
        writer.writeheader()
        writer.writerows(data_list)

    print("已完成爬取，結果儲存在：api.csv！")
else:
    print(f"請求失敗，狀態碼：{response.status_code}")
    with open('response_debug.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
