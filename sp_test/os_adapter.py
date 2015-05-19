import os
class os_adapter(object):
    os = ''
    def __init__(self):
        self.os = os.name
        self.sep = os.sep

    def fopen(self, filename):
        if self.os == 'nt':
            sep = '\\'
        dir_list = filename.strip.split('\\')


