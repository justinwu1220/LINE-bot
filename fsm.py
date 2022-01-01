from transitions.extensions import GraphMachine
import requests
from bs4 import BeautifulSoup
from utils import send_text_message, send_flex_message
#from selenium import webdriver
import time
import os
global headers
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        }

class TocMachine(GraphMachine):
    

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_getting_new(self, event):
        text = event.message.text
        return text.lower() == "new"

    def is_getting_search(self, event):
        text = event.message.text
        return text.lower() == "search"

    def is_getting_today(self, event):
        text = event.message.text
        return text.lower() == "today"    

    def on_exit_idle(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "awaked")

    def on_enter_today_anim(self, event):
        r = requests.get('https://ani.gamer.com.tw/', headers=headers)
        if r.status_code == 200:
            print(f'請求成功：{r.status_code}')

            # 藉由 BeautifulSoup 套件將網頁原始碼使用 `html.parser` 解析器來解析
            soup = BeautifulSoup(r.text, 'html.parser')
            # 取得各個動畫元素區塊
            newanime_item = soup.select_one('.timeline-ver > .newanime-block')
            anime_items = newanime_item.select('.new-count-1')
            info_all = str()
            # 依序針對每個動畫區塊擷取資料
            for anime_item in anime_items:
                anime_name = anime_item.select_one('.anime-name > p').text.strip()
                
                #print(anime_name)  # 動畫名稱
                anime_watch_number = anime_item.select_one('.anime-watch-number > p').text.strip()
                #print(anime_watch_number)  # 觀看人數
                anime_episode = anime_item.select_one('.anime-episode').text.strip()
                #print(anime_episode)  # 動畫集數
                href = anime_item.select_one('a.anime-card-block').get('href')
                anime_href = 'https://ani.gamer.com.tw/'+href
                #print('https://ani.gamer.com.tw/'+anime_href)  # 觀看連結

                # contents：將 tag 的子節點以列表的方式輸出
                #anime_date = anime_item.select_one('.anime-date-info').contents[-1].string.strip()
                #anime_time = anime_item.select_one('.anime-hours').text.strip()
                #print(anime_date, anime_time)  # 日期與時間
                anime_img = anime_item.select_one('img.lazyload').get('src')
                #print(anime_img)  # 動畫縮圖
                #print('----------')
                info = anime_name+"\n"+anime_href+"\n\n"
                info_all+=info
        else:
            print(f'請求失敗：{r.status_code}')
        
        reply_token = event.reply_token
        send_text_message(reply_token, info_all)
        self.finished()

    def on_enter_new_anim(self, event):
        # 對"巴哈姆特動畫瘋"送出請求
        r = requests.get('https://ani.gamer.com.tw/', headers=headers)
        if r.status_code == 200:
            print(f'請求成功：{r.status_code}')

            # 藉由 BeautifulSoup 套件將網頁原始碼使用 `html.parser` 解析器來解析
            soup = BeautifulSoup(r.text, 'html.parser')
            # 取得各個動畫元素區塊
            newanime_item = soup.select_one('.normal-ver > .newanime-block')
            anime_items = newanime_item.select('.newanime-date-area:not(.premium-block)')
            info_all = str()
            # 依序針對每個動畫區塊擷取資料
            for anime_item in anime_items:
                anime_name = anime_item.select_one('.anime-name > p').text.strip()
                
                #print(anime_name)  # 動畫名稱
                anime_watch_number = anime_item.select_one('.anime-watch-number > p').text.strip()
                #print(anime_watch_number)  # 觀看人數
                anime_episode = anime_item.select_one('.anime-episode').text.strip()
                #print(anime_episode)  # 動畫集數
                href = anime_item.select_one('a.anime-card-block').get('href')
                anime_href = 'https://ani.gamer.com.tw/'+href
                #print('https://ani.gamer.com.tw/'+anime_href)  # 觀看連結

                # contents：將 tag 的子節點以列表的方式輸出
                #anime_date = anime_item.select_one('.anime-date-info').contents[-1].string.strip()
                #anime_time = anime_item.select_one('.anime-hours').text.strip()
                #print(anime_date, anime_time)  # 日期與時間
                anime_img = anime_item.select_one('img.lazyload').get('src')
                #print(anime_img)  # 動畫縮圖
                #print('----------')
                info = anime_name+"\n"+anime_href+"\n\n"
                info_all+=info
        else:
            print(f'請求失敗：{r.status_code}')
        
        reply_token = event.reply_token
        send_text_message(reply_token, info_all)
        self.finished()

    def on_enter_search_anim(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "enter animate name")

    def on_enter_searching(self, event):
        search_input = event.message.text
        url = "https://ani.gamer.com.tw/search.php?kw="+search_input
        # 對"巴哈姆特動畫瘋"送出請求
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            print(f'請求成功：{r.status_code}')
            info_all = str()
            # 藉由 BeautifulSoup 套件將網頁原始碼使用 `html.parser` 解析器來解析
            soup = BeautifulSoup(r.text, 'html.parser')
            # 取得各個動畫元素區塊
            newanime_item = soup.select_one('.old_list > .animate-theme-list')
            list_block = newanime_item.select_one('.theme-list-block')
            anime_items = list_block.select('a.theme-list-main')
            if anime_items == []:
                info_all = "not found"
                #print("empty")
            else:
                # 依序針對每個動畫區塊擷取資料
                for anime_item in anime_items:
                    anime_name = anime_item.select_one('.theme-name').text.strip()
                    #print(anime_name)  # 動畫名稱
                    anime_watch_number = anime_item.select_one('.show-view-number > p').text.strip()
                    #print(anime_watch_number)  # 觀看人數
                    anime_episode = anime_item.select_one('.theme-number').text.strip()
                    #print(anime_episode)  # 動畫集數
                    href = anime_item.get('href')
                    anime_href = 'https://ani.gamer.com.tw/'+href
                    #print('https://ani.gamer.com.tw/'+anime_href)  # 觀看連結

                    anime_year = anime_item.select_one('.theme-time').text.strip()
                    #print(anime_year)  # 動畫年分

                    anime_img = anime_item.select_one('img.lazyload').get('src')
                    #print(anime_img)  # 動畫縮圖

                    #print('----------')
                    info_all += anime_name+"\n"+anime_href+"\n"+anime_year+"\n\n"
        else:
            print(f'請求失敗：{r.status_code}')

        

        reply_token = event.reply_token
        send_text_message(reply_token, info_all)
        self.finished()