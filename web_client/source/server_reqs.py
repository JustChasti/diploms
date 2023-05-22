import requests
from config import server_host
from source.decorators import default_decorator


@default_decorator
def sign_in(username, password):
    data = {
        'username': username,
        'password': password
    }
    respone = requests.post(f'{server_host}/login', json=data)
    data = respone.json()
    if data['access_token'] and data['refresh_token']:
        return (data['access_token'], data['refresh_token'])
    else:
        return False
    

@default_decorator
def sign_up(username, password):
    data = {
        'username': username,
        'password': password
    }
    respone = requests.post(f'{server_host}/add_user', json=data)
    data = respone.json()['tokens']
    if data['access_token'] and data['refresh_token']:
        return (data['access_token'], data['refresh_token'])
    else:
        return False


@default_decorator
def get_user_info(access_token, refresh_token):
    try:
        respone = requests.get(f'{server_host}/user_info/{access_token}')
        data = {
            'username': respone.json()['username'],
            'id': respone.json()['id'],
            'count_tasks': respone.json()['count_tasks'],
            'count_banned_proxies': respone.json()['count_banned_proxies'],
            'count_max_proxies': respone.json()['count_max_proxies']
        }
        return (data,)
    except Exception as e:
        try:
            data = {
                'refresh_token': refresh_token,
            }
            respone = requests.get(f'{server_host}/refresh', json=data)
            token = respone.json()['access_token']
            respone = requests.get(f'{server_host}/user_info/{token}')
            data = respone.json()['username']
            data = {
                'username': respone.json()['username'],
                'id': respone.json()['id'],
                'count_tasks': respone.json()['count_tasks'],
                'count_banned_proxies': respone.json()['count_banned_proxies'],
                'count_max_proxies': respone.json()['count_max_proxies']
            }
            return (data, token)
        except Exception as e:
            return False
