import re
import config
from getcontent import get_content, replace_hashtag, edit_text, translate_text
from datetime import datetime

class CoinDesk():
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
        divs = soup.find_all(class_='side-cover-card')
        all_url = []
        for div in divs:
            url = div.find('a')
            url = self.delete_param(url['href'])
            
            date = div.find(class_='eeyqKG').find('span').text
            today = datetime.today().strftime('%B %d, %Y')
            if today == date:
                all_url.append(f"https://www.coindesk.com{url}")
        return all_url

    #Получение названия поста
    def get_title(self, soup):
        if soup == -1:
            return
        
        title = soup.title.string
        return title
    
    def get_image(self, url):
        soup = get_content(url)
        img_link = soup.find(class_="ftMzOf").find('picture').find('img').attrs['src']
        return img_link

    #Получение хэштегов
    def get_tags(self, soup):
        if soup == -1:
            return
        res = []
        
        tags = soup.find(attrs={"data-module-name": "article-tags-module"})
        if tags:
            tags = tags.find_all('a')
        else:
            return res
        for tag in tags:
            tag_text = tag.find('span').text.replace('#', '').strip()
            if config.EXCLUDE != "off":
                if tag_text in config.EXCLUDE:
                    return -1
            if config.REPLACMENT != "":
                tag = replace_hashtag(tag_text)
                if tag != '':
                    res.append("#" + tag.replace(" ", "_"))
            
        return res

    #Получение текста со страницы
    def get_text(self, soup):
        if soup == -1:
            return
        res = ""
        res += soup.find(attrs={"data-module-name": "article-header"}).find('h2').text + "\n"
        paragraphs = soup.find(attrs={"data-module-name": "article-body"}).find_all('p', class_=False, recursive=True)
        for paragraph in paragraphs:
            #Удаление цитат
            if paragraph.find_parent(['blockquote']) is not None:
                continue
            if 'read more' in paragraph.text.lower() or 'see also' in paragraph.text.lower() or 'newsletter here' in paragraph.text.lower():
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
            res += paragraph_text.strip() + '\n\n'
        res = translate_text(res)
        return(res)

    #Вызов всех функций и формирование сообщения
    def get_page(self, url):
        soup = get_content(url)
        if soup == -1:
            return -1
        page = ""
        if config.HEADER != "":
            page += config.HEADER + "\n\n"
        page += "<b>" + translate_text(self.get_title(soup)) + "</b>"
        #Добавление хэштегов
        if config.HASHTAG == "on":
            tags = self.get_tags(soup)
            if tags == -1:
                return -1
            if len(tags) > 0:
                page += '\n' + ", ".join(tags)
        page += "\n\n" + self.get_text(soup)
        page = edit_text(page)
        #Добавление дополнительного текста
        if config.TEXT != "":
            if config.TEXT_URL == "":
                page += config.TEXT + "\n"
            else:
                page += f'<a href="{config.TEXT_URL}">{config.TEXT}</a>' + "\n"    
        return page
    
    def get_last_title(self, soup):
        return soup.find(class_="side-cover-card").find('h4').text

