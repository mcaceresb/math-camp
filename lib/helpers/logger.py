import sys


class Logger(object):
    def __init__(self, logfile = None, logonly = False):
        self.logonly = logonly
        if not self.logonly:
            self.terminal = sys.stdout
        self.log = open(logfile if logfile else 'log.log', "w")

    def write(self, message):
        if not self.logonly:
            self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass
