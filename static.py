import requests
from bs4 import BeautifulSoup
import json
import csv

url = "https://www.phttps://www.ptt.cc/bbs/index.html"

headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    data_list = []

    # 專門抓標題區塊
    for article in soup.find_all('div', class_='r-ent'):
        title_tag = article.find('div', class_='title').find('a')
        if title_tag:
            title = title_tag.text.strip()
            href = "https://www.ptt.cc" + title_tag['href']
            data_list.append({
                'title': title,
                'url': href
            })

    # 寫入 JSON
    with open('static.json', 'w', encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)

    # 寫入 CSV
    with open('static.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'url'])
        writer.writeheader()
        writer.writerows(data_list)

    print("✅ 爬蟲完成，資料已經儲存為 static.json 和 static.csv！")
else:
    print(f"❌ 網頁請求失敗，狀態碼：{response.status_code}")
