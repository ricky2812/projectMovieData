from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd 
import time
import concurrent.futures
from IPython.display import display

# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC


CHROME_PATH = 'C:/Program Files/Google/Chrome/Application/chrome.exe.'
DRIVER_PATH = 'chromedriver.exe'
WINDOW_SIZE = "1920,1200"

options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=%s" % WINDOW_SIZE)
options.binary_location = CHROME_PATH

batch_size = 10
t1 = time.perf_counter()
l_id = []
data = pd.read_csv('testdata.csv')
m_id = list(data['ID'])
for i in range(0,len(m_id),batch_size):
    l_id.append(m_id[i:i+batch_size])

def work(l_id):
    def web(id):
        
        driver.get('https://www.imdb.com/title/'+ id)

        try:
            m_name = driver.find_element_by_xpath('//*[@class="sc-b73cd867-0 eKrKux"]').text
        except:
            m_name = 'N/A'

        try:
            rating = driver.find_element_by_xpath('//*[@class="sc-7ab21ed2-1 jGRxWM"]').text
            rating = float(rating)
        except:
            rating = 'N/A'

        try:
            year = driver.find_element_by_xpath('/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[1]/div[1]/div/ul/li[1]/a').text
        except:
            year = 'N/A'

        try:
            director = driver.find_element_by_xpath('//*[@class="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"]').text
            if director == '':
                director = 'N/A'
        except:
            director = 'N/A'

        gen = driver.find_elements_by_xpath('//*[@class="ipc-inline-list ipc-inline-list--show-dividers baseAlt"]')
        if len(gen) > 0:
            genres = []
            for i in gen:
                genres.append(i.text)
        else:
            genres = 'N/A'

        ac = driver.find_elements_by_xpath('//ul[@class="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content baseAlt"][2]/li')
        if len(ac) > 0:
            actors = []
            for i in ac:
                actors.append(i.text)
        else:
            actors = 'N/A'

        new_row = dict({'ID':id,
                        'name': m_name,
                        'rating': rating,
                        'year': year,
                        'director': director,
                        'actors': actors,
                        'genres': genres,
                        })
        return new_row
        
    df = pd.DataFrame()
    driver = webdriver.Chrome(executable_path = DRIVER_PATH, chrome_options = options)
    for id in l_id:
        df = df.append(web(id), ignore_index=True)
    driver.close()
    df.to_csv('contextsheet.csv', mode='a', header=False, index=False) 


mainsheet = pd.DataFrame(columns=['ID','name', 'rating', 'year', 'director', 'actors', 'genres'])
mainsheet.to_csv('contextsheet.csv',index=False)
with concurrent.futures.ThreadPoolExecutor(max_workers = 6) as executor:
    executor.map(work, l_id)

display(pd.read_csv('contextsheet.csv'))


t2 = time.perf_counter()
print(f'Finished in {t2-t1} seconds')