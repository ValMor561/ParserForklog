import requests
from bs4 import BeautifulSoup
import re
import config
import random

def get_proxy():
    https_proxy = random.choice(config.PROXY)   
    proxies = {
        'https': https_proxy
    }
    return proxies

def get_content(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    count_try = 0
    if config.PROXY[0] != "off":
        while count_try != 10:
            proxies = get_proxy()
            try:
                response = requests.get(url=url, headers=headers, proxies=proxies)
            except requests.exceptions.ProxyError:
                count_try += 1
            finally:
                break
    else:
        response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup
    else:
        return -1
    
def get_title(soup):
    if soup == -1:
        return
    
    title = soup.title.string
    return title

def get_tags(soup):
    if soup == -1:
        return
    res = []

    tags = soup.find(class_='post_tags_top').find_all('a')
    for tag in tags:
        res.append(tag.text.replace(" ", "_"))
    return res

def get_text(soup):
    if soup == -1:
        return
    res = ""

    paragraphs = soup.find(class_='post_content').find_all('p', class_=False, recursive=True)
    for paragraph in paragraphs:
        if paragraph.text == "":
            continue
        if paragraph.find_parent(['blockquote']) is not None:
            continue
        if paragraph.find_parent(['div'])['class'][0] != 'post_content':
            continue
        paragraph_text = ''
        for element in paragraph.contents:
            if element.name == 'a':  
                paragraph_text += element.text  
            elif isinstance(element, str):  
                paragraph_text += element 
        res += paragraph_text + '\n'
    return(res)

def edit_text(text, maxlen = 1000):
    text = text[0:maxlen]
    if maxlen != 1000:
        text += "...\n\n"
        return text
    text = re.sub(r'[^\n]*$', '', text)
    return text

def get_all():
    result = []
    for url in config.URL:
        page = ""
        soup = get_content(url)
        page += "<u><b>" + get_title(soup) + "</b></u>\n\n"
        maxlen = 1000 if  config.TEXT_LENGTH == '*' else int(config.TEXT_LENGTH)
        page += edit_text(get_text(soup), maxlen)
        if config.TEXT != "":
            page += config.TEXT + "\n"
        if config.HASHTAG == "on":
            page += ", ".join(get_tags(soup))
        result.append(page)
    return result

def main():
    url = 'https://forklog.com/news'
    soup = get_content(url)
    get_title(soup)
    get_tags(soup)
    text = get_text(soup)
    print(edit_text(text))

if __name__ == "__main__":
    main()