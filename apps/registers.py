# -*- coding: utf-8 -*-

import sys


class Registers(object):
    def __str__(self):
        print("Register class. Read, process and save files data in arrays")

    def get_data(self, dir_file, name, end):
        """
        Reads the file to extract the value by line,
        then the file data is saved in a list
        and splits the content of lines by '|'

        dir_file(string): File directory
        type(string): Type of data 'person', 'country', 'roles', etc...
        end(int): Columns number
        """
        self.list_response = []
        input_file = open(dir_file, "r")
        for line in input_file:
            content = line.split('|')
            self.verify_data_structure(content, name, end)
            # Because the end of line has a break '\n'
            content[end - 1] = self.clean_value(content[end - 1])
            self.list_response.append(content)
        input_file.close()
        return self.list_response

    def verify_data_structure(self, line, name, end):
        # Verify if all lines has a correct format (same columns number)
        quantity_values = len(line)
        if quantity_values != end:
            print("\nError:\nThis " + name + " hasn't a valid format: ")
            print(line, quantity_values)
            sys.exit()

    def clean_value(self, value):
        # Removes end line characters
        value = value.replace('\n', '')
        return value
