from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException
import time
import json


class EasyApplyIndeed:

    def __init__(self, data): 
        self.email = data['email']
        self.password = data['password']
        self.keywords = data['keywords']
        self.location = data['location']
        self.driver = webdriver.Chrome('./driver/chromedriver') 

       

    def search(self):
        self.driver.maximize_window()  
        self.driver.get('https://uk.indeed.com/?from=gnav-jobsearch--jasx')
        self.driver.implicitly_wait(2)
        search_keywords = self.driver.find_element(By.CSS_SELECTOR,'input#text-input-what') 
        search_keywords.send_keys(self.keywords)
        time.sleep(4)
        search_location = self.driver.find_element(By.CSS_SELECTOR,'input#text-input-where')
        search_location.send_keys(self.location)
        search_location.send_keys(Keys.RETURN)

    def filter(self):
        self.driver.implicitly_wait(1)
        elements = ['//*[@id="filter-radius"]', '//*[@id="filter-radius-menu"]/li[3]/a', '//*[@id="filter-dateposted"]', '//*[@id="filter-dateposted-menu"]/li[2]/a']

        for element in elements:
            try:     
                filt = self.driver.find_element(By.XPATH, element)
                filt.click()
            except StaleElementReferenceException:
                print('Handled Stale Element error')
                pass    
            except NoSuchElementException:
                print('Handled No Such Element error')
                pass
            continue
   
    def interact(self):
        time.sleep(5)     
        checklist = []
        checklist = self.driver.find_elements(By.CLASS_NAME,'job_seen_beacon')
        print(len(checklist))
        for items in checklist:
            try:
                items.click()
                self.driver.implicitly_wait(2)
                items = self.driver.switch_to.frame(self.driver.find_element(By.XPATH,'//*[@id="vjs-container-iframe"]'))
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'ia-IndeedApplyButton')))
                items = self.driver.find_element(By.CLASS_NAME,'ia-IndeedApplyButton').click()
            except NoSuchElementException : 
                print('Handled No Such Element error')
                pass
            except StaleElementReferenceException:
                print('Handled Stale Element error')
                pass
            except ElementClickInterceptedException:
                print ('Handled Element Click Intercepted error')
                pass
                continue

    def login(self):
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
        try:
            time.sleep(3)
            get_that_job = self.driver.find_element(By.CLASS_NAME,'ia-continueButton ia-ContactInfo-continue css-vw73h2 e8ju0x51')
            get_that_job.click()
            print ('USER INPUT NEEDED')
            
        except NoSuchElementException : 
                print('Handled No Such Element error, additional input needed')
                pass
        except StaleElementReferenceException:
                print('Handled Stale Element error, additional input needed')
                pass
        except ElementClickInterceptedException:
                print ('Handled Element Click Intercepted error, additional input needed')
                pass
        print ('END OF RUN')
                   

    def apply(self):    
        
        self.search()
        self.filter()
        self.interact()
        self.login()
        self.last_stage()
        
    
if  __name__ == '__main__':
    with open('config.json') as config_file:
        data = json.load(config_file)

        bot = EasyApplyIndeed(data)
        bot.apply()

   
   
    


