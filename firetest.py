from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import concurrent.futures

FIREFOX_BINARY_PATH = 'C:/Program Files/Mozilla Firefox/firefox.exe'
DRIVER_PATH = 'geckodriver.exe'

driver = webdriver.Firefox(executable_path=DRIVER_PATH, firefox_binary=FIREFOX_BINARY_PATH)

driver.get('https://www.imdb.com/title/tt0111161/')

time.sleep(5)
driver.quit()