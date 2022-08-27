from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException,TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time
import json


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
        self.driver.implicitly_wait(2)
        time.sleep(4)

        search_keywords = self.driver.find_element(By.CSS_SELECTOR,'input#text-input-what') 
        search_keywords.send_keys(self.keywords)        
        time.sleep(3)

        search_location = self.driver.find_element(By.CSS_SELECTOR,'input#text-input-where')
        search_location.send_keys(self.location)
        search_location.send_keys(Keys.RETURN)
        self.driver.implicitly_wait(1)

    def filter(self):
        """Filtering rules from dropdown menu's."""
        
        elements = [
            '//*[@id="filter-radius"]',
            '//*[@id="filter-radius-menu"]/li[3]/a', 
            '//*[@id="filter-dateposted"]', 
            '//*[@id="filter-dateposted-menu"]/li[2]/a'
        ]

        for element in elements:
            try:     
                filt = self.driver.find_element(By.XPATH, element)
                filt.click()
            except StaleElementReferenceException:
                print('Handled Stale Element error')    
            except NoSuchElementException:
                print('Handled No Such Element error')
   
        time.sleep(5)
   
    def interact(self):
        """Iterates through results. MOST FAILURES ARE HERE. Failures due to unforseen elements appearing on page DOM, changes often so hard to handle exceptions """
             
        checklist = self.driver.find_elements(By.CLASS_NAME,'job_seen_beacon')
        print(f'Jobs found {len(checklist)}')

        for element in checklist:
            try:
                element.click()
                self.driver.implicitly_wait(2)
                element = self.driver.switch_to.frame(self.driver.find_element(By.XPATH,'//*[@id="vjs-container-iframe"]'))
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'ia-IndeedApplyButton')))
                element = self.driver.find_element(By.CLASS_NAME,'ia-IndeedApplyButton')
                ActionChains(self.driver).move_to_element(By.CLASS_NAME,'ia-IndeedApplyButton')
                ActionChains.click()
                ActionChains.perform()
                time.sleep(1.5)
            except NoSuchElementException : 
                print('Handled No Such Element error')
                pass
            except StaleElementReferenceException:
                for element in checklist[1:]:
                    try:
                        element.click()
                        self.driver.implicitly_wait(2)
                        element = self.driver.switch_to.frame(self.driver.find_element(By.XPATH,'//*[@id="vjs-container-iframe"]'))
                        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'ia-IndeedApplyButton')))
                        element = self.driver.find_element(By.CLASS_NAME,'ia-IndeedApplyButton')
                        ActionChains(self.driver).move_to_element(By.CLASS_NAME,'ia-IndeedApplyButton')
                        ActionChains.click()
                        ActionChains.perform()
                        time.sleep(1.5)
                    except StaleElementReferenceException:
                        print('Handled Stale Element error')
                        pass
                    continue
                print('Handled Stale Element error')
                pass
            
            except ElementClickInterceptedException:
                print('Handled Element Click Intercepted error')
                pass

            except TimeoutException:
                for element in checklist[1:]:
                    try:
                        element.click()
                        self.driver.implicitly_wait(2)
                        element = self.driver.switch_to.frame(self.driver.find_element(By.XPATH,'//*[@id="vjs-container-iframe"]'))
                        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'ia-IndeedApplyButton')))
                        element = self.driver.find_element(By.CLASS_NAME,'ia-IndeedApplyButton')
                        ActionChains(self.driver).move_to_element(By.CLASS_NAME,'ia-IndeedApplyButton')
                        ActionChains.click()
                        ActionChains.perform()
                        time.sleep(1.5)
                    except StaleElementReferenceException:
                        print('Handled Stale Element error')
                        pass
                    continue
                print('Handled Timeout error')    
            continue 

    def login(self):
        """Logs in when suitable job is clicked . Do this low down in order of functions as Captcha often presented at this point ."""

        time.sleep(1)
        self.driver.implicitly_wait(7)
        login_email = self.driver.find_element(By.ID,'ifl-InputFormField-3')  
        login_email.clear()
        login_email.send_keys(self.email)
        time.sleep(5)    
        login_email.send_keys(Keys.RETURN)
        time.sleep(7)
        login_password = self.driver.find_element(By.ID,'ifl-InputFormField-141')
        login_password.clear()
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
            print('Handled No Such Element error, additional input needed')
            pass
        except StaleElementReferenceException:
            print('Handled Stale Element error, additional input needed')
            pass
        except ElementClickInterceptedException:
            print('Handled Element Click Intercepted error, additional input needed')
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
