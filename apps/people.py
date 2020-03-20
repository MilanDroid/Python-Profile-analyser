# -*- coding: utf-8 -*-

from apps.registers import Registers


class People(object):

    def __init__(self, folder, filename):
        self.register = Registers()
        self.filename = folder + "People/" + filename
        self.content = []
    
    def start(self):
        self.content = self.register.get_data(self.filename, 'person', 8)

    def file_out(self, out_list, folder):
        filename = folder + "People/people.out"
        f = open(filename, "w")

        for row in out_list:
            line = str(row[0]) + "\n"
            f.write(line)
