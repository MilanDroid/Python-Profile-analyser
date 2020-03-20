# -*- coding: utf-8 -*-

from apps.registers import Registers


class Roles(object):

    def __init__(self, folder, filename):
        self.register = Registers()
        self.filename = folder + "Roles/" + filename
        self.content = []

    def start(self):
        self.content = self.register.get_data(self.filename, 'rol', 3)
