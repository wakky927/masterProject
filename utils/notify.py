import configparser
import os

import requests


# Config Line Notify Token
conf = configparser.ConfigParser()
path = os.path.join(os.path.dirname(__file__), 'config.ini')
conf.read(path, 'UTF-8')

ACCESS_TOKEN = conf['line-notify']['access_token']


def send_message_to_line(message):
    access_token = ACCESS_TOKEN
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    data = {'message': message}
    requests.post('https://notify-api.line.me/api/notify', headers=headers, data=data)


if __name__ == '__main__':
    send_message_to_line("Test")
