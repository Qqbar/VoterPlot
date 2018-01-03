#!/usr/local/bin/python

# NC2CSV
# ==========================
# AUTHOR: Qqbar
# DATE CREATED: 2017.06.13

# IMPORTS #
#---------------#
import math
import datetime
import sys
import os
import csv
from collections import defaultdict

# LOOKUP DICTS #
#------------------------#
CANDIDATE = {
'Hillary Clinton':'CLINTON',
'Donald J. Trump':'TRUMP'
}

OFFICE = {
'1001':'President'
}

YEAR = 2016
STATE = 'NC'

class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

class NC2CSV(object):
    '''
    A Class for converting NC txt data to
    NC CSV data for plotting.
    '''
    
    def __init__(self):
        self.new = 0
        self.voter_tsv_data_filepath = '../raw/{0}/{1}/ORIGINAL/'.format(YEAR,STATE)
        self.voter_tsv_data_filename = 'results_pct_{0}1108.txt'.format(YEAR)
        self.final_voter_dict = dict()
        self.voter_csv_data_filename = '{0}vote.csv'.format(YEAR)

    def import_file(self):
        
        voter_dict = AutoVivification()
        header_list = list()
#         c_list = list()
        with open("{0}{1}".format(self.voter_tsv_data_filepath, self.voter_tsv_data_filename), 'r') as voter_file:
            for line_num, line in enumerate(voter_file):
                tsv = line.strip("\r\n").split("\t")
                if line_num == 0:
                    header_list = tsv
                elif line_num >= 1:
                    if tsv[3] == '1001':
                        county = tsv[0]
#                         c_list.append(county)
                        precinct = tsv[2]
                        candidate = tsv[6]
                        num_votes = tsv[13]
                        location = "{0}_{1}".format(county,precinct)
                        if candidate == 'Hillary Clinton':
                            voter_dict[county][location]['CLINTON'] = num_votes
                        elif candidate == 'Donald J. Trump':
                            voter_dict[county][location]['TRUMP'] = num_votes
                        else:
                            voter_dict[county][location]['OTHER'] = num_votes

        for x in voter_dict:
            for y in voter_dict[x]:
                try:
                    a = int(voter_dict[x][y]['CLINTON'])
                    b = int(voter_dict[x][y]['TRUMP'])
                    c = int(voter_dict[x][y]['OTHER'])
                    voter_dict[x][y]['SUM'] = a + b + c
                except:
                    pass

        self.final_voter_dict = voter_dict
#         for c in sorted(set(c_list)):
#             print c

    def write_file(self):

        header_list = ['County Name', 'Reporting Unit', 'Total Votes', 'Donald J. Trump / Michael R. Pence', 'Hillary Clinton / Tim Kaine', 'Other']
        csv_list = list()
        for county in sorted(self.final_voter_dict):
            for location in sorted(self.final_voter_dict[county]):
                v_c = self.final_voter_dict[county][location]['CLINTON']
                v_t = self.final_voter_dict[county][location]['TRUMP']
                v_o = self.final_voter_dict[county][location]['OTHER']
                v_s = self.final_voter_dict[county][location]['SUM']
                csv_list.append([county, location, v_s, v_t, v_c, v_o])

        with open("{0}{1}".format(self.voter_tsv_data_filepath, self.voter_csv_data_filename), 'w') as voter_csv_file:
            voter_csv_file.write("# HEADER DATA")
            voter_csv_file.write("\n")
            voter_csv_file.write(','.join(map(str,header_list)))
            voter_csv_file.write("\n")
            voter_csv_file.write("# VOTE DATA")
            voter_csv_file.write("\n")
            for ent in csv_list:
                voter_csv_file.write(','.join(map(str,ent)))
                voter_csv_file.write("\n")

if __name__ == '__main__':
    nc_1 = NC2CSV()
    nc_1.import_file()
    #nc_1.write_file()