import requests
from time import sleep
from datetime import datetime
from random import randint
from loguru import logger
from requests.auth import HTTPProxyAuth
from config import login, password
from db.db import proxies
from modules.decorators import default_decorator


def check(server:str, port: int):
    session = requests.Session()
    logger.info(f'http://{login}:{password}@{server}:{port}')
    proxy_servers = {
        'http': f'http://{login}:{password}@{server}:{port}',
        'https': f'http://{login}:{password}@{server}:{port}',
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
        logger.exception(e)
        return False


def proxy_daemon():
    while True:
        minutes = randint(60, 120)
        try:
            all_proxie = proxies.find({})
            for i in all_proxie:
                logger.info(f"{i['address']} {i['port']} {i['in_use']} {i['active']}")
                result = check(i['address'], i['port'])
                if result:
                    proxies.update_one(filter={'_id': i['_id']}, update={'$set': {'active':True}})
                else:
                    proxies.update_one(filter={'_id': i['_id']}, update={'$set': {'active':False}})
                    logger.warning(i['address'])
            sleep(60*minutes)
        except Exception as e:
            logger.exception(e)
            sleep(60*minutes)


@default_decorator('cant add this proxy')
def add_new_proxy(address, port):
    result = check(address, port)
    if result:
        proxies.insert_one({
            'address': address,
            'port': port,
            'in_use': False,
            'login': '',
            'password': '',
            'last_used': datetime.now(),
            'active': True,
            'ban_list': []
        })
        return {'info': f'proxy {address}:{port} added'}
    else:
        return {'info': f'proxy {address}:{port} cannot provide a stable connection'}
