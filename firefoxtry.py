from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import concurrent.futures
from IPython.display import display
import json

Firefox_PATH = 'C:/Program Files/Mozilla_Firefox/firefox.exe'
DRIVER_PATH = 'geckodriver.exe'

WINDOW_SIZE = "1920,1200"
options = Options()
options.add_argument("--headless") 
options.add_argument("--window-size=%s" % WINDOW_SIZE)
options.binary_location = Firefox_PATH

t1 = time.perf_counter()

batch_size = 10
sublist = []
data = pd.read_csv('testdata.csv')
mainlist = list(data['ID'])
for i in range(0,len(mainlist),batch_size):
    sublist.append(mainlist[i:i+batch_size])

t1 = time.perf_counter()
def work(sublist):
    def scrape(id):
        driver.get('https://www.imdb.com/title/' + id)
        data = driver.find_element(By.ID, '__NEXT_DATA__').get_attribute('innerHTML')
        data = json.loads(data)
    

        base_address = "data['props']['pageProps']['aboveTheFoldData']"
        title_path = (f"{base_address}['originalTitleText']['text'] if 'originalTitleText' in {base_address} else 'N/A'")
        year_path = (f"{base_address}['releaseYear']['year'] if 'releaseYear' in {base_address} else 'N/A'")
        rating_path = (f"{base_address}['ratingsSummary']['aggregateRating'] if 'ratingsSummary' in {base_address} else 'N/A'")
        genre_path = (f"{base_address}['genres']")
        general_cast_path = (f"{base_address}['principalCredits']")
        
        general_cast = eval(general_cast_path)
        title = eval(title_path)
        year = eval(year_path)
        rating = eval(rating_path)

        director = 'N/A'
        actor_list = []

        for item in general_cast:
            type = item['category']['text']
            if type == 'Director':
                director = item['credits'][0]['name']['nameText']['text']
            elif type == 'Stars':
                actors = item['credits']
                for actor in actors:
                    name = actor['name']['nameText']['text']
                    actor_list.append(name)
                if len(actor_list) == 0:
                    actor_list = 'N/A'
        genres = eval(genre_path)
        genre_list = []
        if genres == None:
            genre_list = 'N/A'
        else:
            for genre in genres['genres']:
                genre_list.append(genre['text'])

        items = {'ID': id, 'Title': title, 'Year': year, 'Rating': rating, 'Director': director, 'Actors': actor_list, 'Genres': genre_list}
        return items
    df = pd.DataFrame()
    driver = webdriver.Firefox(executable_path=DRIVER_PATH, options=options)
    for id in sublist:
        df = df.append(scrape(id), ignore_index=True)
    driver.close()
    df.to_csv('imdb_data.csv',mode='a', header=False, index=False)


sheet = pd.DataFrame(columns=['ID','Title', 'Year', 'Rating', 'Director', 'Actors', 'Genres'])
sheet.to_csv('imdb_data.csv', index=False)

with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
    results = executor.map(work, sublist)

t2 = time.perf_counter()

display(pd.read_csv('imdb_data.csv'))

print(f'Finished in {t2-t1} seconds')
