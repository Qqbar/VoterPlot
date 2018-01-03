#!/usr/local/bin/python

# VoterData
# ==========================
# AUTHOR: Qqbar
# DATE CREATED: 2017.06.10

# IMPORTS #
#---------------#
import math
import datetime
import sys
import os
import json
import csv
from collections import defaultdict

# 3RD PARTY IMPORTS #
# -------------------------------#
import plotly
from plotly.graph_objs import Scatter, Layout

# GLOBALS #
#---------------#
# YEAR
YEAR = 2016

#ETYPE
# Election type of interest
# PE = Presidential Election
ETYPE = 'PE'

# STATE
# State of interest
STATE = 'NC'

# GRANULARITY
# S/C/W/P
GRANULARITY = 'P'

# DATA FILENAME
# File name for the voter data
CSV_DATA_FILENAME = '{0}_{1}_{2}_{3}.csv'.format(YEAR, ETYPE, GRANULARITY, STATE)

# DATA FILE PATH
# Path to the data file
CSV_DATA_FILEPATH = '../raw/{0}/{1}/'.format(YEAR, STATE)

# CLASSES #
#---------------#
class VoterData(object):
    '''
    Class that contains all of the data
    to be analyzed/plotted
    '''
    
    def __init__(self):
        self.year = YEAR
        self.state = STATE

        self.voter_csv_data_filepath = CSV_DATA_FILEPATH
        self.voter_csv_data_filename = CSV_DATA_FILENAME 

        self.voter_data_list = list()
        self.voter_data_json = ''

    def import_voter_data(self):
        '''
        Imports the data from csv file
        into list of dictionary
        '''
        # [ {COUNTY:  <COUNTY>
        #   MUNICIPALITY: <MUNICIPALITY>
        #   WARD: <WARD>
        # ...},{}]
        voter_data_dict = dict()
        header_list = list()
        #OPEN FILE
        with open("{0}{1}".format(self.voter_csv_data_filepath, self.voter_csv_data_filename), 'r') as voter_file:
            for line in voter_file:
                csl = line.strip("\n").split(",")
                # CONVERT NUMBERS TO INTS
                for i,c in enumerate(csl):
                    try:
                        csl[i] = int(c)
                    except:
                        pass
                # GET HEADER LIST
                if "HEADER DATA" in csl[0]:
                    # CREATE CANDIDATE KEYS
                    header_list = next(voter_file).strip("\n").split(",")
                    continue
                # GET VOTE DATA
                if len(header_list) > 0 and len(csl) > 1:
                    voter_data_dict = dict(zip(header_list, csl))
                    self.voter_data_list.append(voter_data_dict)

    def data_2_json(self):
        '''
        Converts voter_data_list
        to json object
        '''
        
        self.voter_data_json = json.dumps(self.voter_data_list, sort_keys=True, indent=4, separators=(',', ': '))

    def create_plot(self, county, range):
        '''
        Creates a scatter plot using the voter data
        contained in self.voter_data_list
        '''
        y1_data = list()
        y2_data = list()
        y3_data = list()
        x_data = list()
        # Sort voter_data_list by total votes
        sorted_voter_data_list = sorted(self.voter_data_list, key=lambda k: k['Total Votes']) 
        # Parse through voter data list
        for entry in sorted_voter_data_list:
            if entry["County Name"].strip(" ") == county:
                total_votes = float(entry["Total Votes"])
                votes_clinton = float(entry["Hillary Clinton / Tim Kaine"])
                votes_trump = float(entry["Donald J. Trump / Michael R. Pence"])
                try:
                    votes_other = float(entry["Other"])
                except:
                    votes_other = 0
                x_data.append(total_votes)
                try:
                    y1_data.append(votes_clinton/total_votes)
                except:
                    y1_data.append(0)
                try:
                    y2_data.append(votes_trump/total_votes)
                except:
                    y2_data.append(0)
                try:
                    y3_data.append(votes_other/total_votes)
                except:
                    y3_data.append(0)
        trace1 = Scatter(x=x_data, y=y1_data, name='CLINTON', mode='markers')
        trace2 = Scatter(x=x_data, y=y2_data, name='TRUMP', mode='markers')
        trace3 = Scatter(x=x_data, y=y3_data, name='OTHER', mode='markers')
        data = [trace1, trace2, trace3]

        #X LABEL
        xaxis_label = dict(
            title = 'PRECINCT',
            titlefont= dict(
                family= 'HELVETICA',
                size= 18,
                color= '#7f7f7f'
            )
        )

        #Y LABEL
        yaxis_label = dict(
            title = 'NORMALIZED VOTE RATIO PER PRECINCT',
            titlefont= dict(
                family= 'HELVETICA',
                size= 18,
                color= '#7f7f7f'
            )
        )

        plotly.offline.plot({"data": data, "layout": Layout(title="{0} | {1}".format(county, STATE), xaxis = xaxis_label, yaxis = yaxis_label)}, \
            filename = "{0}_{1}_{2}.html".format(YEAR, STATE, county), auto_open=False)
        
    def create_summed_plot(self, county, range, plot_type):
        '''
        Creates a scatter plot using the voter data
        contained in self.voter_data_list
        '''
        y1_data = list()
        y2_data = list()
        y3_data = list()
        x_data = list()
        # Sort voter_data_list by total votes
        sorted_voter_data_list = sorted(self.voter_data_list, key=lambda k: k['Total Votes']) 
        #sorted_voter_data_list = self.voter_data_list
        votes_summed_clinton = 0
        votes_summed_trump = 0
        votes_summed_other = 0
        votes_summed_total = 0
        for entry in sorted_voter_data_list:
            if entry["County Name"].strip(" ") == county:
                total_votes = float(entry["Total Votes"])
                votes_clinton = float(entry["Hillary Clinton / Tim Kaine"])
                votes_trump = float(entry["Donald J. Trump / Michael R. Pence"])
                try:
                    votes_other = float(entry["Other"])
                except:
                    votes_other = 0
                votes_summed_total += total_votes
                if plot_type == 'sum_tot':
                    x_data.append(votes_summed_total)
                elif plot_type == 'sum_ind':
                    x_data.append(total_votes)
                try:
                    votes_summed_clinton += votes_clinton
                    y1_data.append(votes_summed_clinton/votes_summed_total)
                except:
                    y1_data.append(0)
                try:
                    votes_summed_trump += votes_trump
                    y2_data.append(votes_summed_trump/votes_summed_total)
                except:
                    y2_data.append(0)
                try:
                    votes_summed_other+= votes_other
                    y3_data.append(votes_summed_other/votes_summed_total)
                except:
                    y3_data.append(0)


        trace1 = Scatter(x=x_data, y=y1_data, name='CLINTON', mode='markers')
        trace2 = Scatter(x=x_data, y=y2_data, name='TRUMP', mode='markers')
        trace3 = Scatter(x=x_data, y=y3_data, name='OTHER', mode='markers')
        data = [trace1, trace2, trace3]

        #X LABEL
        xaxis_label = dict(
            title = 'PRECINCT',
            titlefont= dict(
                family= 'HELVETICA',
                size= 18,
                color= '#7f7f7f'
            )
        )
        if plot_type == 'sum_tot':
            xaxis_label['title'] = 'SUMMED VOTES BY PRECINCT'

        #Y LABEL
        yaxis_label = dict(
            title = 'RUNNING NORMALIZED VOTE RATIO',
            titlefont= dict(
                family= 'HELVETICA',
                size= 18,
                color= '#7f7f7f'
            )
        )

        plotly.offline.plot({"data": data, "layout": Layout(title="{0} | {1} | [Running Total]".format(county, STATE), xaxis = xaxis_label, yaxis = yaxis_label)}, \
            filename = "{0}_{1}_{2}_{3}.html".format(plot_type, YEAR, STATE, county), auto_open=False)

if __name__ == '__main__':
    vd_1 = VoterData()
    vd_1.import_voter_data()
    vd_1.data_2_json()
    #vd_1.create_plot("WAYNE",[0,0])
    vd_1.create_summed_plot("WAYNE",[0,0],"sum_ind")