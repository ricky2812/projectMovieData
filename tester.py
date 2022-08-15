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

CHROME_PATH = 'C:/Program Files/Google/Chrome/Application/chrome.exe.'
DRIVER_PATH = 'chromedriver.exe'
WINDOW_SIZE = "1920,1200"
options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=%s" % WINDOW_SIZE)
options.binary_location = CHROME_PATH

list_id = ['tt9419884','tt3466016']

sheet = pd.DataFrame(columns=['ID','Title', 'Year', 'Rating', 'Director', 'Actors', 'Genres'])

driver = webdriver.Chrome(executable_path = DRIVER_PATH, chrome_options = options)
driver.get('https://www.imdb.com/title/' + list_id[1])
data = driver.find_element(By.ID, '__NEXT_DATA__').get_attribute('innerHTML')
data = json.loads(data)

base_address = "data['props']['pageProps']['aboveTheFoldData']"

title_path = (f"{base_address}['originalTitleText']['text'] if 'originalTitleText' in {base_address} else 'N/A'")
title = eval(title_path)
print('Title: ', title)

year_path = (f"{base_address}['releaseYear']['year'] if 'releaseYear' in {base_address} else 'N/A'")
year = eval(year_path)
print('year: ', year)

rating_path = (f"{base_address}['ratingsSummary']['aggregateRating'] if 'ratingsSummary' in {base_address} else 'N/A'")
rating = eval(rating_path)
print('rating: ', rating)

director_path = (f"{base_address}['principalCredits'][0]['credits'][0]['name']['nameText']['text'] if 'principalCredits' in {base_address} else 'N/A'")
director = eval(director_path)
print('director: ', director)

actor_path = (f"{base_address}['principalCredits'][2]['credits'] if 'principalCredits' in {base_address} else 'N/A'")
actors = eval(actor_path)
actor_list = []
for actor in actors:
    actor_list.append(actor['name']['nameText']['text'])

genre_path = (f"{base_address}['genres']['genres'] if 'genres' in {base_address} else 'N/A'")
genres = eval(genre_path)
genre_list = []
for genre in genres:
    genre_list.append(genre['text'])

items = {'ID': list_id[1], 'Title': title, 'Year': year, 'Rating': rating, 'Director': director, 'Actors': actor_list, 'Genres': genre_list}
print(items)
 


sheet = sheet.append(items, ignore_index=True)
driver.close()
display(sheet)