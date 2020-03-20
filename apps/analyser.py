# -*- coding: utf-8 -*-

import os
import sys
import random
import operator
from apps.people import People
from apps.countries import Countries
from apps.roles import Roles
from apps.industries import Industries

# GLOBAL VARIABLES SECTION, USE ONLY FOR CONSTANT VALUES
DIR_ROOT = os.getcwd() + "/"
DIR_INPUTS = DIR_ROOT + "resources/files/inputs/"
DIR_OUTPUTS = DIR_ROOT + "resources/files/outputs/"


class Analyser(object):
    def __init__(self, country, industry, rol, people):
        self.people_out = []
        self.MAX_RECOMMENDATIONS = 0
        self.MAX_CONNECTIONS = 0

        self.countries = Countries(DIR_INPUTS, country)
        self.industries = Industries(DIR_INPUTS, industry)
        self.roles = Roles(DIR_INPUTS, rol)
        self.people = People(DIR_INPUTS, people)

        # Importance of parameters. Between 0 - 100
        self.get_weights()

        # This is only for analytics purpose on testing, etc...
        # can remove it from here
        self.list_roles = []
        self.list_countries = []
        self.list_industries = []
        self.list_people = self.people.content
        self.dict_stats = {}
    
    def get_weights(self):
        message = "Change defaults weights (y/n):"
        default_weights = input(message)

        if default_weights.lower() == 'y':
            self.W_RECOMMENDATIOS = self.input_number('Recommendations weight (0-100):')
            self.W_CONNECTIONS = self.input_number('Connections weight (0-100):')
            self.W_INDUSTRIES = self.input_number('Industries weight (0-100):')
            self.W_COUNTRIES = self.input_number('Countries weight (0-100):')
            self.W_ROLES = self.input_number('Roles weight (0-100):')

            comprobation = self.W_RECOMMENDATIOS + self.W_CONNECTIONS
            comprobation += self.W_INDUSTRIES + self.W_COUNTRIES
            comprobation += self.W_ROLES

            if comprobation != 100:
                print("Sum of weights needs to be 100")
                self.get_weights()
        else:   
            self.W_RECOMMENDATIOS = 45
            self.W_CONNECTIONS = 30
            self.W_INDUSTRIES = 10
            self.W_COUNTRIES = 8
            self.W_ROLES = 7

    def input_number(self, message):
        while True:
            try:
                user_input = int(input(message))       
            except ValueError:
                print("Not an integer! Try again.")
                continue
            else:
                return user_input 
            break 
        
    def start_process(self):
        self.people.start()
        self.industries.start()
        self.roles.start()
        self.countries.start()

        self.explore_list()
        
    def explore_list(self):
        for person in self.people.content:
            self.extract_unique_values(person)

        # This lines can be removed, are only for test and analitycs
        self.order_lists()
        self.stats()

    def extract_unique_values(self, person):
        connections = int(person[7])
        recommendations = int(person[6])

        if self.MAX_CONNECTIONS < connections:
            self.MAX_CONNECTIONS = connections

        if self.MAX_RECOMMENDATIONS < recommendations:
            self.MAX_RECOMMENDATIONS = recommendations

        # Testing and dev, can be removed
        # This lines helps to generate a list of roles, countries and industries
        if self.checking_list(person[3], self.list_roles):
            self.list_roles.append(person[3])

        if self.checking_list(person[4], self.list_countries):
            self.list_countries.append(person[4])

        if self.checking_list(person[5], self.list_industries):
            self.list_industries.append(person[5])

    def checking_list(self, value, source_list):
        return value not in source_list
    
    def get_evaluatization(self):
        for client in self.people.content:
            p_rol = self.valorization(self.roles.content, client[3])
            p_countries = self.valorization(self.countries.content, client[4])
            p_industries = self.valorization(self.industries.content, client[5])

            p_recommendations = int(client[6]) / self.MAX_RECOMMENDATIONS
            p_connections = int(client[7]) / self.MAX_CONNECTIONS

            p_rol = p_rol * self.W_ROLES
            p_countries = p_countries * self.W_COUNTRIES
            p_industries = p_industries * self.W_INDUSTRIES
            p_recommendations = p_recommendations * self.W_RECOMMENDATIOS
            p_connections = p_connections * self.W_CONNECTIONS

            p_total = p_rol
            p_total += p_countries
            p_total += p_industries
            p_total += p_recommendations
            p_total += p_connections
            
            p_total = p_total/100

            self.people_out.append([client[0], p_total])
        self.sort_out()
        self.people.file_out(self.people_out, DIR_OUTPUTS)
        self.print_out_menu()

    def valorization(self, source_list, value):
        for items in source_list:
            if value == items[1]:
                return float(items[2])

    def sort_out(self):
        self.people_out.sort(key=lambda x: x[1])
        self.people_out.reverse()
        self.people_out = self.people_out[:100]
    
    def print_out_menu(self):
        option = input("Print out list with details (y/n):")

        if option == "y":
            for person in self.people_out:
                for row in self.people.content:
                    if row[0] == person[0]:
                        print(row)

    #
    # Analitycs and test functions from here, can remove it
    #
    """
    This function extract all parameters from people input and start
    a process to give fill al lists

    It's a process to extract stats and fill test data
    """        
    def stats(self):
        self.dict_stats['people'] = {
            'quantity': len(self.people.content)
        }

        self.dict_stats['roles'] = {
            'quantity': len(self.list_roles)
        }

        self.dict_stats['countries'] = {
            'quantity': len(self.list_countries)
        }

        self.dict_stats['industries'] = {
            'quantity': len(self.list_industries)
        }

        print(self.dict_stats)

    def order_lists(self):
        self.list_roles.sort()
        self.list_countries.sort()
        self.list_industries.sort()

    """
    This section has all visualization methods
    """
    def menu_print_lists(self):
        selection = None
        dict_options = {
            1: "roles",
            2: "countries",
            3: "industries",
            4: "people"
        }
        show = input("Do you want see a list? (y/n): ")

        if show.lower() == 'y':
            self.explore_list()
            selection = int(input(
                "Enter number of list.\r\n" +
                "1. Roles\r\n" +
                "2. Countries\r\n" +
                "3. Industries\r\n" +
                "4. People\r\n" +
                "Enter your selection: "
            ))

            self.printing_selection(selection, dict_options)
        else:
            print("Process clompleted...")

    def printing_selection(self, selection, dict_options):
        if selection in dict_options:
            option = "list_" + dict_options[selection]
            printable_lst = getattr(self, option, "That list doesn't exists")
            self.print_list(printable_lst)
        else:
            print("That's not a valid option")
            print("Process clompleted...")

    def print_list(self, value):
        print(value)

    """
    Tests input generation area.
    Fill a list with a random valorization
    """
    def create_lists(self, filename, list_input):
        i = 0
        f = open(filename, "w")

        for row in list_input:
            value = round(random.uniform(0, 1), 8)
            line = str(i) + '|' + row + '|' + str(value) + "\n"
            f.write(line)

            i += 1

    def init_lists(self):
        self.create_lists(self.roles.filename, self.list_roles)
        self.create_lists(self.countries.filename, self.list_countries)
        self.create_lists(self.industries.filename, self.list_industries)

    # This function helps to verify if all countries are on countries.in
    def check_countries(self):
        list_test_countries = []

        for country in self.countries.content:
            list_test_countries.append(country[1])
            tmp = country[2]
            print(tmp)

        for country in self.list_countries:
            if country not in list_test_countries:
                print(country)
                print('This is not on list countries.in')  
