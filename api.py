import requests
import json
import csv

# MLB 官方打擊數據API
url = "https://statsapi.mlb.com/api/v1/stats?stats=season&group=hitting&limit=100"

# 發送GET請求
response = requests.get(url)

# 檢查回應狀態
if response.status_code == 200:
    data = response.json()

    # 取得球員數據區塊
    stats = data.get('stats', [])[0].get('splits', [])

    data_list = []

    for player in stats:
        name = player['player']['fullName']                      # 球員姓名
        at_bats = player['stat'].get('atBats', 0)                # 打數
        hits = player['stat'].get('hits', 0)                     # 安打
        avg = player['stat'].get('avg', 0)                       # 打擊率

        data_list.append({'player': name, 'at_bats': at_bats, 'hits': hits, 'avg': avg})

    # 輸出成 JSON 檔案
    with open('mlb_api.json', 'w', encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)

    # 輸出成 CSV 檔案
    with open('mlb_api.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['player', 'at_bats', 'hits', 'avg'])
        writer.writeheader()
        writer.writerows(data_list)

    print(f"✅ 已成功抓取 {len(data_list)} 筆 MLB 球員數據，儲存完成！")

else:
    print(f"❌ 請求失敗，狀態碼：{response.status_code}")
