import os
class os_adapter(object):
    os = ''
    def __init__(self):
        self.os = os.name

    def fopen(self, filename):
        dir_list = filename.strip.split('\\')

