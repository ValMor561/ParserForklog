import re
import config
from getcontent import get_content, replace_hashtag, edit_text, get_first_paragrapth
from datetime import datetime

class ForkLog():
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
        divs = soup.find_all(class_='post_item')
        all_url = []
        for div in divs:
            url = div.find('a')
            url = self.delete_param(url['href'])

            date = div.find(class_='post_date').text
            today = datetime.now().strftime("%d.%m.%Y")
            if today == date:
                all_url.append(url)
        return all_url

    #Получение названия поста
    def get_title(self, soup):
        if soup == -1:
            return
        
        title = soup.title.string
        return title
    
    def get_image(self, url):
        soup = get_content(url)
        img_link = soup.find(class_='article_image_mob').find('img').attrs['src']
        return img_link

    #Получение хэштегов
    def get_tags(self, soup):
        if soup == -1:
            return
        res = []
        
        
        tags = soup.find(class_='post_tags_top').find_all('a')
        include = False
        for tag in tags:
            if config.INCLUDE == "on":
                if tag.text.replace('#', '') in config.INCLUDE_LIST:
                    include = True
            if config.EXCLUDE != "off":
                if tag.text.replace('#', '') in config.EXCLUDE:
                    return -1
            if config.REPLACMENT != "":
                tag = replace_hashtag(tag.text.replace('#', ''))
                if tag != '':
                    res.append("#" + tag.replace(" ", "_"))
        if config.SOURCE_TAG == "on":
            res.append("#Forklog")
        if config.INCLUDE == "on" and not include:
            return -1     
        return res

    #Получение текста со страницы
    def get_text(self, soup):
        if soup == -1:
            return
        res = ""

        paragraphs = soup.find(class_='post_content').find_all('p', class_=False, recursive=True)
        for paragraph in paragraphs:
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
                elif element.name == 'span':
                    if 'old_tooltip' in element.attrs['class']:
                        paragraph_text += element.text

            #Удаление пустых абзацев
            if paragraph_text == "" or paragraph_text == ' ':
                continue
            res += paragraph_text + '\n\n'
        return(res)

    #Вызов всех функций и формирование сообщения
    def get_page(self, url):
        res = {}
        soup = get_content(url)
        page = ""
        if config.HEADER != "":
            page += config.HEADER + "\n\n"
        title = self.get_title(soup)
        res ['title'] = title
        page += "<b>" + title + "</b>"
        #Добавление хэштегов
        if config.HASHTAG == "on":
            tags = self.get_tags(soup)
            if tags == -1:
                return -1
            page += '\n' + ", ".join(tags)
        text = self.get_text(soup)
        res['first_p'] = get_first_paragrapth(text)
        page += "\n\n" + text
        page = edit_text(page) + "\n"
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
        return soup.find(class_="text_blk").find('p').text
