from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException,TimeoutException
import time
import json
import logging
import pyautogui as pg


logging.basicConfig(filename="botlogfile.log",
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filemode='a')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class EasyApplyIndeed:

    def __init__(self, config: dict): 
        """ Initialise parameters here. Directs program to your config file. """

        self.email: str = config.get('email')
        self.password: str = config.get('password')
        self.keywords: str = config.get('keywords')
        self.location: str = config.get('location')

        if self.email is None or self.password is None or self.keywords is None or self.location is None:
            raise KeyError

        self.driver = webdriver.Chrome('./driver/chromedriver') 

    def search(self):
        """Goes to site. Information to be loaded into search queries."""

        self.driver.maximize_window()  
        self.driver.get('https://uk.indeed.com/?from=gnav-jobsearch--jasx')
        time.sleep(2)

        search_keywords = self.driver.find_element(By.CSS_SELECTOR,'input#text-input-what') 
        search_keywords.send_keys(self.keywords)        
        time.sleep(1)

        search_location = self.driver.find_element(By.CSS_SELECTOR,'input#text-input-where')
        search_location.send_keys(self.location)
        search_location.send_keys(Keys.RETURN)
        self.driver.implicitly_wait(1)

    def filter(self): # change elements in list here if you want different filter parameters 
        """Filtering rules from dropdown menu's."""
        
        elements = [
            '//*[@id="filter-radius"]',
            '//*[@id="filter-radius-menu"]/li[2]/a', 
            '//*[@id="filter-dateposted"]', 
            '//*[@id="filter-dateposted-menu"]/li[2]/a'
        ]

        for element in elements:     
            filt = self.driver.find_element(By.XPATH, element)
            filt.click()
        time.sleep(3)
   
    def interact(self):
        """Iterates through results."""
             
        checklist = self.driver.find_elements(By.CLASS_NAME,'job_seen_beacon')
        print(f'Jobs found {len(checklist)}')

        for element in checklist:
            element.click()
            time.sleep(2)
            pg.moveTo(1892,652)
            time.sleep(2)
            pg.click()                              
        
    def login(self):
        """Logs in when suitable job is clicked . Do this low down in order of functions as Captcha often presented at this point ."""
        try:
            self.driver.implicitly_wait(8)
            login_email = self.driver.find_element(By.CSS_SELECTOR,'#ifl-InputFormField-3')
            login_email.send_keys(self.email)
        except: NoSuchElementException
        
        pg.moveTo(1688,978)
        pg.click()
        time.sleep(3)
        pg.typewrite(self.email)      
        pg.click()
        time.sleep(7)
        pg.moveTo(1682,508)
        pg.click()
        pg.typewrite(self.password)
        pg.moveTo(1915,652)        
        time.sleep(2)
        pg.click()
        print('USER INPUT NEEDED')

                   
    def apply(self):    
        self.search()
        self.filter()
        self.interact()
        self.login()


if  __name__ == '__main__':
    with open('config.json') as config_file:
        config = json.load(config_file)
        bot = EasyApplyIndeed(config)
        bot.apply()  