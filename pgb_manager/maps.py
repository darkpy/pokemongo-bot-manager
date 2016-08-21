from pgb_manager.config import Config, LineConfig

MAPS_FILE = 'maps.txt'


class Map(LineConfig):
    def parse(self):
        self.country, self.location = self.line.split(':')


class Maps(Config):
    LineClass = Map
    default_file = MAPS_FILE

    def get_location(self, country):
        return self.filter(country=country)[0].location
