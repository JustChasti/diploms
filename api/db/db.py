from datetime import datetime
from time import sleep
from pymongo import MongoClient, ASCENDING
from loguru import logger
from config import base_host, base_port, client_name, selenium_hosts
from config import proxy_list, login, password, http_port
from db.state_machine import StateMachine
from modules.decorators import default_decorator


while True:
    try:
        client = MongoClient(
            base_host, base_port
        )[client_name]
        users = client['users']
        tasks = client['tasks']
        hosts = client['hosts']
        proxies = client['proxy']
        break
    except Exception as e:
        logger.exception(e)
        sleep(5)


def set_default_proxies():
    for i in proxy_list:
        proxies.update_one(
            filter={'address': i},
            update={"$set": {
                'address': i,
                'port': http_port,
                'in_use': False,
                'login': login,
                'password': password,
                'last_used': datetime.now(),
                'active': True,
                'ban_list': []  # ['user_id_1',..., 'user_id_n']
            }},
            upsert=True
        )


def create_host_list():
    for i in selenium_hosts:
        hosts.update_one(
            filter={'hostname': i},
            update={"$set": {
                'hostname': i,
                'locked': False
            }},
            upsert=True
        )

    StateMachine.add_states(selenium_hosts)
    for host in StateMachine.hosts:
        logger.info(host['hostname'])
        logger.warning(host['open'])


@default_decorator(errormessage='error in finding proxy')
def get_available_proxy(user_id):
    unused = proxies.find(filter={
        'in_use': False,
        'active': True
    })
    if unused:
        for i in unused:
            if user_id not in i['ban_list']:
                proxies.update_one({'_id': i['_id']}, {'$set':{'in_use': True}})
                return {'address': i['address'], 'login': i['login'], 'password': password}
    used = proxies.find(filter={
        'in_use': True,
        'active': True,
    }).sort('last_used', ASCENDING)
    if used:
        for i in used:
            if user_id not in i['ban_list']:
                proxies.update_one({'_id': i['_id']}, {'$set':{'last_used': datetime.now()}})
                return {'address': i['address'], 'login': i['login'], 'password': password}
    return {'address': '', 'login': '', 'password': ''}


@default_decorator(errormessage='error in banning user')
def ban_user_proxy(user_id, address):
    proxy = proxies.update_one(
        filter={
            'address': address
        },
        update={
            '$push':{
                'ban_list': user_id
            }
        }
    )
    if proxy:
        return {'info': 'that proxy are now at ban 4 you'}
    else:
        return {'info': 'no proxy with that address'}
    
