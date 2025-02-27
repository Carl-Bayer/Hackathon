#import time
#import datetime
#import json
import os
#from selenium import webdriver
from selenium.webdriver.edge.service import Service

from selenium.webdriver.common.by import By


import selenium
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import csv

import configparser


# Read the property file
config = configparser.ConfigParser()
config.read('C:\\scraper\\config.ini')

# Get the start and end page numbers
start_page = int(config['PaginationSection']['start_page'])
end_page = int(config['PaginationSection']['end_page'])
print("---- definition is ---", start_page , '---->', end_page)

options = Options()
options.binary_location = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"

#driver = webdriver.Firefox(executable_path='C:\scraper\geckodriver.exe',options=options)
driver_path = 'C:\scraper\geckodriver.exe'
driver = webdriver.Firefox(service=Service(driver_path), options = options)


url_list = []

start_url = 'https://www.nmpa.gov.cn/datasearch/home-index.html#category=yp'
#start_url = 'https://www.nmpa.gov.cn/xxgk/ggtg/index.html'



driver.get(start_url)
time.sleep(15)

action = ActionChains(driver)
action.move_by_offset(100, 100).click().perform()

time.sleep(5)

first_click = driver.find_element(By.XPATH,'//*[@id="home"]/main/div[2]/div[2]/div[1]/div[1]/div[4]/a/span')
"""//*[@id="home"]/main/div[2]/div[2]/div[1]/div[1]/div[4]/a/span"""

first_click.click()

search_box = driver.find_element(By.XPATH,'//*[@id="home"]/main/div[1]/div[7]/div/div[2]/input')
search_box.send_keys("备2024")
search_box.send_keys(Keys.RETURN)


time.sleep(5)

driver.switch_to.window(driver.window_handles[0])

action = ActionChains(driver)
action.move_by_offset(100, 100).click().perform()

time.sleep(5)

driver.close()

driver.switch_to.window(driver.window_handles[0])
action = ActionChains(driver)
action.move_by_offset(100, 100).click().perform()
#j=664
j=start_page





dpaths = ['//*[@id="dataTable"]/div[2]/table/tbody/tr[' + str(i) + ']/td[2]/div/div/div' for i in range(1,13)]
          
column_names = ["备案号",
                "药品通用名称",
                "药品批准文号/原料药登记号",
                "上市许可持有人",
                "上市许可持有人地址",
                "生产企业名称",
                "生产企业地址",
                "备案内容","备案机关",
                "备案日期","备注","注"]



table_data = []
while j>=1:
    time.sleep(3)
    i = 1
    print("--- j ---", j)
    #if j==664:
    if j==start_page:
        try:
            input_page = driver.find_element(By.XPATH,'//*[@id="home"]/div[3]/div[3]/div/div/span[3]/div/input')
            input_page.clear()
            #input_page.send_keys("664")
            input_page.send_keys(str(start_page))
            input_page.send_keys(Keys.RETURN)
            time.sleep(2)
        except:
            print('--- locate specific page error')
    
    while i <= 10:
        page_data = []
        if i == 1:
            driver.switch_to.window(driver.window_handles[0])


        path = '//*[@id="home"]/div[3]/div[2]/div/div/div[3]/table/tbody/tr['+str(i)+']/td[4]/div/button'
        print(path)
        
        #for dpath in dpaths:
        elements = driver.find_element(By.XPATH,'//*[@id="home"]/div[3]/div[2]/div/div/div[3]/table/tbody/tr['+str(i)+']/td[2]/div/p')
        data = [elements.text]
        page_data.append(data)
        
        table_data.extend(list(zip(*page_data)))
        
        time.sleep(2)
        #driver.close()

        #driver.switch_to.window(driver.window_handles[0])
        print(i)
        i = i+1
    next_page = driver.find_element(By.XPATH,'//*[@id="home"]/div[3]/div[3]/div/div/button[1]')
    try:
        """next_page = driver.find_element(By.XPATH,'//*[@id="home"]/div[3]/div[3]/div/div/button[1]')"""
        next_page = driver.find_element(By.CLASS_NAME,"btn-prev")
        if "disable" in next_page.get_attribute("class"):
            j = 1
            continue    
        #elif j==575:
        elif j==end_page:
            break   
        else:
            next_page.click()
            j=j-1
            time.sleep(3)
    except NoSuchElementException:
        break
    
    

    """table_data.extend(list(zip(*page_data)))"""
    
driver.quit()


table_data.insert(0, column_names)

file_path = "C:\\scraper\\Registration_filter.csv"
with open(file_path, 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerows(table_data)

os.system(f'aws s3 cp {file_path} s3://py-crawling')

"""while True:
    time.sleep(5)
    links = driver.find_element()"""