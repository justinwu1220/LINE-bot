from transitions.extensions import GraphMachine

from utils import send_text_message, send_flex_message
from selenium import webdriver
import time
import os


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_getting_search(self, event):
        text = event.message.text
        return text.lower() == "search"

    def on_enter_ready(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "Please enter the name of game")

    def on_enter_search(self, event):
        url = "https://gg.deals/deals/?store=4&type=1,2,3,7,9,10,11"
        search_key = event.message.text

        options = webdriver.ChromeOptions()
        options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        options.add_argument("--headless")
        options.add_argument('--disable-gpu')
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("prefs", {"profile.password_manager_enabled": False, "credentials_enable_service": False})

        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)
        driver.get(url)
        
        element = driver.find_element_by_id("search-by-main-name")
        element.send_keys(search_key)
        time.sleep(1)
        game_list = driver.find_elements_by_class_name("game-info-wrapper")
        num_of_list = len(game_list)
        list_arr = []
        str_arr = str()
        if num_of_list == 0:
            str_arr = "Not found"

        else:
            for i in range(num_of_list):
                game = game_list[i]
                name = game.find_element_by_class_name("game-info-title-wrapper").get_attribute('textContent')
                old_price = game.find_element_by_class_name("price-old").get_attribute('textContent')
                new_price = game.find_element_by_class_name("game-price-new").get_attribute('textContent')
                discount = game.find_element_by_class_name("badge").get_attribute('textContent')
                li =[name, old_price, new_price, discount]
                list_arr.append(li)
                #str_arr += "\n"+name+"\ncurrent price: "+new_price+"\toriginal price: "+old_price+"\tdiscount: "+discount+"\n"
            
        driver.close()
        #self.finished(event, str_arr)   
        self.finished(event, list_arr) 

    def on_enter_result(self, event, str_arr):
        reply_token = event.reply_token
        send_text_message(reply_token, str_arr)
        self.go_idle()