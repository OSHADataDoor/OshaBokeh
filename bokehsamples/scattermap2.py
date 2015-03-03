# Author:   Bala Venkatesan
# License:  Apache 2.0


from bokeh.plotting import *
from bokeh.models import HoverTool, ColumnDataSource
import pandas as pd
from collections import OrderedDict


datafile = pd.read_csv("./annual_averages_by_state.csv")
populations = pd.DataFrame(data=datafile, columns=['STATE','TOTAL_POPULATION'])
employed = pd.DataFrame(data=datafile, columns=['STATE','EMPLOYED'])
unemployed = pd.DataFrame(data=datafile, columns=['STATE','UNEMPLOYED'])
print unemployed

def mtext(p, x, y, textstr):
    p.text(x, y, text=textstr,
         text_color="#449944", text_align="center", text_font_size="10pt")

## returns population value from table.
def valueforstate(df,state):
    value=0
    for i, row in enumerate(df.values):
        #first column is stateName
        stateName = row[0]
        if(stateName.upper() == state.upper()):
            #second column is population in 2012
            value = row[1].replace(",","").strip()
    return int(value)





########################################################################
# Loading accident data by state
# breaking it out into 4 quartiles
########################################################################
datafile = pd.read_csv("/Users/bvenkatesan/Documents/workspace/PyCharmProjects/capstone/data/incidents_state_totals.csv")


accidents = pd.DataFrame(datafile, columns=['code','state','totals'])

quartiles = pd.qcut(datafile["totals"],4,labels=[1, 2, 3, 4], precision=1)

########################################################################
# color palate
########################################################################
colormap = {
    '1'         : "#ffffb2",
    '2' : "#fecc5c",
    '3'              : "#fd8d3c",
    '4'                : "#f03b20",
    '0':  "#f7f7f7",
}


def drawFile(removeOutliers, filename):
    state_colors = []
    state_names = []
    pops = []
    fatalities=[]
    employment=[]
    unemployment=[]

    p = figure(title="Fatalities Plot")

    ########################################################################
    # looping through the datafile to create state-by-state mapping
    ########################################################################
    for i, row in enumerate(accidents.values):

        try:
            code = row[0]
            state = row[1]
            total = row[2]
            if( removeOutliers and (code == 'CA')):
                print removeOutliers
                print 'remove outlier is true '+ state
                pass
            else:
                print 'remove outlier is false '+ state
                pops.append(valueforstate(populations,state))
                employment.append(valueforstate(employed,state))
                unemployment.append(valueforstate(unemployed,state))
                fatalities.append(total)
                state_colors.append(colormap[str(quartiles[i])])
                state_names.append(state)
                #print pops.__len__()
                #print state_colors.__len__()
                #print state_names.__len__()
                #print fatalities.__len__()
                print employment
                print unemployment.__len__()
            #idx = min(int(rate/2), 5)
            #state_colors.append(colors[idx])
        except KeyError:
            state_colors.append(colormap['0'])



    ########################################################################
    # Creating columndatasource for hover tool
    ########################################################################
    hoverLabels = ColumnDataSource(
        data=dict(
            x=fatalities,
            y=pops,
            state= state_names,
            employed= employment,
            unemployed = unemployment,
        )
    )

    ########################################################################
    # Loading accident data by state
    ########################################################################
    p = figure(title="Fatalities Total without Outlier", toolbar_location="left", tools="resize,hover,save",
               plot_width=1100, plot_height=700)

    hover = p.select(dict(type=HoverTool))
    hover.tooltips = OrderedDict([
        ('State: ', '@state'),
        ('Fatalities: ', '@x'),
        ('Population (in 000s): ', '@y'),
        ('Employment (in 000s): ', '@employed'),
        ('Unemployment (in 000s): ', '@unemployed'),
    ])


    output_file(filename)

    p.scatter(fatalities, pops, marker="circle", line_color="#6666ee", ylabel='fatality', source=hoverLabels,
              fill_color=state_colors, fill_alpha=0.5, size=12)

    show(p)  # open a browser

if __name__ == '__main__':
    drawFile(False,'../temp/scatter2_with_outlier.html')
    drawFile(True,'../temp/scatter2_without_outlier.html')