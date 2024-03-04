import requests
from bs4 import BeautifulSoup
import re
import config
import random
import bd

#Выбор случайного прокси
def get_proxy():
    https_proxy = random.choice(config.PROXY)   
    proxies = {
        'https': https_proxy
    }
    return proxies

#Получение информации на странице
def get_content(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    count_try = 0
    if config.PROXY[0] != "off":
        #Перебор прокси если не получилось подключиться
        while count_try != 10:
            proxies = get_proxy()
            try:
                response = requests.get(url=url, headers=headers, proxies=proxies)
            except requests.exceptions.ProxyError:
                count_try += 1
            finally:
                break
    #Подключение без прокси
    else:
        response = requests.get(url, headers=headers)
    #Если ни одна прокси не подошла
    if count_try == 10:
         response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup
    else:
        return -1

#Получение всех ссылок с категории
def get_href(soup):
    divs = soup.find_all(class_='post_item')
    all_url = []
    for div in divs:
        url = div.find('a')
        all_url.append(url['href'])
    return all_url

#Получение названия поста
def get_title(soup):
    if soup == -1:
        return
    
    title = soup.title.string
    return title

#Получение хэштегов
def get_tags(soup):
    if soup == -1:
        return
    res = []

    tags = soup.find(class_='post_tags_top').find_all('a')
    for tag in tags:
        res.append(tag.text.replace(" ", "_"))
    return res

#Получение текста со страницы
def get_text(soup):
    if soup == -1:
        return
    res = ""

    paragraphs = soup.find(class_='post_content').find_all('p', class_=False, recursive=True)
    for paragraph in paragraphs:
        #Удаление пустых абзацев
        if paragraph.text == "":
            continue
        #Удаление цитат
        if paragraph.find_parent(['blockquote']) is not None:
            continue
        #Удаление прочих лишних абзацев
        if paragraph.find_parent(['div'])['class'][0] != 'post_content':
            continue
        paragraph_text = ''
        for element in paragraph.contents:
            #Удаление ссылок
            if element.name == 'a':  
                paragraph_text += element.text  
            elif isinstance(element, str):  
                paragraph_text += element 
        res += paragraph_text + '\n'
    return(res)

#Обработка длинны текста
def edit_text(text, maxlen = 1000):
    text = text[0:maxlen]
    if maxlen != 1000:
        text += "...\n\n"
        return text
    #Удаление последнего неполного абзаца
    text = re.sub(r'[^\n]*$', '', text)
    return text

#Вызов всех функций и формирование сообщения
def get_page(url):
    soup = get_content(url)
    page = ""
    page += "<u><b>" + get_title(soup) + "</b></u>\n\n"
    page += edit_text(get_text(soup), config.TEXT_LENGTH)
    #Добавление дополнительного текста
    if config.TEXT != "":
        page += config.TEXT + "\n"
    #Добавление хэштегов
    if config.HASHTAG == "on":
        page += ", ".join(get_tags(soup))
    return page
