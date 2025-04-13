import requests
import json
import csv

# MLB 官方 stats API
url = "https://statsapi.mlb.com/api/v1/stats?stats=season&group=hitting&limit=100"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()  # 取得 JSON 資料

    # 這裡可以根據API返回格式，取出選手成績
    stats = data.get('stats', [])[0].get('splits', [])

    # 準備寫入CSV
    with open('mlb_stats.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['選手', '打數', '安打', '打擊率'])  # 範例表頭

        for player in stats:
            name = player['player']['fullName']
            atBats = player['stat'].get('atBats', 0)
            hits = player['stat'].get('hits', 0)
            avg = player['stat'].get('avg', 0)

            writer.writerow([name, atBats, hits, avg])

    print(f"已成功抓取 {len(stats)} 筆 MLB 球員數據，結果已儲存到 mlb_stats.csv！")

else:
    print(f"請求失敗，狀態碼：{response.status_code}")
