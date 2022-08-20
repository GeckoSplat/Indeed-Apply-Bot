from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
import time
import json


class EasyApplyIndeed:

    def __init__(self, data): 
        self.email = data['email']
        self.password = data['password']
        self.keywords = data['keywords']
        self.location = data['location']
        self.driver = webdriver.Chrome('./driver/chromedriver') 

    def login(self):
        self.driver.maximize_window()
        self.driver.get('https://secure.indeed.com/auth?hl=en_GB&co=GB&continue=https%3A%2F%2Fuk.indeed.com%2F&tmpl=desktop&service=my&from=gnav-util-homepage&jsContinue=https%3A%2F%2Fuk.indeed.com%2F&empContinue=https%3A%2F%2Faccount.indeed.com%2Fmyaccess')
        time.sleep(15)
        login_email = self.driver.find_element(By.ID,'ifl-InputFormField-3')
        login_email.clear()
        login_email.send_keys(self.email)
        time.sleep(5)    
        login_email.send_keys(Keys.RETURN)
        time.sleep(12)
        login_password = self.driver.find_element(By.ID,'ifl-InputFormField-136')
        login_password.clear()
        login_password.send_keys(self.password)
        time.sleep(6)
        login_password.send_keys(Keys.RETURN)    

    def search(self):  
        self.driver.implicitly_wait(2)
        search_keywords = self.driver.find_element(By.CSS_SELECTOR,'input#text-input-what') 
        search_keywords.send_keys(self.keywords)
        search_location = self.driver.find_element(By.CSS_SELECTOR,'input#text-input-where')
        search_location.send_keys(self.location)
        search_location.send_keys(Keys.RETURN)

    def filter(self):
        self.driver.implicitly_wait(2)
        elements = ['//*[@id="filter-radius"]', '//*[@id="filter-radius-menu"]/li[2]/a', '//*[@id="resultsCol"]/div[3]/div[4]/div[1]/span[2]/a']

        for element in elements:
            self.driver.implicitly_wait(2)
            filt = self.driver.find_element(By.XPATH, element)
            filt.click()

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
                print('negated No Such Element error')
                pass
            except StaleElementReferenceException:
                print('negated Stale Element error')
                pass
            except ElementClickInterceptedException:
                print ('negated Element Click Intercepted error')
                pass
            
                continue



    def apply(self):  # this will be last function. call all funcs in order here    
        self.login()
        self.search()
        self.filter()
        self.interact()

        
    
if  __name__ == '__main__':
    with open('config.json') as config_file:
        data = json.load(config_file)

        bot = EasyApplyIndeed(data)
        bot.apply()

    # TO DO need to figure out login / beat capcha VID ON THIS   <<<<< this next
    


