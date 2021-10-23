from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import re 
import bs4 

REGEX_ROWS = ("<tr><td>(.+?)</td><td>(.+?)</td><td>(.+?)</td><td>(.+?)</td><td>(.+?)</td></tr>") 

# Т.к. страница имеет артефакты в структуре HTML, забираем фикшеную версию
s =  Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)
driver.minimize_window()
driver.get('http://lib.ru/HITPARAD/hitlast1000.txt')
html = driver.page_source
driver.quit()

def parseBS4(html):
    result = []

    soup = bs4.BeautifulSoup(html, features="html.parser")
    tables = soup.find_all("table", width='100%')
    
    if not tables:
        raise Exception(f"На странице нет подходящих таблиц")

    for t in tables:
        rows = t.find_all("tr")

        if not rows or len(rows) == 0:
            raise Exception(f"Ошибка с поиском данных в элементе {t.text}")

        for r in rows:
            cells = r.find_all("td")

            if not cells or len(cells) == 0:
                raise Exception(f"Ошибка с поиском данных в элементе {t.text}")
                
            num,author,name,_,_ = cells

            # print(num.text, author.text, name.text, sep='\t')
            result.append([num.text, author.text, name.text])
    
    return result


def parseRegex(html): 
    line = html.replace('\n','')   
    return regexParseLine(line)


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


"""Web Server"""

from flask import Flask, render_template

app = Flask(__name__) 

@app.route('/')
def page_index():
    return render_template('index.html') 

@app.route('/bs4')
def page_bs4():
    return render_template('bs4.html', data=parseBS4(html)) 

@app.route('/regex')
def page_regex():
    return render_template('regex.html', data=parseRegex(html)) 


# res = parseBS4(html)
# for r in res:
#     print(r)

# res = parseRegex(html)
# for r in res:
#     print(r)

if __name__ == "__main__": 
    app.run(port=5000)
