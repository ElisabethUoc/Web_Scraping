import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from IPython.display import IFrame
import time

url = 'https://www.hometogo.com/search/5460aea910151?adults=2&arrival=2021-05-31&duration=6&maxPricePerNight=175EUR'

driver = webdriver.Chrome('chromedriver')
driver.get(url)

time.sleep(2)  # Allow 2 seconds for the web page to open
scroll_pause_time = 1 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
i = 1
while True:
    # scroll one screen height each time
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

RULES_SEARCH_PAGE = {
    'name': {'tag': 'div', 'class': 'text-medium fwb c-black lh18 ovh text-overflow'},
    'price': {'tag': 'span', 'class': 'fwb wsnw fz16'},
    'location': {'tag': 'span', 'class': 'c-gray-extra-dark text-small text-overflow'},
    'rating': {'tag': 'div', 'class': 'df aib cols>m4 text-medium c-accent-normal'},
    'cancelation': {'tag': 'span', 'class': 'fz11'},
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


for feature in RULES_SEARCH_PAGE:
    try:
        print(f"{feature}: {extract_element(listings[0], RULES_SEARCH_PAGE[feature])}")
    except:
        print(f"{feature}: empty")
