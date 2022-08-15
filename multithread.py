from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import concurrent.futures
import json

CHROME_PATH = 'C:/Program Files/Google/Chrome/Application/chrome.exe.'
DRIVER_PATH = 'chromedriver.exe'
WINDOW_SIZE = "1920,1200"
options = Options()
options.add_argument("--headless") 
options.add_argument("--window-size=%s" % WINDOW_SIZE)
options.binary_location = CHROME_PATH

def lotr():
    batch_size = 1
    sublist = []
    data = pd.read_csv('metadata.csv')
    mainlist = list(data['ID'])
    end = len(mainlist)
    for i in range(0,500,batch_size): #(0,end,batch_size) at the end
        sublist.append(mainlist[i:i+batch_size])

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
            if actor_list == []:
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
        driver = webdriver.Chrome(executable_path = DRIVER_PATH, chrome_options = options)
        for id in sublist:
            df = df.append(scrape(id), ignore_index=True)
        driver.close()
        df.to_csv('imdb_data.csv',mode='a', header=False, index=False)

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(work, sublist)

if __name__ == '__main__':
    lotr()