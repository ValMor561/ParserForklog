import configparser

def get_config(filename):
    config = configparser.ConfigParser()
    config.read(filename)

    return config

def get_multiple_values(param):
    if ".txt" in param:
        with open(param, 'r') as file:
            lines = file.readlines()
            lines = [line.strip() for line in lines]
            return lines
    return param.split('\n')

config = get_config('config.ini')
BOT_TOKEN = config['DEFAULT']['bot_token']
CHANEL_ID = config['DEFAULT']['channels_id']
ADMINS = config['DEFAULT']['admins']
PROXY = get_multiple_values(config['PROXY']['proxy'])
WORK_DAYS = config['SETTINGS']['work_days']
WORK_START_TIME = config['SETTINGS']['work_start_time']
WORK_END_RIME = config['SETTINGS']['work_end_time']
WORK_TIME = config['SETTINGS']['work_time']
WORK_PERIOD = config['SETTINGS']['work_period']
URL = get_multiple_values(config['MESSAGE']['URL'])
HASHTAG = config['MESSAGE']['hashtag']
TEXT = config['MESSAGE']['text']
TEXT_LENGTH = config['MESSAGE']['text_length']