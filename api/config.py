import os
from dotenv import load_dotenv

load_dotenv()

# test-acc gray, qwerty, 645b8f50b2f1111db4e60947

admin_password = 'Qwerty21'
my_host = '0.0.0.0'
base_host = 'mongo'
base_port = 27017
client_name = 'balancer'
login = os.getenv('LOGIN')
password = os.getenv('PASSWORD')
encrypt_salt = b'$2b$08$yINtjjwcwMuOCM6/tHITRO'

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
rabbit_host = 'rabbitmq'
queue_tasks_name = 'tasks'

selenium_hosts = (
    'chrome1',
    'chrome2'
)

page_load_timeout = 15
page_dir = 'files'
