import requests
from bs4 import BeautifulSoup
import json
import csv
import os

url = "https://www.dcard.tw/f/yzu"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    data_list = []

    articles = soup.find_all('a', class_='tgn9uw-0')
    for article in articles[:10]:  # 限前10篇
        title = article.text.strip()
        href = article['href']
        full_url = f"https://www.dcard.tw{href}"
        data_list.append({'title': title, 'url': full_url})

    os.makedirs('output', exist_ok=True)

    with open('output/dcard.json', 'w', encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)

    with open('output/dcard.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'url'])
        writer.writeheader()
        writer.writerows(data_list)

    print("✅ 爬蟲完成，已儲存到 output/ 資料夾！")
else:
    print(f"❌ 請求失敗，狀態碼：{response.status_code}")
    exit(1)
