from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import json
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
import csv
from threading import Thread, Event
from time import sleep

import os
from dotenv import load_dotenv
load_dotenv()
DEFAULT_PROFILE = os.getenv('DEFAULT_PROFILE')
SEARCH_LINK = os.getenv('SEARCH_LINK')

class Bot(Thread):
    def __init__(self):
        Thread.__init__(self)
        self._stop = Event()
        self.setdriver()
    def stop(self): 
        self._stop.set() 
    def stopped(self): 
        return self._stop.isSet() 
    def setdriver(self):
        try:
            print('setting chrome driver')
            options = webdriver.FirefoxOptions()
            options.add_argument("--start-maximized")
            # options.headless = True
            profile = webdriver.FirefoxProfile(DEFAULT_PROFILE)
            self.driver = webdriver.Firefox(executable_path="geckodriver.exe", options=options, firefox_profile=profile)
            self.driver.get(SEARCH_LINK)
        except Exception as e:
            print(e)
    # def _
    def run(self):
        print('Checking page')

        


def main():
    my_bot = Bot()
    my_bot.start()


if __name__ == '__main__':
    main()