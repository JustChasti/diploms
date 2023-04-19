import requests
from loguru import logger


def check(server:str, port: int):
    proxy_servers = {
        'http': f'http://{server}:{port}',
        'https': f'http://{server}:{port}',
    }
    response = requests.get('https://google.com', proxies=proxy_servers)
    if response.status_code == 200:
        return True
    else:
        logger.warning(response.status_code)
        return False


print(check('163.172.182.164', 3128))
