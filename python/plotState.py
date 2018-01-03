#!/usr/local/bin/python

# plotState
# ==========================
# AUTHOR: Qqbar
# DATE CREATED: 2017.06.14

# IMPORTS #
#---------------#
from VoterData import *
from countyLists import *

if __name__ == '__main__':
    vd_1 = VoterData()
    vd_1.import_voter_data()

    for co in COUNTY_DICT[STATE]:
        #vd_1.create_plot(co, [0,0])
        #vd_1.create_summed_plot(co,[0,0],"sum_ind")
        vd_1.create_summed_plot(co,[0,0],"sum_tot")
#     vd_1.data_2_json()
#     vd_1.create_plot("WAYNE",[0,0])