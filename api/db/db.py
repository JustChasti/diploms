from pymongo import MongoClient
from loguru import logger
from config import base_host, base_port, client_name, selenium_hosts, proxy_list
from time import sleep
from db.state_machine import StateMachine


while True:
    try:
        client = MongoClient(
            base_host, base_port
        )[client_name]
        users = client['users']
        tasks = client['tasks']
        hosts = client['hosts']
        proxy = client['proxy']
        break
    except Exception as e:
        logger.exception(e)
        sleep(5)


def set_default_proxies():
    for i in proxy_list:
        proxy.update_one(
            filter={'address': i},
            update={"$set": {
                'address': i,
                'in_use': False,
                'users': []
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
