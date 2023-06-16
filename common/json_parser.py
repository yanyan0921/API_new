import json


class JsonParser:

    def __init__(self, path):
        self.json_str = open(path)

    def load(self):
        return json.load(self.json_str)
