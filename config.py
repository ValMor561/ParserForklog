import configparser

#Чтение конфигурационного файла
def get_config(filename):
    config = configparser.ConfigParser()
    config.read(filename, encoding="utf-8")

    return config

#Функция для считывания значений из файла если он указан в качестве параметра, либо из .ini файла
#На вход подается значение хранящееся в конфиге
def get_multiple_values(param):
    if ".txt" in param:
        with open("/var/www/crypto/news_forklog/"+param, 'r') as file:
            lines = file.readlines()
            lines = [line.strip() for line in lines]
            return lines
    return param.replace(" ", "").split(',')

all_week_days = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
config = get_config('/var/www/crypto/news_forklog/config.ini')

#Глобальные переменные всех параметров
BOT_TOKEN = config['DEFAULT']['bot_token']
CHANELLS_ID = config['DEFAULT']['channels_id'].replace(" ", "").split(",")
ADMINS = config['DEFAULT']['admins'].replace(" ", "").split(",")
PROXY = get_multiple_values(config['PROXY']['proxy'])
WORK_DAYS = all_week_days if config['SETTINGS']['work_days'] == '*' else config['SETTINGS']['work_days'].split(", ")
WORK_START_TIME = config['SETTINGS']['work_start_time']
WORK_END_RIME = config['SETTINGS']['work_end_time']
WORK_TIME = config['SETTINGS']['work_time'].split(',')
WORK_PERIOD = config['SETTINGS']['work_period']
URL = get_multiple_values(config['MESSAGE']['URL'])
HASHTAG = config['MESSAGE']['hashtag']
TEXT = config['MESSAGE']['text']
TEXT_URL = config['MESSAGE']['text_url']
TEXT_LENGTH = 1000 if config['MESSAGE']['text_length'] == '*' else int(config['MESSAGE']['text_length'])
HOST=config['BD']['host']
DATABASE=config['BD']['database']
USER=config['BD']['user']
PASSWORD=config['BD']['password']
TABLENAME=config['BD']['tablename']
