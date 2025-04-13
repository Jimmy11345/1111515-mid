# static.py
import requests
from bs4 import BeautifulSoup
import json
import csv
import os

# 巴哈姆特指定討論版網址
url = "https://forum.gamer.com.tw/B.php?bsn=36730"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

response = requests.get(url, headers=headers)

# 確認請求是否成功
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    data_list = []

    # 找到文章標題區塊，巴哈通常標題在 class="b-list__main__title"
    for link in soup.select('.b-list__main__title'):
        title = link.get_text(strip=True)
        href = link.get('href')

        if href and href.startswith('C.php?bsn=36730&snA='):
            full_url = "https://forum.gamer.com.tw/" + href
            data_list.append({
                'title': title,
                'url': full_url
            })

    # 儲存為 JSON 格式
    os.makedirs('output', exist_ok=True)
    json_filename = 'output/static.json'
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)

    # 儲存為 CSV 格式
    csv_filename = 'output/static.csv'
    with open(csv_filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'url'])
        writer.writeheader()
        writer.writerows(data_list)

    print("爬蟲完成，資料已經儲存為 JSON 和 CSV！")

else:
    print(f"網頁請求失敗，狀態碼：{response.status_code}")
