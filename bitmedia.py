import re
from getcontent import get_content, replace_hashtag, edit_text, get_first_paragrapth
from datetime import datetime
import config

class BitMedia():

    def __init__(self):
        self.tags = {}

    
    #Удаление парметров
    def delete_param(self, url):
        match = re.match(r'([^?]*)\?', url)
        if match:
            return match.group(1)
        else:
            return url

    #Получение всех ссылок с категории
    def get_href(self, url):
        soup = get_content(url)
        divs = soup.find_all(class_='news-item')
        all_url = []
        for div in divs:
            found_url = div.find(class_='link-detail').find('a')
            found_url = self.delete_param(found_url['href'])

            date = div.find(class_='news-date').text
            today = datetime.now().strftime("%d.%m.%Y")
            if today == date:
                if url.endswith("/"):
                    url = url[:-1]
                found_url = url + found_url
                tags = self.get_tags_from_url(div)
                if tags == -1:
                    continue
                self.tags[found_url] = tags
                all_url.append(found_url)
        return all_url

    #Получение названия поста
    def get_title(self, soup):
        if soup == -1:
            return
        title = soup.find(class_='article-top').find('h1').text
        return title

    def get_image(self, url):
        soup = get_content(url)
        img_link = "https://bits.media" + soup.find(class_='article-picture').attrs['data-lazy-src']
        return img_link


    #Получение хэштегов
    def get_tags_from_url(self, soup):
        if soup == -1:
            return
        res = []

        tags = soup.find(class_='news-tags').find_all('a')
        include = False
        for tag in tags:
            tag = tag.text.strip(" ")
            if config.INCLUDE == "on":
                if tag in config.INCLUDE_LIST:
                    include = True
            if config.EXCLUDE != "off":
                if tag in config.EXCLUDE:
                    return -1
            if config.REPLACMENT != "":
                tag = replace_hashtag(tag)
            if tag != '':
                res.append('#' + tag.replace(" ", "_"))
        if config.SOURCE_TAG == "on":
            res.append("#Bitmedia")
        if config.INCLUDE == "on" and not include:
            return -1 
        return res

    #Получение текста со страницы
    def get_text(self, soup):
        if soup == -1:
            return
        res = soup.find(class_='articleBody').find(class_='first-p').text + '\n\n'

        paragraphs = soup.find(class_='articleBody').find_all('p', class_=False, recursive=True)
        for paragraph in paragraphs:
            #Удаление цитат
            if paragraph.find_parent(['blockquote']) is not None:
                continue
            #Удаление прочих лишних абзацев
            if 'class' not in paragraph.find_parent(['div']).attrs:
                continue
            if paragraph.find_parent(['div'])['class'][0] != 'articleBody':
                continue
            paragraph_text = ''
            for element in paragraph.contents:
                #Удаление ссылок
                if element.name == 'a':  
                    paragraph_text += element.text  
                elif isinstance(element, str):  
                    paragraph_text += element.replace("\r", "").replace("\n", "").replace("\t", "").strip(" ")
                elif element.name == 'span':
                    if 'old_tooltip' in element.attrs['class']:
                        paragraph_text += element.text

            #Удаление пустых абзацев
            if paragraph_text == "" or paragraph_text == ' ':
                continue
            res += paragraph_text + '\n\n'
        return(res)

    #Обработка длинны текста
    def edit_text(self, text, maxlen = 1000):
        text = text[0:maxlen]
        if maxlen != 1000:
            text += "...\n\n"
            return text
        #Удаление последнего неполного абзаца
        text = re.sub(r'[^\n]*$', '', text)
        return text

    #Вызов всех функций и формирование сообщения
    def get_page(self, url):
        res = {}
        soup = get_content(url)
        page = ""
        if config.HEADER != "":
            page += config.HEADER + "\n\n"
        title = self.get_title(soup)
        res['title'] = title
        page += "<b>" + title + "</b>"
        #Добавление хэштегов
        if config.HASHTAG == "on":
            page += '\n' + ", ".join(self.tags[url])
        text = self.get_text(soup)
        res['first_p'] = get_first_paragrapth(text)
        page += "\n\n" + text
        page =  edit_text(page) + "\n"
        #Добавление дополнительного текста
        if config.FIRST_TEXT != "":
            if config.FIRST_TEXT_URL == "":
                page += "\n<b>" + config.FIRST_TEXT + "</b>\n"
            else:
                page += f'\n<b><a href="{config.FIRST_TEXT_URL}">{config.FIRST_TEXT}</a></b>\n'
        if config.SECOND_TEXT != "":
            if config.SECOND_TEXT_URL == "":
                page += "\n" + config.SECOND_TEXT + "\n"
            else:
                page += f'\n<a href="{config.SECOND_TEXT_URL}">{config.SECOND_TEXT}</a>' + "\n"
        res['page'] = page
        return res
    
    def get_last_title(self, soup):
        return soup.find(class_="news-name-line").find('a').text
    
