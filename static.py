import requests
from bs4 import BeautifulSoup
import json
import csv
from urllib.parse import urljoin
import os

url = "https://www.ptt.cc/bbs/miHoYo/index.html"

# 解決 PTT 年齡驗證與防爬蟲
cookies = {'over18': '1'}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Referer': 'https://www.google.com/',
    'Accept-Language': 'zh-TW,zh;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive'
}


response = requests.get(url, cookies=cookies, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    data_list = []

    articles = soup.find_all('div', class_='r-ent')
    for article in articles:
        a_tag = article.find('a')
        if a_tag:
            title = a_tag.text.strip()
            href = a_tag['href']
            full_url = urljoin(url, href)
            data_list.append({'title': title, 'url': full_url})

    os.makedirs('output', exist_ok=True)

    with open('output/ptt.json', 'w', encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)

    with open('output/ptt.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'url'])
        writer.writeheader()
        writer.writerows(data_list)

    print("✅ 爬蟲完成，已儲存到 output/ 資料夾！")
else:
    print(f"❌ 請求失敗，狀態碼：{response.status_code}")
    exit(1)
