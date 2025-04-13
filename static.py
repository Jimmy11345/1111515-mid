import requests
import json
import csv

# Dcard miHoYo 看板 API
url = "https://www.dcard.tw/f/yzu"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    data_list = []

    for post in data:
        title = post['title']
        link = f"https://www.dcard.tw/f/yzu/p/{post['id']}"

        data_list.append({'title': title, 'url': link})

    # 儲存 JSON
    with open('dcard.json', 'w', encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)

    # 儲存 CSV
    with open('dcard.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'url'])
        writer.writeheader()
        writer.writerows(data_list)

    print(f"✅ 已成功抓取 {len(data_list)} 筆 Dcard miHoYo 文章！")

else:
    print(f"❌ 請求失敗，狀態碼：{response.status_code}")
