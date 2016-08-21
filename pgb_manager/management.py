import json
import subprocess

from pgb_manager.accounts import Accounts
from pgb_manager.proxies import Proxies

MANAGER_CONFIG = 'manager.json'
COMMAND = ['sleep', '10']


class Management(object):
    def __init__(self):
        self.accounts = Accounts()
        self.proxies = Proxies()
        self.config = json.load(open(MANAGER_CONFIG))

    def start(self):
        account = self.accounts.get()
        proxy = self.proxies.get_random_by_country(account.country)
        account.set_running()
        proxy.set_running()
        try:
            p = subprocess.Popen(self.config.get('COMMAND', COMMAND), env=self.get_environment(proxy))
            p.wait()
        except KeyboardInterrupt:
            pass
        self.exit(account, proxy)

    def exit(self, account, proxy):
        account.set_stopped()
        proxy.set_stopped()

    def get_environment(self, proxy):
        proxy = self.proxies.get_proxy_url(proxy)
        return {'HTTP_PROXY': proxy, 'HTTPS_PROXY': proxy}