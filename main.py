from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException,TimeoutException
import time
import json
import logging
import pyautogui


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

    def filter(self):
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
   
    def interact(self):#TODO sort try catches
        """Iterates through results. MOST FAILURES ARE HERE. Failures due to unforseen elements appearing on page DOM, changes often so hard to handle exceptions """
             
        checklist = self.driver.find_elements(By.CLASS_NAME,'job_seen_beacon')
        print(f'Jobs found {len(checklist)}')

        for element in checklist:
            try:
                element.click()
                time.sleep(2)
                pyautogui.moveTo(1892,652)
                time.sleep(2)
                pyautogui.click()                              
            except NoSuchElementException:
                self.driver.switchTo().defaultContent()
                for element in checklist[1:]:
                    try:
                        element.click()
                        time.sleep(5)
                        pyautogui.moveTo(1892,652)
                        pyautogui.click
                        #self.driver.switchTo().defaultContent()
                    except NoSuchElementException : 
                        pass
                    except StaleElementReferenceException:
                        self.driver.switchTo().defaultContent()          

    def login(self):#TODO find last input elements
        """Logs in when suitable job is clicked . Do this low down in order of functions as Captcha often presented at this point ."""
        try:
            self.driver.implicitly_wait(8)
            login_email = self.driver.find_element(By.CSS_SELECTOR,'#ifl-InputFormField-3')
            login_email.send_keys(self.email)
        except: NoSuchElementException
        
        pyautogui.moveTo(1688,978)
        pyautogui.click()
        time.sleep(3)
        login_email = self.drivers        
        login_email.send_keys(self.email)    
        login_email.send_keys(Keys.RETURN)
        self.driver.implicitly_wait(7)
        login_password = self.driver
        login_password.send_keys(self.password)
        time.sleep(2)
        login_password.send_keys(Keys.RETURN)    

    def last_stage(self):
        """Gets as far as uploading a CV. I thought it best to start manually checking things at this point."""

        try:
            time.sleep(3)
            get_that_job = self.driver.find_element(By.CLASS_NAME,'ia-continueButton ia-ContactInfo-continue css-vw73h2 e8ju0x51')
            get_that_job.click()
            print('USER INPUT NEEDED')
        except NoSuchElementException: 
            pass
        except StaleElementReferenceException:
            pass
        except ElementClickInterceptedException:
            pass
            print('END OF RUN')
                   
    def apply(self):    
        self.search()
        self.filter()
        self.interact()
        self.login()
        self.last_stage()


if  __name__ == '__main__':
    with open('config.json') as config_file:
        config = json.load(config_file)
        bot = EasyApplyIndeed(config)
        bot.apply()  