import os
import requests
from bs4 import BeautifulSoup

url = "https://www.ptt.cc/bbs/miHoYo/index.html"
dn = "ptt/" + url.split("/")[-1]  # 資料夾檔名
if not os.path.exists(dn):  # 如果沒有這個資料夾就創建一個
    os.makedirs(dn)
    
response = requests.get(url, cookies={"over18":"1"})
html = BeautifulSoup(response.text, "html.parser")

allows = ["jpg", "jpeg", "png", "gif"]  # 被允許的副檔名
links = html.find_all("a")
for link in links:
    href = link["href"]  # 取得網址
    sub = href.split(".")[-1]
    if sub.lower() in allows:  # 讓所有字母變成小寫
        print("download:", href)
        fp = dn + "/" + href.split("/")[-1]  # 自己做檔名跟副檔名
        f = open(fp, "wb")
        f.write(response.raw.read())  # 把裡面的內容讀出來寫入新檔案
        f.close()
    print("-" * 30)
