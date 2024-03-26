import random
import requests
from bs4 import BeautifulSoup
import config

def transform_to_http_format(input_string):
    parts = input_string.split(":")
    ip = parts[0]
    port = parts[1]
    login = parts[2] if len(parts) > 2 else ""
    password = parts[3] if len(parts) > 3 else ""
    
    if login and password:
        http_formatted_string = f"http://{login}:{password}@{ip}:{port}"
    else:
        http_formatted_string = f"http://{ip}:{port}"
    
    return http_formatted_string

#Выбор случайного прокси
def get_proxy():
    proxy = random.choice(config.PROXY)   
    https_proxy = transform_to_http_format(proxy)
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
        while count_try != 3:
            proxies = get_proxy()
            try:
                response = requests.get(url=url, headers=headers, proxies=proxies)
                break
            except requests.exceptions.ProxyError:
                print("Прокси не подошла пробую другую")
                count_try += 1
    #Подключение без прокси
    else:
        response = requests.get(url, headers=headers)
    #Если ни одна прокси не подошла
    if count_try == 3:
        response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup
    else:
        return -1
