import json

from pgb_manager.config import Config, LineConfig
from pgb_manager.maps import Maps

ACCOUNTS_FILE = 'accounts.txt'
JSON_TEMPLATE = 'account-config.json'
MANAGER_CONFIG = 'manager.json'
ACCOUNT_CONFIG_FILE = 'configs/{username}.json'

class Account(LineConfig):

    def parse(self):
        self.username, self.password = self.line.split(' ', 1)[0].split(':')
        splitted = self.line.split(' ')
        self.country = splitted[1]
        self.level = splitted[2]

    def set_stopped(self):
        return self.replace_status('stopped')

    def set_running(self):
        return self.replace_status('running')

    def set_finished(self):
        return self.replace_status('finished')


class Accounts(Config):
    LineClass = Account
    default_file = ACCOUNTS_FILE

    def __init__(self):
        super(Accounts, self).__init__()
        self.maps = Maps()
        self.config = json.load(open(MANAGER_CONFIG))

    def filter_available(self, line):
        return line.split(' ')[-1] not in ['(running)', '(finished)']

    def create(self, account):
        data = open(JSON_TEMPLATE).read()
        location = self.maps.get_location(account.country)
        data = data.replace('<USERNAME>', account.username).replace('<PASSWORD>', account.password).\
            replace('<LOCATION>', location).replace('<GMAP_KEY>', self.config['GMAP_KEY'])
        with open(ACCOUNT_CONFIG_FILE.format(**vars(account)), 'w') as f:
            f.write(data)

    def get(self):
        account = self.first_available()
        status = account.get_status()
        if not status:
            self.create(account)
        return account
