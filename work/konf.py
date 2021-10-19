import datetime
import os
from dataclasses import dataclass
from pathlib import Path
from time import sleep
from requests import get
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


SCRIPT_PATH = Path(__file__).parent.resolve()
CACHED_FOLDER = f'{SCRIPT_PATH}\\Cached'

MAIN_URL = r'https://teplov.ru/'

@dataclass
class SystemInfo():
    systemName: str


def initDriver():
    Path(CACHED_FOLDER).mkdir(parents=True, exist_ok=True)

    s =  Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    driver.minimize_window()

    return driver


def getPages(driver):
    result = []

    driver.get(MAIN_URL) 
    # driver.get(f'{CACHED_FOLDER}/index.html')

    # sleep(2)

    systemUrls = driver.find_elements(By.CSS_SELECTOR, '.menu_sidebar>li>a[href="/catalog/pravilnye-dymokhody-teplov-i-sukhov/"]+ul>li')

    for a in systemUrls:
        link = a.find_element(By.CSS_SELECTOR, 'a')
        url = link.get_attribute('href') 
        txt = a.get_attribute("innerText")
        print(txt, url,sep="\t")
        result.append({
            'title':txt,
            'url': url
            })

    return result


def parsePages(driver, pages):
    result = []

    for page in pages:

        print(f"Load '{page['title']}' url: '{page['url']}'")

        sleep(3)
        driver.get(page['url'])
        sleep(3)

        systemSubNames = driver.find_elements(By.CSS_SELECTOR, '.element-title>h2')
        systemTables = driver.find_elements(By.CSS_SELECTOR, '.dataTables_scrollBody>.stripe.row-border.order-column.dt-body-center.dataTable.no-footer')

        index = 0
        for tName in systemSubNames:
            txt = tName.get_attribute("innerText")
            print(f'Load sub system: "{txt}"')

            index += 1

        break

    return result

def main():
    driver = initDriver()
    
    pages = getPages(driver)

    data = parsePages(driver, pages)

    driver.quit()

if __name__ == '__main__':
    main()
