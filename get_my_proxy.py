# https://hidemy.name/ru/proxy-list/?maxtime=1000&type=h#list
from random import choice

def get_useregent_list():
    useragents = open('useragent.list').read().split('\n')
    return choice(useragents)


def get_proxies_list():
    proxies = open('proxies.list').read().split('\n')
    return choice(proxies)
