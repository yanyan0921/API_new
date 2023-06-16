import configparser
from pathlib import Path
import os


class ConfigLoader:

    def __init__(self, name):
        self.parser = configparser.ConfigParser()
        file_path = Path(__file__).parent.resolve()
        self.config_file = os.path.join(str(file_path), name + ".cfg")
        self.parser.read(self.config_file)

    def get_sections(self):
        return self.parser.sections()

    def get_setting_endpoint(self):
        return self.parser.items("endpoint")

    def get_setting_additional_properties(self):
        return self.parser.items("additionalProperties")

    def get_setting(self, section, item):
        try:
            return self.parser.get(section, item)
        except Exception as e:
            print('read config excepiton:' + str(e))
