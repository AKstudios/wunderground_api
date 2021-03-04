# merge all daily wunderground csv data files into one file
# Akram Ali
# updateed on 03/21/2020

from datetime import datetime, timedelta
import time
import os

line = []
dt_hours = []
hours = []
master=[]

# filepath = 'C:\\Users\\AKstudios\\Desktop\\wunderground'
filepath = 'C:\\Users\\AK\\Dropbox\\2018 - TRV control project\\All data [14 Jan - 17 Mar 2019]\\wunderground\\daily\\2020'
start = '2020-02-01'
end =  '2020-03-20'
# h1 = '7:53 PM'     # data for every day starts with 7:53 PM on Wunderground in 2018-2019
h1 = '1:53 AM'     # data for every day starts with 1:53 AM on Wunderground in 2020 for some weird god forsaken reason

d = datetime.strptime(start, '%Y-%m-%d')
a = datetime.strptime('%s %s' % (start,h1), '%Y-%m-%d %I:%M %p')

filenames = [name for name in os.listdir(filepath) if name.endswith(".csv")]

for csv in filenames:
    # extract all lines from csv
    with open('%s\\%s' % (filepath, csv), 'r') as file:
        file.readline()
        for row in file:
            line.append(row.split(','))

    # get rid of all time stamps that don't have 53 in it
    for row in line:
        if '53' in row[0]:
            hours.append(row)
        else:
            pass

    # convert time in list to datetime format
    for row in hours:
        dt = datetime.strptime('%s %s' % (d.date(),str(row[0])), '%Y-%m-%d %I:%M %p')
        dt_hours.append(dt)


    # iterate over entire day, sort and append to master list with proper date and times
    for n in range(24):
        a_time = a.time()   # extract only time from datetime
        a_string = a_time.strftime("%#I:%M %p") # convert to string -- # removes the leading zero in Windows. use - in Linux
        for l in hours:
            if l[0] == a_string:    # check where that particular hour is
                fixed = l
                fixed[0] = str(a)
                master.append(fixed)    # add that hour to the list
            else:
                pass

        a += timedelta(hours=1) # increment hours

    # set next day
    d += timedelta(days=1)

    # set next date of a
    a = datetime.strptime('%s %s' % (d.date(),h1), '%Y-%m-%d %I:%M %p')

    # clear all necessary lists
    line[:]=[]
    hours[:]=[]
    dt_hours[:]=[]

for n in master:
    z = ','.join(n)
    with open('outdoor.csv', 'a') as file:
        file.write(z)
