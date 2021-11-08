class Debugger():
    LEVELS = {'S': 0, 'D': 1, 'E': 2}

    def __init__(self, lvl=0):
        self.lvl =lvl

    def set_level(self, level):
        if level:
            self.lvl = self.LEVELS[level[0].upper()]

    def log(self, log, level):
        if self.LEVELS[level[0].upper()] >= self.lvl:
            print('{}/{}: {}'.format(level[0].upper(), self.__name__, log))
