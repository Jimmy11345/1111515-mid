from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv
from webdriver_manager.chrome import ChromeDriverManager
import time

# 設定瀏覽器選項
options = Options()
options.add_argument('--headless')  # 無頭模式，不開視窗
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

# 啟動瀏覽器
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 打開動畫瘋首頁
driver.get('https://ani.gamer.com.tw/')
time.sleep(3)  # 等待 JavaScript 加載完成

# 解析內容
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

# 爬取動畫資料
newanime_item = soup.select_one('.timeline-ver > .newanime-block')
anime_items = newanime_item.select('.newanime-date-area:not(.premium-block)')

data_list = []

for anime_item in anime_items:
    name_tag = anime_item.select_one('.anime-name > p')
    watch_tag = anime_item.select_one('.anime-watch-number > p')
    episode_tag = anime_item.select_one('.anime-episode')
    href_tag = anime_item.select_one('a.anime-card-block')

    anime_name = name_tag.text.strip() if name_tag else 'N/A'
    anime_watch_number = watch_tag.text.strip() if watch_tag else 'N/A'
    anime_episode = episode_tag.text.strip() if episode_tag else 'N/A'
    anime_href = 'https://ani.gamer.com.tw/' + href_tag.get('href') if href_tag else 'N/A'

    print(anime_name, anime_watch_number, anime_episode, anime_href)
    print('----------')

    data_list.append({
        'name': anime_name,
        'watch': anime_watch_number,
        'episode': anime_episode,
        'url': anime_href
    })

# 寫入 CSV
with open('ani_gamer.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'watch', 'episode', 'url'])
    writer.writeheader()
    writer.writerows(data_list)

print("✅ 成功！已寫入 ani_gamer.csv")
