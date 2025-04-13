import cloudscraper

# 建立 CloudScraper 物件
scraper = cloudscraper.create_scraper()

# 目標 URL
url = 'https://www.ptt.cc/bbs/miHoYo/index.html'

# 發送請求並處理
response = scraper.get(url)

# 打印返回的頁面內容
print(response.text)
