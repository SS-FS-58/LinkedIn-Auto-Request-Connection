from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from threading import Thread, Event
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

import os
from dotenv import load_dotenv


class Bot(Thread):
    def __init__(self):
        Thread.__init__(self)
        self._stop = Event()
        self.total_request = 100
        self.today_count = 0
        self.page = 1
        self.setdriver()
    
    def stop(self): 
        self._stop.set() 
    
    def stopped(self): 
        return self._stop.isSet()

    def init_task_info(self):
        load_dotenv()
        self.DEFAULT_PROFILE = os.getenv('DEFAULT_PROFILE')
        self.channel_link = "https://www.youtube.com/c/DanLok/about"

    def setdriver(self):
        try:
            self.init_task_info()
            options = webdriver.FirefoxOptions()
            options.add_argument("--start-maximized")
            # options.headless = True
            profile = webdriver.FirefoxProfile(self.DEFAULT_PROFILE)
            self.driver = webdriver.Firefox(executable_path="geckodriver.exe", options=options, firefox_profile=profile)
            
        except Exception as e:
            print(e)
    
    def close(self):
        try:
            self.driver.quit()
        except Exception as e:
            print(e)

    def _next_page(self):
        self.page += 1
        self.driver.get(f'{self.SEARCH_LINK}&page={self.page}')
        print('next page : ', self.page)

    def _click_button_with_label(self, label):
        try:
            self.driver.find_element(By.XPATH, f'//button/span[text()="{label}"]').click()
            return True
        except Exception as e:
            print(e)
            return False


    def get_email(self):
        try:
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//tp-yt-paper-button[@id="button"]/*[text()="View email address"]'))).click()
            # view_email_button_ele = self.driver.find_element(By.XPATH, '//tp-yt-paper-button[@id="button"]/*[text()="View email address"]').find_element_by_xpath('..')
            # view_email_button_ele.click()
            print("clicked view email button!")
            WebDriverWait(self.driver, 5).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@title='reCAPTCHA']")))
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//span[@id="recaptcha-anchor"]'))).click()
            self.driver.switch_to.default_content()
            sleep(1)
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[@id="submit-btn"]'))).click()
            email = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//a[@id="email"]'))).text
            # email = self.driver.find_element_by_xpath('//a[@id="email"]').text
            return email
        except Exception as e:
            print(e)
            return False

    def perform_task(self):
        try:
            self.driver.get(self.channel_link)
            business_email = self.get_email()
            print(business_email)
        except Exception as e:
            print(e)

    def run(self):
        while True:
            self.perform_task()
            

def main():
    my_bot = Bot()
    my_bot.start()


if __name__ == '__main__':
    main()