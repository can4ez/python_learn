# Решение КТ4
# Вар. 3: http://lib.ru/HITPARAD/hitlast1000.txt

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
URL = r'http://lib.ru/HITPARAD/hitlast1000.txt'
# Сделаем путь для кеширвоания данных
# в идеале нужно немного доработать
# в конкретной ситуации в этом нет необходимости
CACHED_FOLDER = f'{SCRIPT_PATH}\\Cached'
CACHED_FILE = f'{CACHED_FOLDER}\\{Path(URL).name}.html'

REGEX_ROWS = ("<tr><td>(.+?)</td><td>(.+?)</td><td>(.+?)</td><td>(.+?)</td><td>(.+?)</td></tr>") 

def cache_html(driver, url): 
    """
    Будем хорошими людьми, обойдемся без постоянных запросов к серверу
    (актуально на этапе тестирования, но почему бы не вынести в фу-ю ☺)
    Также пригодится для парсинга через Regex
    """
    if os.path.isfile(CACHED_FILE):
        # Если файл недавно кеширован, то вернем True
        if datetime.datetime.now().timestamp() - os.path.getmtime(CACHED_FILE) < 180:
            return True

    driver.get(url)

    # Чтобы точно прогрузилась страница
    sleep(2)

    try:
        print(f'Try cached url("{url}") to file "{CACHED_FILE}"')
        with open(CACHED_FILE, 'w', encoding='UTF-8') as f: 
            if f.write(driver.page_source) > 0: 
                return True
    except Exception as e:
        print(e)

    return False

def getData(driver, url): 
    print(f'Get data info from url: "{url}"')

    driver.get(url)

    sleep(2)

    tables = driver.find_elements(By.CSS_SELECTOR, "table[width='100%']")

    if tables is None:
        raise Exception(f"На странице нет подходящей таблицы")

    c = 1

    for t in tables:
        rows = t.find_elements(By.CSS_SELECTOR, "tr")
        if rows is None or len(rows) == 0:
            raise Exception(f"Ошибка с поиском данных в элементе {t.text}")

        print(f"Таблица #{c}")

        for row in rows:
            cells = row.find_elements(By.CSS_SELECTOR, "td")
            
            if cells is None or len(cells) == 0:
                raise Exception(f"Ошибка с поиском данных в элементе {t.text}")
                
            num,author,name,_,_ = cells

            print(num.text, author.text, name.text, sep='\t')

        c += 1

def initDriver():
    Path(CACHED_FOLDER).mkdir(parents=True, exist_ok=True)

    s =  Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    driver.minimize_window()

    return driver

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def regexParseLine(line):
    matches = re.finditer(REGEX_ROWS, line)
    print(matches)
    
    books = []

    for _, match in enumerate(matches, start=1):
        books.append(match.groups())
    
    # Это наверняка можно как-то сделать красивее, но уже устал...
    res = []
    for x in books:
        r = []
        for a in x:
            r.append(striphtml(a))

        res.append(r)

    return res  

def getDataFromUrl(url):
    try:
        resp = get(url=url)
        if not resp:
            raise Exception(f"Сервер вернул код статуса HTTP: {resp.status_code}")
    except Exception as e:
        print(e)
        return False

    return resp.text

def getDataRegex(url, web = False):
    result = []

    if web == True:
        data = getDataFromUrl(url, web)
        print(data)
        
        if data == False:
            raise Exception(f"Нет данных для обработки")
                    
        lines = data.split('\n')

        for line in lines:
            result.append(regexParseLine(line))
    else :
        try:
            with open(url, 'r', encoding='UTF-8') as f:
                line = f.read().replace('\n','')
                res = regexParseLine(line)
                for r in res:
                    print(r[0],r[1],r[2],r[3],r[4],sep='\t')
        except Exception as e:
            print(e) 

def main():
    driver = initDriver()

    if cache_html(driver, URL) != False:
        print(f'Open cached file "{CACHED_FILE}"')
        getData(driver, CACHED_FILE)
        # getDataRegex(CACHED_FILE)
    else :
        print('Error cahe file, go to origin url...')
        getData(driver, URL)

    driver.quit()

if __name__ == '__main__':
    main()
