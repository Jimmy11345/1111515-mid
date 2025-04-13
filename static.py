import requests
from bs4 import BeautifulSoup
import json
import csv
from urllib.parse import urljoin

url = "https://www.ptt.cc/bbs/miHoYo/index.html"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    data_list = []

    for link in soup.find_all('a'):
        title = link.get_text(strip=True)
        href = link.get('href')
        if href:
            full_url = urljoin(url, href)
            data_list.append({
                'title': title,
                'url': full_url
            })

    with open('static.json', 'w', encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)

    with open('static.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'url'])
        writer.writeheader()
        writer.writerows(data_list)

    print("✅ 爬蟲完成，資料已儲存！")

else:
    print(f"❌ 網頁請求失敗，狀態碼：{response.status_code}")
