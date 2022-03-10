from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['mvideo']
products = db.products

s = Service('../chromedriver')
options = Options()
options.add_argument('start-maximized')

driver = webdriver.Chrome(service=s, options=options)
driver.implicitly_wait(30)

driver.get("https://www.mvideo.ru/")

wait = WebDriverWait(driver, 30)
button = wait.until(EC.presence_of_element_located(By.CLASS_NAME, 'tab-button ng-star-inserted'))
button = driver.find_elements(By.CLASS_NAME, 'tab-button ng-star-inserted')[1]
button.click()

products = driver.find_elements(By.XPATH, "//div[contains(@class, 'mvid-carousel-inner')]")
items_list = []
for product in products:
    name = product.find_element(By.XPATH, ".//div[contains(@class, '_ngcontent-serverapp-c237')]").text
    items_list.append(name)

products.insert_many(items_list)
driver.close()