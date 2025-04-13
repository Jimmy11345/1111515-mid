import requests
import csv
import os

# 發送 GET 請求，從高雄市開放資料平台獲取資料
web = requests.get('https://data.kcg.gov.tw/dataset/6f29f6f4-2549-4473-aa90-bf60d10895dc/resource/30dfc2cf-17b5-4a40-8bb7-c511ea166bd3/download/lightrailtraffic.json')

# 如果請求成功
if web.status_code == 200:
    data = web.json()  # 解析 JSON 資料
    
    if isinstance(data, list):
        fieldnames = data[0].keys()  # 依據第一筆資料的 key 作為欄位名稱

        os.makedirs('output', exist_ok=True)
        csv_filename = 'output/api.csv'

        with open(csv_filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        print("✅ 資料已成功儲存為 CSV 檔案！")
    else:
        print("❌ 無法處理該 JSON 格式，資料不是列表型別。")
else:
    print(f"❌ 資料請求失敗，狀態碼：{web.status_code}")
