import os
from dotenv import load_dotenv

load_dotenv()

# test-acc gray, qwerty, 645b8f50b2f1111db4e60947

admin_password = 'Qwerty21'
my_host = '0.0.0.0'
base_host = 'mongodb'
base_port = 27017
client_name = 'balancer'
login = 'chastinescape'
password = 'PiLHz9R28T'
encrypt_salt = b'$2b$08$yINtjjwcwMuOCM6/tHITRO'

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 1
REFRESH_TOKEN_EXPIRE_DAYS = 60

http_port = 59100
rabbit_host = 'rabbitmq'
queue_tasks_name = 'tasks'

selenium_hosts = (
    'chrome1',
    'chrome2'
)

page_load_timeout = 15
page_dir = 'files'
