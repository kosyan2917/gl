import string
import random
from anticaptchaofficial.hcaptchaproxyless import *
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import threading


#https://wn.nr/j3JLCs
#//i[@class='far fa-envelope']
#$('form').submit()
#document.querySelector('[name="h-captcha-response"]').innerHTML = captcha
#document.querySelector('[name="g-recaptcha-response"]').innerHTML = captcha
class AutoReg:
    
    def __init__(self):
        self.datakey = '2df90a06-8aca-45ee-8ba2-51e9a9113e82'
        self.ref = 'https://wn.nr/j3JLCs'
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--window-size=1600,900")
        self.driver = uc.Chrome(executable_path='chromedriver.exe', chrome_options=options)
        self.actions = ActionChains(self.driver)
        self.wait = WebDriverWait(self.driver, 10)
        self.key = self.get_key()
        self.driver.get(self.ref)


    @staticmethod
    def get_key():
        with open('data.txt', 'r') as file:
            return file.readline()

    def wait_for_element(self, element):
        return self.wait.until(EC.presence_of_element_located((By.XPATH, element)))

    @staticmethod
    def gen_code():
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
        
    def start(self):
        while True:
            el = self.wait_for_element(".//i[@class='far fa-envelope']")
            el = self.driver.find_elements_by_xpath(".//a[@class='no-underline email-background popup-window']")[3]
            el.click()
            self.wait_for_element('.//input[@name=\'name\']')
            name = self.driver.find_elements_by_xpath(".//input[@name='name']")[1]
            name.click()
            name.send_keys(self.gen_code())
            email = self.driver.find_elements_by_xpath(".//input[@name='email']")[1]
            email.click()
            email.send_keys(self.gen_code()+'@monkos.ru')
            button = self.driver.find_element_by_xpath('.//button[@class=\'btn btn-primary ng-scope\']')
            button.click()
            href = self.wait.until(EC.element_to_be_clickable((By.XPATH, ".//a[@class='no-underline enter-link custom-border custom_action-border clearfix mandatory default']")))
            href.click()
            el = self.wait_for_element('.//label[@class=\'radio ng-binding\']')
            el.click()
            self.driver.find_element_by_xpath(".//button[@class='btn btn-primary']").click()
            self.wait_for_element(".//h2[text()='Prove that you are human']")
            token = self.captcha()
            self.driver.execute_script(f'''var fcName = '';
    var elements = document.getElementsByClassName('hcaptcha ng-scope ng-isolate-scope')[0];
    var mt = Object.getOwnPropertyNames(elements);
    for(var i=0;i<mt.length;i++)
        {{
        if(mt[i].includes('jQuery')){{
            fcName = mt[i];
            break;
        }}
    }}
    if(fcName!=''){{elements[fcName].$scope.challengeCompleted(\'{token}\')}}''')
            self.wait_for_element('.//a[@data-logout-link="true"]')
            el = self.driver.find_elements_by_xpath('.//a[@data-logout-link="true"]')[2]
            el.click()
        
    def captcha(self):
        solver = hCaptchaProxyless()
        solver.set_verbose(1)
        solver.set_key(self.key)
        solver.set_website_url(self.driver.current_url)
        solver.set_website_key(self.datakey)
        response = solver.solve_and_return_solution()
        while not response:
            response = solver.solve_and_return_solution()
            time.sleep(2)
        return response
        
        
def thread_it(num):
    threads = []
    for i in range(0,num):
        reg = AutoReg()
        thread = threading.Thread(target=reg.start)
        thread.start()
        threads.append(thread)
    return threads

if __name__ == '__main__':
    print(thread_it(5))
    
'''var fcName = '';
var elements = document.getElementsByClassName('hcaptcha ng-scope ng-isolate-scope')[0];
var mt = Object.getOwnPropertyNames(elements);
for(var i=0;i<mt.length;i++)
    {
    if(mt[i].includes('jQuery')){
        fcName = mt[i];
        break;
    }
}
if(fcName!=''){elements[fcName].$scope.challengeCompleted(token)'''