import requests
from bs4 import BeautifulSoup
import json
import csv

# 要爬取的網站URL
url = "https://www.ptt.cc/bbs/miHoYo/index.html"

# 模擬瀏覽器的 headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36'
}

# PTT年齡驗證cookie
cookies = {'over18': '1'}

# 發送HTTP請求，帶上headers與cookies
response = requests.get(url, headers=headers, cookies=cookies)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    data_list = []

    # 找到所有 a 標籤
    for link in soup.find_all('a'):
        title = link.get_text(strip=True)
        href = link.get('href')

        data_list.append({
            'title': title,
            'url': href
        })

    # 輸出為 JSON 檔案
    with open('static.json', 'w', encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)

    # 輸出為 CSV 檔案
    with open('static.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'url'])
        writer.writeheader()
        writer.writerows(data_list)

    print("爬蟲完成，資料已經儲存為 JSON 和 CSV！")

else:
    print(f"網頁請求失敗，狀態碼：{response.status_code}")
