# VoterPlot
A repository for raw data, reduced data and plots from the US general election/s.

## Data Model

- data  (directory)
  - year  (directory)
    - state (directory)
      - raw (directory)
        - raw_data_file/s (file/s)
      - reduced (directory)
        - year_PE_P_state.csv (files/s)
        
- results (directory)
  - year  (directory)
    - state (directory)
      - METHOD_1  (directory)
        - year_state_county.html  (file/s)
      - METHOD_2
        - sum_ind_year_state_county.html  (file/s)
      - METHOD_3
        - sum_tot_year_state_county.html  (file/s)

## Data
The raw data (as downloaded from each state's .gov website) is available in the data->year->state->raw directory, where year is the 4-digit election year, and state is the 2 character state abreviation.

The data->year->state->reduced directory contains a formatted subset of the raw data file for each state. Again, year is the 4-digit election year, and state is the 2 character state abreviation.

## Results
The resultant plots can be found in the results->year->state->METHOD directories.

#### METHOD_1
This directory contains scatter plots where the X-axis corresponds to the number of votes in each voting precinct (in increasing order) and the Y-axis corresponds to the ratio of votes for each candidate in the respective precinct.

For example: (Assuming only 2 precincts in the county) 
If Clinton received 4 votes, Trump received 5 votes, and the total number of votes in that precinct was 10, there would be a Clinton data point at .4, a Trump data point at .5, and an 'Other' data point at .1. These would all be plotted at x=10.
If in another precint Clinton received 10 votes, Trump received 8 votes, and the total number of votes in that precinct was 20, there would be a Clinton data point at .5, a Trump data point at .4, and an 'Other' data point at .1. These would all be plotted at x=20.

#### METHOD_2
This directory contains scatter plots where the X-axis corresponds to the number of votes in each voting precinct (in increasing order) and the Y-axis corresonds to the ratio of votes for each candidate as the sum of all previously counted precincts

For example: (Assuming only 2 precincts in the county)
If Clinton received 4 votes, Trump received 5 votes, and the total number of votes in that precinct was 10, there would be a Clinton data point at .4, a Trump data point at .5, and an 'Other' data point at .1. These would all be plotted at x=10.
If in another precint Clinton received 10 votes, Trump received 8 votes, and the total number of votes in that precinct was 20, there would be a Clinton data point at .467 ((4+10)/30), a Trump data point at .433 ((5+8)/30), and an 'Other' data point at .1 ((1+2)/30). These would all be plotted at x=20.

#### METHOD_3
This directory contains scatter plots where the X-axis corresponds to the sum total of votes in all previously counted precincts (precincts added in increasing order) and the Y-axis corresonds to the ratio of votes for each candidate as the sum of all previously counted precincts

For example: (Assuming only 2 precincts in the county)
If Clinton received 4 votes, Trump received 5 votes, and the total number of votes in that precinct was 10, there would be a Clinton data point at .4, a Trump data point at .5, and an 'Other' data point at .1. These would all be plotted at x=10.
If in another precint Clinton received 10 votes, Trump received 8 votes, and the total number of votes in that precinct was 20, there would be a Clinton data point at .467 ((4+10)/30), a Trump data point at .433 ((5+8)/30), and an 'Other' data point at .1 ((1+2)/30). These would all be plotted at x=30 (10+20).
