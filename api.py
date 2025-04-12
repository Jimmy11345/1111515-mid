import requests
from bs4 import BeautifulSoup
import csv

# PTT miHoYo 板網址
url = "https://www.youtube.com/"

# 模擬瀏覽器 headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36'
}

# PTT需要同意年滿18歲
cookies = {'over18': '1'}

# 發送請求
response = requests.get(url, headers=headers, cookies=cookies)

# 確認是否成功
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    data_list = []

    # 找到所有文章標題區塊
    articles = soup.find_all('div', class_='r-ent')

    for article in articles:
        title_tag = article.find('div', class_='title').find('a')
        if title_tag:
            title = title_tag.text.strip()           # 標題文字
            link = "https://www.ptt.cc" + title_tag['href']  # 完整文章連結

            data_list.append({'title': title, 'url': link})

    # 將結果寫入CSV檔案
    with open('api.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'url'])
        writer.writeheader()
        writer.writerows(data_list)

    print("已完成爬取，結果儲存在：api.csv！")

else:
    print(f"請求失敗，狀態碼：{response.status_code}")
