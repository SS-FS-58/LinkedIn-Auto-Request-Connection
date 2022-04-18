from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from threading import Thread, Event
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
        self.SEARCH_LINK = os.getenv('SEARCH_LINK')
        self.SEND_MESSAGE = os.getenv('SEND_MESSAGE').replace('\\n','\n')

    def setdriver(self):
        try:
            self.init_task_info()
            options = webdriver.FirefoxOptions()
            options.add_argument("--start-maximized")
            # options.headless = True
            profile = webdriver.FirefoxProfile(self.DEFAULT_PROFILE)
            self.driver = webdriver.Firefox(executable_path="geckodriver.exe", options=options, firefox_profile=profile)
            self.driver.get(self.SEARCH_LINK)
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

    def perform_task(self):
        try:
            while self.today_count < self.total_request:
                connectable_buttons = self.driver.find_elements(By.XPATH, '//button/span[text()="Connect"]')
                for connectable_button in connectable_buttons:
                    connectable_button.click()
                    self._click_button_with_label("Add a note")
                    self.driver.find_element(By.XPATH, '//textarea[@id="custom-message"]').send_keys(self.SEND_MESSAGE)
                    if self._click_button_with_label("Send"):
                        self.today_count += 1
                    else:
                        self._click_button_with_label("Cancel")
                        actions = ActionChains(self.driver)
                        actions.send_keys(Keys.ESCAPE)
                        actions.perform()
                self._next_page()
        except Exception as e:
            print(e)

    def run(self):
        while True:
            self.perform_task()
            self.close()
            sleep(3600*24)
            self.setdriver()

def main():
    my_bot = Bot()
    my_bot.start()


if __name__ == '__main__':
    main()