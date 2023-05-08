import requests
from loguru import logger
from requests.auth import HTTPProxyAuth
from config import login, password


def check(server:str, port: int):
    session = requests.Session()
    proxy_servers = {
        'http': f'http://{login}:{password}@{server}:{port}',
        'https': f'http://{login}:{password}@{server}:{port}',
    }
    session.proxies = proxy_servers
    auth = HTTPProxyAuth(login, password)
    session.auth = auth
    try:
        response = session.get('https://google.com')
        if response.status_code == 200:
            return True
        else:
            logger.warning(response.status_code)
            return False
    except Exc as e:
        return False
