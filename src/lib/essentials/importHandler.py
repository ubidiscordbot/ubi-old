class ImportHandler:
    def __init__(self):
        self.imports = [[], []]

    def add(self, payload, name):
        self.imports[0].append(payload)
        self.imports[1].append(name)

    def get(self):
        return self.imports

    def has(self, name):
        if name in self.imports[1]:
            return True
        else:
            return False