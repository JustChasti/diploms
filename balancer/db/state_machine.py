from loguru import logger


class StateMachine(object):
    __instance = None
    hosts = []

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(StateMachine, cls).__new__(cls)

    @classmethod
    def getInstance(cls):
        if not cls.__instance:
            cls.__instance = StateMachine()
        return cls.__instance

    @classmethod
    def add_states(cls, hosts: list):
        for host in hosts:
            cls.hosts.append({
                'hostname': host,
                'open': True
            })

    @classmethod
    def set_state(cls, host_name: str, open: bool):
        for host in cls.hosts:
            if host['name'] == host_name:
                host['open'] = open
                return {'succes': True}
        return {'succes': False}

    @classmethod
    def get_state(cls):
        for host in cls.hosts:
            if host['open'] is True:
                return host
        return None
