from transitions.extensions import GraphMachine

from utils import send_text_message, send_flex_message
from selenium import webdriver
import time
import os


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_getting_new(self, event):
        text = event.message.text
        return text.lower() == "new"

    def is_getting_search(self, event):
        text = event.message.text
        return text.lower() == "search"

    def on_enter_new_anim(self, event):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        }
        # 對"巴哈姆特動畫瘋"送出請求
        r = requests.get('https://ani.gamer.com.tw/', headers=headers)
        if r.status_code == 200:
            info_arr = []
            print(f'請求成功：{r.status_code}')

            # 藉由 BeautifulSoup 套件將網頁原始碼使用 `html.parser` 解析器來解析
            soup = BeautifulSoup(r.text, 'html.parser')
            # 取得各個動畫元素區塊
            newanime_item = soup.select_one('.timeline-ver > .newanime-block')
            anime_items = newanime_item.select('.newanime-date-area:not(.premium-block)')

            # 依序針對每個動畫區塊擷取資料
            for anime_item in anime_items:
                anime_name = anime_item.select_one('.anime-name > p').text.strip()
                
                #print(anime_name)  # 動畫名稱
                anime_watch_number = anime_item.select_one('.anime-watch-number > p').text.strip()
                print(anime_watch_number)  # 觀看人數
                anime_episode = anime_item.select_one('.anime-episode').text.strip()
                print(anime_episode)  # 動畫集數
                anime_href = anime_item.select_one('a.anime-card-block').get('href')
                print('https://ani.gamer.com.tw/'+anime_href)  # 觀看連結

                # contents：將 tag 的子節點以列表的方式輸出
                anime_date = anime_item.select_one('.anime-date-info').contents[-1].string.strip()
                anime_time = anime_item.select_one('.anime-hours').text.strip()
                print(anime_date, anime_time)  # 日期與時間
                anime_img = anime_item.select_one('img.lazyload').get('src')
                print(anime_img)  # 動畫縮圖
                print('----------')
                info = [anime_name, anime_href, anime_episode]
            info_arr.append(info)
        else:
            print(f'請求失敗：{r.status_code}')
        
        reply_token = event.reply_token
        send_text_message(reply_token, info_arr)
