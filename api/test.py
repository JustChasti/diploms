import requests
from loguru import logger
from requests.auth import HTTPProxyAuth


login = 'chastinescape'
password = 'PiLHz9R28T'


def check(server:str, port: int):
    session = requests.Session()
    proxy_servers = {
        'http': f'http://{login}:{password}@{server}:{59100}',
        'https': f'http://{login}:{password}@{server}:{59100}',
    }
    session.proxies = proxy_servers
    auth = HTTPProxyAuth(login, password)
    session.auth = auth
    try:
        response = session.get('https://google.com', timeout=10)
        if response.status_code == 200:
            return True
        else:
            logger.warning(response.status_code)
            return False
    except Exception as e:
        return False
    

print(check('185.231.244.160', 59100))
