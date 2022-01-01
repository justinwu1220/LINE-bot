from transitions.extensions import GraphMachine
import requests
import itertools
from bs4 import BeautifulSoup
from utils import send_text_message, send_flex_message
import time
import os
global headers
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        }

class TocMachine(GraphMachine):
    

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_getting_nothing(self, event):
        text = event.message.text
        return text.lower() != "本季新番" and text.lower() != "搜尋" and text.lower() != "今日更新" and text.lower() != "熱門"

    def is_getting_new(self, event):
        text = event.message.text
        return text.lower() == "本季新番"

    def is_getting_search(self, event):
        text = event.message.text
        return text.lower() == "搜尋"

    def is_getting_today(self, event):
        text = event.message.text
        return text.lower() == "今日更新"    

    def is_getting_hot(self, event):
        text = event.message.text
        return text.lower() == "熱門" 

    def on_enter_command_failed(self, event):
        text = "歡迎來到動畫瘋LINE-BOT\n\n輸入關鍵字啟動查詢功能\n\n--熱門\n--今日更新\n--本季新番\n--搜尋"
        reply_token = event.reply_token
        send_text_message(reply_token, text)
        self.finished()

    def on_exit_idle(self, event):
        text = "歡迎來到動畫瘋LINE-BOT\n\n輸入關鍵字啟動查詢功能\n\n--熱門\n--今日更新\n--本季新番\n--搜尋"
        reply_token = event.reply_token
        send_text_message(reply_token, text)

    def on_enter_today_anim(self, event):
        r = requests.get('https://ani.gamer.com.tw/', headers=headers)
        if r.status_code == 200:
            print(f'請求成功：{r.status_code}')
            soup = BeautifulSoup(r.text, 'html.parser')
            newanime_item = soup.select_one('.timeline-ver > .newanime-block')
            anime_items = newanime_item.select('.new-count-1')
            info_all = "今日更新\n\n"
            for anime_item in anime_items:
                anime_name = anime_item.select_one('.anime-name > p').text.strip() # 動畫名稱
                anime_watch_number = anime_item.select_one('.anime-watch-number > p').text.strip() # 觀看人數
                anime_episode = anime_item.select_one('.anime-episode').text.strip() # 動畫集數
                href = anime_item.select_one('a.anime-card-block').get('href')
                anime_href = 'https://ani.gamer.com.tw/'+href # 觀看連結

                anime_date = anime_item.select_one('.anime-date-info').contents[-1].string.strip()
                anime_time = anime_item.select_one('.anime-hours').text.strip()
                anime_img = anime_item.select_one('img.lazyload').get('src')
                #print(anime_img)  # 動畫縮圖
                #print('----------')
                info = anime_date+" "+anime_time+"\n\n"+anime_name+"\n"+anime_href+"\n\n"
                info_all+=info
        else:
            print(f'請求失敗：{r.status_code}')
        
        reply_token = event.reply_token
        send_text_message(reply_token, info_all)
        self.finished()

    def on_enter_hot_anim(self, event):
        r = requests.get('https://ani.gamer.com.tw/', headers=headers)
        if r.status_code == 200:
            print(f'請求成功：{r.status_code}')
            soup = BeautifulSoup(r.text, 'html.parser')
            newanime_item = soup.select_one('.normal-ver > .newanime-block')
            anime_items = newanime_item.select('.newanime-date-area:not(.premium-block)')
            info_all = "熱門\n\n"
            index = 1
            for anime_item in itertools.islice(anime_items, 0, 3):
                anime_name = anime_item.select_one('.anime-name > p').text.strip() # 動畫名稱
                anime_watch_number = anime_item.select_one('.anime-watch-number > p').text.strip() # 觀看人數
                anime_episode = anime_item.select_one('.anime-episode').text.strip() # 動畫集數
                href = anime_item.select_one('a.anime-card-block').get('href')
                anime_href = 'https://ani.gamer.com.tw/'+href # 觀看連結
                anime_img = anime_item.select_one('img.lazyload').get('src')
                #print(anime_img)  # 動畫縮圖
                #print('----------')
                info = "TOP"+str(index)+"\n\n"+anime_name+"\n"+anime_watch_number+"次觀看\n"+anime_href+"\n\n"
                info_all+=info
                index += 1

        else:
            print(f'請求失敗：{r.status_code}')
        
        reply_token = event.reply_token
        send_text_message(reply_token, info_all)
        self.finished()

    def on_enter_new_anim(self, event):
        r = requests.get('https://ani.gamer.com.tw/', headers=headers)
        if r.status_code == 200:
            print(f'請求成功：{r.status_code}')
            soup = BeautifulSoup(r.text, 'html.parser')
            newanime_item = soup.select_one('.timeline-ver > .newanime-block')
            anime_items = newanime_item.select('.newanime-date-area:not(.premium-block)')
            info_all = "本季新番\n\n"
            for anime_item in anime_items:
                anime_name = anime_item.select_one('.anime-name > p').text.strip() # 動畫名稱
                anime_watch_number = anime_item.select_one('.anime-watch-number > p').text.strip() # 觀看人數
                anime_episode = anime_item.select_one('.anime-episode').text.strip() # 動畫集數
                href = anime_item.select_one('a.anime-card-block').get('href')
                anime_href = 'https://ani.gamer.com.tw/'+href # 觀看連結
                anime_img = anime_item.select_one('img.lazyload').get('src')
                #print(anime_img)  # 動畫縮圖
                #print('----------')
                info = anime_name+"\n"+anime_episode+"\n"+anime_href+"\n\n"
                info_all+=info
        else:
            print(f'請求失敗：{r.status_code}')
        
        reply_token = event.reply_token
        send_text_message(reply_token, info_all)
        self.finished()

    def on_enter_search_anim(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "輸入搜尋名稱...")

    def on_enter_searching(self, event):
        search_input = event.message.text
        url = "https://ani.gamer.com.tw/search.php?kw="+search_input
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            print(f'請求成功：{r.status_code}')
            info_all = "搜尋結果\n\n"
            soup = BeautifulSoup(r.text, 'html.parser')
            newanime_item = soup.select_one('.old_list > .animate-theme-list')
            list_block = newanime_item.select_one('.theme-list-block')
            anime_items = list_block.select('a.theme-list-main')
            if anime_items == []:
                info_all = "查無結果"
            else:
                for anime_item in anime_items:
                    anime_name = anime_item.select_one('.theme-name').text.strip() # 動畫名稱
                    anime_watch_number = anime_item.select_one('.show-view-number > p').text.strip() # 觀看人數
                    anime_episode = anime_item.select_one('.theme-number').text.strip() # 動畫集數
                    href = anime_item.get('href')
                    anime_href = 'https://ani.gamer.com.tw/'+href # 觀看連結

                    anime_year = anime_item.select_one('.theme-time').text.strip() # 動畫年分

                    anime_img = anime_item.select_one('img.lazyload').get('src')
                    #print(anime_img)  # 動畫縮圖

                    #print('----------')
                    info_all += anime_name+"\n"+anime_episode+"\n"+anime_watch_number+"次觀看\n"+anime_href+"\n"+anime_year+"\n\n"
        else:
            print(f'請求失敗：{r.status_code}')

        

        reply_token = event.reply_token
        send_text_message(reply_token, info_all)
        self.finished()