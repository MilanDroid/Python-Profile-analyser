# -*- coding: utf-8 -*-

from apps.registers import Registers


class Industries(object):

    def __init__(self, folder, filename):
        self.register = Registers()
        self.filename = folder + "Industries/" + filename
        self.content = []

    def start(self):
        self.content = self.register.get_data(self.filename, 'industry', 3)
