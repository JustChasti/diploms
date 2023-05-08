import os
from dotenv import load_dotenv


load_dotenv()

login = os.getenv('LOGIN')
password = os.getenv('PASSWORD')

proxy_list = {
    '185.231.244.160',
    '185.231.244.178',
    '185.231.244.69',
    '185.231.244.181',
    '185.231.244.222',
    '185.231.244.132',
    '185.231.244.142',
    '185.231.244.141',
    '185.231.244.143',
    '185.231.244.146'
}

http_port = 59100
