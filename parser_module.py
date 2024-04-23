import config
from getcontent import get_content
from forklog import ForkLog
from bitmedia import BitMedia
from coindesk import CoinDesk

def choise_module(url):
    if "https://forklog.com" in url:
        return ForkLog()
    elif "https://bits.media" in url:
        return BitMedia()
    elif "https://www.coindesk.com" in url:
        return CoinDesk()
    
#Получение времени последнего поста
def get_title():
    res = "Названия последних постов:\n"
    for url in config.URL:
        PM = choise_module(url)
        soup = get_content(url)
        title = PM.get_last_title(soup)
        res += f'{url} - {title}\n'
    return res
