#!/usr/local/bin/python

# MI2CSV
# ==========================
# AUTHOR: Qqbar
# DATE CREATED: 2017.06.12

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
'-1142':'HOEFLING',
'-1141':'MATUREN',
'-1140':'MOOREHEAD',
'-1139':'MCMULLIN',
'-1137':'KOTLIKOFF',
'-1136':'HARTNELL',
'-1135':'FOX',
'-1130':'STEIN',
'-1128':'CLINTON',
'-1112':'SOLTYSIK',
'-1110':'TRUMP',
'-1108':'CASTLE',
'-1101':'JOHNSON'
}

OFFICE = {
'1':'President'
}

COUNTY = {
'1':'ALCONA',
'2':'ALGER',
'3':'ALLEGAN',
'4':'ALPENA',
'5':'ANTRIM',
'6':'ARENAC',
'7':'BARAGA',
'8':'BARRY',
'9':'BAY',
'10':'BENZIE',
'11':'BERRIEN',
'12':'BRANCH',
'13':'CALHOUN',
'14':'CASS',
'15':'CHARLEVOIX',
'16':'CHEBOYGAN',
'17':'CHIPPEWA',
'18':'CLARE',
'19':'CLINTON',
'20':'CRAWFORD',
'21':'DELTA',
'22':'DICKINSON',
'23':'EATON',
'24':'EMMET',
'25':'GENESEE',
'26':'GLADWIN',
'27':'GOGEBIC',
'28':'GD. TRAVERSE',
'29':'GRATIOT',
'30':'HILLSDALE',
'31':'HOUGHTON',
'32':'HURON',
'33':'INGHAM',
'34':'IONIA',
'35':'IOSCO',
'36':'IRON',
'37':'ISABELLA',
'38':'JACKSON',
'39':'KALAMAZOO',
'40':'KALKASKA',
'41':'KENT',
'42':'KEWEENAW',
'43':'LAKE',
'44':'LAPEER',
'45':'LEELANAU',
'46':'LENAWEE',
'47':'LIVINGSTON',
'48':'LUCE',
'49':'MACKINAC',
'50':'MACOMB',
'51':'MANISTEE',
'52':'MARQUETTE',
'53':'MASON',
'54':'MECOSTA',
'55':'MENOMINEE',
'56':'MIDLAND',
'57':'MISSAUKEE',
'58':'MONROE',
'59':'MONTCALM',
'60':'MONTMORENCY',
'61':'MUSKEGON',
'62':'NEWAYGO',
'63':'OAKLAND',
'64':'OCEANA',
'65':'OGEMAW',
'66':'ONTONAGON',
'67':'OSCEOLA',
'68':'OSCODA',
'69':'OTSEGO',
'70':'OTTAWA',
'71':'PRESQUE ISLE',
'72':'ROSCOMMON',
'73':'SAGINAW',
'74':'ST. CLAIR',
'75':'ST. JOSEPH',
'76':'SANILAC',
'77':'SCHOOLCRAFT',
'78':'SHIAWASSEE',
'79':'TUSCOLA',
'80':'VAN BUREN',
'81':'WASHTENAW',
'82':'WAYNE',
'83':'WEXFORD',
}

YEAR = 2016
STATE = 'MI'

class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

class MI2CSV(object):
    '''
    A Class for converting MI txt data to
    MI CSV data for plotting.
    '''
    
    def __init__(self):
        self.new = 0
        self.voter_tsv_data_filepath = '../raw/{0}/{1}/ORIGINAL/{0}GEN/'.format(YEAR,STATE)
        self.voter_tsv_data_filename = '{0}vote.txt'.format(YEAR)
        self.final_voter_dict = dict()
        self.voter_csv_data_filename = '{0}vote.csv'.format(YEAR)
        
    def import_file(self):
        
        voter_dict = AutoVivification()
        with open("{0}{1}".format(self.voter_tsv_data_filepath, self.voter_tsv_data_filename), 'r') as voter_file:
            for line in voter_file:
                
                tsv = line.split("\t")
                county = tsv[6]
                city = int(tsv[7])
                ward = int(tsv[8])
                precinct = int(tsv[9])
                candidate = tsv[5]
                num_votes = int(tsv[11])
                #Unique location id
                location = '{0:02d}{1:02d}{2:03d}'.format(city,ward,precinct)
                if candidate == '-1128': #CLINTON
                    voter_dict[COUNTY[county]][location]['CLINTON'] = num_votes 
                elif candidate == '-1110': #TRUMP
                    voter_dict[COUNTY[county]][location]['TRUMP'] = num_votes 
                elif candidate != '-1128' and candidate != '-1110' and candidate in CANDIDATE.keys():
                    print candidate
                    voter_dict[COUNTY[county]][location]['OTHER'] = num_votes 

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
    mi_1 = MI2CSV()
    mi_1.import_file()
    mi_1.write_file()
    