import plotly.figure_factory as ff
import datetime
import numpy as np
import random

def plotResult(table, maxValue):
    df = []
    mn = 0
    colors = []
    for row in table:
        mn += 1
        row.sort(key=lambda x: x[2])
        for slot in row:
            start_time=str(datetime.timedelta(seconds=slot[0]))
            end_time=str(datetime.timedelta(seconds=slot[1]))
            today = datetime.date.today()
            entry = dict(
                Task='Machine-{0}'.format(mn), 
                Start="{0} {1}".format(today, start_time), 
                Finish="{0} {1}".format(today, end_time),
                duration=slot[1] - slot[0],
                Resource='Job {0}'.format(slot[2] + 1)
                )
            df.append(entry)

            #Generate random colors
            if(len(colors) < len(row)):
                a = min(255 - ( slot[2] * 10 ), 255)
                b = min(slot[2] * 10, 255)
                c = min(255, int(random.random() * 255))
                colors.append("rgb({0}, {1}, {2})".format(a, b, c))

    #In order to see the line ordered by integers and not by dates we need to generate the dateticks manually
    #we create 11 linespaced numbers between 0 and the maximum value
    num_tick_labels = np.linspace(start = 0, stop = maxValue, num = 11, dtype = int)
    date_ticks = ["{0} {1}".format(today, str(datetime.timedelta(seconds=int(x)))) for x in num_tick_labels]

    fig = ff.create_gantt(df,colors=colors, index_col='Resource', group_tasks=True, show_colorbar=True, showgrid_x=True, title='Job shop Schedule')
    fig.layout.xaxis.update({
        'tickvals' : date_ticks,
        'ticktext' : num_tick_labels
        })
    fig.show()
