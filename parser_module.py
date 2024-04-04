import config
from getcontent import get_content
from forklog import ForkLog
from bitmedia import BitMedia
def choise_module(url):
    if "https://forklog.com" in url:
        return ForkLog()
    elif "https://bits.media" in url:
        return BitMedia()

#Получение времени последнего поста
def get_title():
    res = "Названия последних постов:\n"
    for url in config.URL:
        PM = choise_module(url)
        soup = get_content(url)
        title = PM.get_last_title(soup)
        res += f'{url} - {title}\n'
    return res
