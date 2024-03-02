import requests
from bs4 import BeautifulSoup
import config
import random

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'
}


https_proxy = random.choice(config.PROXY)   
proxies = {
    'https': https_proxy
}

def get_location(url):
    try:
        response = requests.get(url=url, headers=headers, proxies=proxies)
    except requests.exceptions.ProxyError:
        return 1
    soup = BeautifulSoup(response.text, 'html')
    
    ip = soup.find('div', class_='ip').text.strip()
    location = soup.find('div', class_='value-country').text.strip()
    
    print(f'IP: {ip}\nLocation: {location}')


def main():
    get_location(url='https://2ip.ru')
    
    
if __name__ == '__main__':
    main()