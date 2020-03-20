# -*- coding: utf-8 -*-

from apps.analyser import Analyser

# INIT PROCESS
ranking = Analyser("countries.in", "industries.in", 'roles.in', "people.in")
ranking.start_process()
ranking.get_evaluatization()

#
# Analitycs functions from here, can remove it
#
"""
This functions are used to extract a list of countries ,
roles and indurtries on input file and generate a test values
"""
# ranking.init_lists()
# ranking.menu_print_lists()
