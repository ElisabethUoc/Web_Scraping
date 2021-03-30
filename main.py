import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from IPython.display import IFrame
import time
import pandas as pd
import csv

url = 'https://www.hometogo.com/search/5460aea910151?adults=2&arrival=2021-05-31&duration=6&maxPricePerNight=175EUR'

driver = webdriver.Chrome('chromedriver')
driver.get(url)

time.sleep(2)  # Allow 2 seconds for the web page to open
scroll_pause_time = 1
screen_height = driver.execute_script("return window.screen.height;")   # get screen height
i = 1
while True:
    # scroll screen height
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
    i += 1
    time.sleep(scroll_pause_time)
    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    scroll_height = driver.execute_script("return document.body.scrollHeight;")
    # Break the loop when the height we need to scroll to is larger than the total scroll height
    if screen_height * i > scroll_height:
        break

soup = BeautifulSoup(driver.page_source, 'html.parser')

listings = soup.find_all('div', 'posr h100p w100p')

FEATURES = {
    'name': {'tag': 'div', 'class': 'text-medium fwb c-black lh18 ovh text-overflow'},
    'price': {'tag': 'span', 'class': 'fwb wsnw fz16'},
    'location': {'tag': 'span', 'class': 'c-gray-extra-dark text-small text-overflow'},
    'rating': {'tag': 'span', 'class': 'text-small c-accent-normal'},
    'important_info': {'tag': 'span', 'class': 'fz11'},
    'specifications': {'tag': 'div', 'class': 'text-small text-overflow'},
    'link': {'tag': 'a', 'get': 'href'}
}


def extract_element(listing_html, params):
    # 1. Find the right tag
    if 'class' in params:
        elements_found = listing_html.find_all(params['tag'], params['class'])
    else:
        elements_found = listing_html.find_all(params['tag'])
    # 2. Extract the right element
    tag_order = params.get('order', 0)
    element = elements_found[tag_order]
    # 3. Get text
    if 'get' in params:
        output = element.get(params['get'])
    else:
        output = element.get_text()
    return output


one_row = []
for i in range(len(listings)):
    for feature in FEATURES:
        try:
            one_row.append(extract_element(listings[i], FEATURES[feature]))
        except:
            one_row.append('empty')

list_of_rows = [one_row[i:i+7] for i in range(0, len(one_row), 7)]

with open('hometogo.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(list_of_rows)
    
df = pd.read_csv('hometogo.csv')
df.columns = list(FEATURES.keys())
df.to_csv('hometogo.csv')