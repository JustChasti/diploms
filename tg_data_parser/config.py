import os
from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv('TG_ID')
api_hash = os.getenv('TG_HASH')

# mongodb
base_host = 'mongo'
base_port = 27017
client_name = 'data_parser'

# elasticsearch

keywords_count = 3
elastic_index = 'articles'
elastic_host = 'http://elasticsearch:9200'

# telegram channels /betta
channels = (
    'https://t.me/habr_com',
    'https://t.me/d_code',
    'https://t.me/exploitex'
)

# delay 4 crawler
my_host = '0.0.0.0'
get_info_delay = 60  # in minutes
