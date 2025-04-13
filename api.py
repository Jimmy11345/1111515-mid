import requests
from bs4 import BeautifulSoup
import csv

# 創建 session 保持連線
session = requests.Session()

# 設定 headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Origin': 'https://term.ptt.cc',
    'Referer': 'https://www.ptt.cc/bbs/miHoYo/index.html'
}

# 發送 GET 請求
response = session.get("https://www.ptt.cc/bbs/miHoYo/index.html", headers=headers)

# 如果請求失敗，印出錯誤訊息
if response.status_code != 200:
    print(f"❌ 請求失敗，狀態碼：{response.status_code}")
    
    # 印出伺服器回傳的詳細錯誤訊息
    print("===== Response Text =====")
    print(response.text)  # 這會印出錯誤頁面或詳細訊息
    
    # 如果有需要，還可以印出 headers
    print("===== Response Headers =====")
    print(response.headers)
    
    exit()  # 結束程式

# 成功的話解析頁面
soup = BeautifulSoup(response.text, 'html.parser')
data_list = []

articles = soup.find_all('div', class_='r-ent')
for article in articles:
    title_tag = article.find('div', class_='title').find('a')
    if title_tag:
        title = title_tag.text.strip()
        link = "https://www.ptt.cc" + title_tag['href']
        data_list.append({'title': title, 'url': link})

# 儲存結果到 CSV
with open('api.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=['title', 'url'])
    writer.writeheader()
    writer.writerows(data_list)

print("✅ 爬蟲成功，資料已儲存在 api.csv")
