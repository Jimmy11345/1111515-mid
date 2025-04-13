import requests
from bs4 import BeautifulSoup
import json
import csv
from urllib.parse import urljoin  # 用來處理相對路徑

# 要爬取的網站URL
url = "https://www.ptt.cc/bbs/miHoYo/index.html"

# 用 session 保持 Cookie（處理 over18）
#session = requests.Session()

# 模擬瀏覽器的 headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36',
    'Referer': 'https://www.ptt.cc/',
    'Origin': 'https://term.ptt.cc',
}

# 模擬滿18歲的確認
#session.post("https://www.ptt.cc/ask/over18", headers=headers, data={'yes': 'yes'})

# 發送請求
response = session.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    data_list = []

    # 遍歷所有文章連結
    for link in soup.find_all('a'):
        title = link.get_text(strip=True)
        href = link.get('href')

        # 將相對路徑轉換為絕對路徑
        full_url = urljoin(url, href)

        # 儲存標題和完整網址
        data_list.append({
            'title': title,
            'url': full_url
        })

    # 儲存為 JSON 格式
    with open('static.json', 'w', encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)

    # 儲存為 CSV 格式
    with open('static.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'url'])
        writer.writeheader()
        writer.writerows(data_list)

    print("爬蟲完成，資料已經儲存為 JSON 和 CSV！")

else:
    print(f"網頁請求失敗，狀態碼：{response.status_code}")
