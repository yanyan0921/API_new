class PropertyLoader:
    properties = {}

    def __init__(self, *args):
        with open(args[0], encoding='utf8') as f:
            for line in f:
                line = line.strip()
                if len(line) != 0 and line.find('='):
                    pairs = line.split('=')
                    self.properties[pairs[0].strip()] = pairs[1].strip()

    def get_property(self, key):
        return self.properties.get(key)
