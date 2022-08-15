from IPython.display import display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import concurrent.futures
import pandas as pd

t1 = time.perf_counter()

df = pd.read_csv('testdata.csv')

idf = list(df['ID'])


CHROME_PATH = '/usr/bin/google-chrome'
CHROMEDRIVER_PATH = 'chromedriver.exe'
WINDOW_SIZE = "1920,1200"

options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=%s" % WINDOW_SIZE)
options.binary_location = CHROME_PATH

def get_data(title_id):
    driver = webdriver.Chrome(
        executable_path=CHROMEDRIVER_PATH, chrome_options=options)
    driver.get('https://www.imdb.com/title/' + title_id)
    try:
        title = driver.find_element(by= By.XPATH, value ='//*[@data-testid = "hero-title-block__title"]').text
    except Exception:
        title = 'N/A'
    # year = driver.find_element_by_xpath('//*[@class="title-year"]').text
    # rating = driver.find_element_by_xpath('//*[@class="rating-rating"]').text
    # director = driver.find_element_by_xpath('//*[@class="director"]').text

    new_row = {'ID': title_id, 'Title': title}
    driver.close()
    print(new_row)
    mainsheet.append(new_row, ignore_index=True)

mainsheet = pd.DataFrame(columns=['ID','Title'])
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(get_data, idf)

print(len(idf))
display(df)
t2 = time.perf_counter()
print(f'Finished in {t2-t1} seconds')