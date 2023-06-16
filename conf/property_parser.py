class Properties:

    def __init__(self, file_name):
        self.file_name = file_name
        self.properties = {}
        try:
            config_open = open(self.file_name, 'r')
            for line in config_open:
                line = line.strip()
                if line.find('==') > 0 and not line.startswith('#'):
                    values = line.split('==')
                    self.properties[values[0].strip()] = values[1].strip()
        except Exception as e:
            raise e
        else:
            config_open.close()

    def has_key(self, key):
        return key in self.properties

    def get(self, key, default_value=''):
        if key in self.properties:
            return self.properties[key]
        return default_value


def parse(file_name):
    return Properties(file_name)
