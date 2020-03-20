# -*- coding: utf-8 -*-

from apps.registers import Registers


class Countries(object):

    def __init__(self, folder, filename):
        self.register = Registers()
        self.filename = folder + "Countries/" + filename
        self.content = []

    def start(self):
        self.content = self.register.get_data(self.filename, "countries", 3)

    def clean(self):
        for country in self.content:
            country[2] = country[2].replace(',', '')
            country[2] = country[2].replace('.00', '')
