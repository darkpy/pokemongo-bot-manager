import json
import random
import re

from pgb_manager.config import Config, LineConfig


PROXIES_FILE = 'proxies.txt'
MANAGER_CONFIG = 'manager.json'


class Proxy(LineConfig):
    def parse(self):
        self.country, rest = re.split('[0-9\-]', self.line, 1)

    def set_stopped(self):
        self.replace_status()

    def set_running(self):
        self.replace_status('running')


class Proxies(Config):
    LineClass = Proxy
    default_file = PROXIES_FILE

    def __init__(self):
        super(Proxies, self).__init__()
        self.config = json.load(open(MANAGER_CONFIG))

    def filter_available(self, line):
        return ' (running)' not in line

    def get_random_by_country(self, country):
        return random.choice(self.filter(country=country))

    def get_proxy_url(self, proxy):
        if 'PROXY_CREDENTIALS' in self.config:
            return 'http://{}@{}:80'.format(self.config['PROXY_CREDENTIALS'], proxy.line)
        return 'http://{}:80'.format(proxy.line)
