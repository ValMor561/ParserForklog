import requests
from bs4 import BeautifulSoup
import re

def get_content(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
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
    print(title)
    return title

def get_tags(soup):
    if soup == -1:
        return
    res = []

    tags = soup.find(class_='post_tags_top').find_all('a')
    for tag in tags:
        print(tag.text)
        res.append(tag.text.replace("#",""))
    print(res)
    return res

def get_text(soup):
    if soup == -1:
        return
    res = ""

    paragraphs = soup.find(class_='post_content').find_all('p', class_=False, recursive=True)
    for paragraph in paragraphs:
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
    print(res)
    return(res)

def edit_text(text, maxlen = 1000):
    text = text[0:maxlen]
    if maxlen != 1000:
        text += "..."
        return text
    text = re.sub(r'[^\n]*$', '', text)
    return text
    
def main():
    url = 'https://forklog.com/news/sutochnyj-pritok-v-bitkoin-etf-dostig-rekordnyh-673-mln'
    soup = get_content(url)
    get_title(soup)
    get_tags(soup)
    text = get_text(soup)
    print(edit_text(text))

if __name__ == "__main__":
    main()