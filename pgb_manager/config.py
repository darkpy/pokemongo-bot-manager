import random

import re


class LineConfig(object):
    status_pattern = ' \((.+)\)$'

    def __init__(self, line, config):
        self.line = line
        self.config = config
        self.parse()

    def evaluate(self, **filters):
        for key, value in filters.items():
            if getattr(self, key, None) != value:
                return False
        return True

    def parse(self):
        pass

    def save(self, new_line):
        self.config.replace(self.line, new_line)
        self.line = new_line

    def get_status(self):
        results = re.findall(self.status_pattern, self.line)
        return results[0] if results else None

    def remove_status(self, modify=True):
        line = re.sub(self.status_pattern, '', self.line)
        self.line = line if modify else self.line
        return line

    def replace_status(self, value=''):
        self.orig_line = self.line
        line = self.remove_status(modify=False)
        if value:
            line += ' ({})'.format(value)
        self.save(line)


class Config(object):
    LineClass = LineConfig
    default_file = None

    def __init__(self, file=None):
        self.file = file or self.default_file

    def readlines(self):
        return map(lambda x: x.rstrip('\n'), open(self.file).readlines())

    def get_line_instance(self, line):
        return self.LineClass(line, self)

    def save(self, lines):
        with open(self.file, 'w') as f:
            f.write('\n'.join(lines))

    def replace(self, orig, to):
        orig = orig.line if isinstance(orig, LineConfig) else orig
        all_available = self.readlines()
        i = all_available.index(orig)
        all_available[i] = to
        self.save(all_available)

    def first_available(self):
        return self.get_line_instance(self.all_availables()[0])

    def random_available(self):
        return self.get_line_instance(random.choice(self.all_availables()))

    def all_availables(self):
        return list(filter(self.filter_available, self.readlines()))

    def filter_available(self, line):
        return True

    def filter(self, **filters):
        return list(filter(lambda x: x.evaluate(**filters), map(self.get_line_instance, self.all_availables())))
