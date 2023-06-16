import os
from configparser import ConfigParser
from pathlib import Path


class ConfigLoader:
    parser = ConfigParser()
    path = Path(__file__).parent.resolve()
    file = None

    def __init__(self, *args):
        self.file = os.path.join(str(self.path), args[0] + ".cfg")
        self.parser.read(self.file)

    def get_setting(self, section, item):
        try:
            return self.parser.get(section, item)
        except Exception as e:
            print('read config exception: ' + str(e))
