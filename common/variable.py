class Variable:

    def __init__(self):
        self.vars = {}

    def clear(self):
        self.vars = {}

    def put(self, key, value):
        self.vars[key] = value

    def get(self, key):
        if key in self.vars.keys():
            return self.vars.get(key)
        else:
            return ""
