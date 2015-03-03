# Author:   Bala Venkatesan
# License:  Apache 2.0


########################################################################
# Wrote this file to separate out the loading of the data from the
# python file where the actual display happens
########################################################################


import pandas as pd
import csv


########################################################################
# Loading  data
########################################################################
statefile = open('./annual_averages_by_state.csv', 'r')
csvreader = csv.reader(statefile)

########################################################################
# initializing a dataframe to parse only required data from file
########################################################################
columns = ["STATE",
           "TOTAL_POPULATION",
           "WORKFORCE",
           "WORK_%_OF_POP",
           "EMPLOYED",
           "EMP_%_OF_POP",
           "UNEMPLOYED",
           "UNEMPLOMENT_RATE",
        ]
data = []
rowIndex = 0

########################################################################
# function that parses the state data for 2012 & 2013 and returns
# a DataFrame with the data read from the file
# the function cleans the data before returning the DataFrame
########################################################################

def state_data():
    for row in csvreader:

        #######################################################################################
        # intialize a bunch of index variables for data clean up
        # startat is used to push the iteration to the right in the case of states with 2 words
        # stopat moves corresponding.
        #######################################################################################
        index = 0
        startat = 0
        stopat=10

        statename = row[0]

        # Initializing pandas series for DataFrame.
        values = []
        for x in enumerate(row):
            print statename
            print x
            if(index == 0):
                values.append(statename.upper())
            else:
                values.append(x.replace(",",""))

            index = index + 1

        data.insert(rowIndex,values)


    df = pd.DataFrame(data,columns=columns)
    return df




if __name__ == '__main__':
    print state_data()
