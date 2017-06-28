# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 10:39:23 2016

@author: msdogan
"""
# web scraping module - Mustafa Dogan
# note: you cannot request hourly data from OASIS more than 31 days
import requests, zipfile, StringIO, time

# some example urls
example_url = 'http://oasis.caiso.com/oasisapi/SingleZip?resultformat=6&queryname=PRC_FUEL&version=1&FUEL_REGION_ID=ALL&startdatetime=20170626T07:00-0000&enddatetime=20170627T07:00-0000'

# building a url - components
queryname = 'PRC_FUEL' # download locational marginal price
FUEL_REGION_ID = 'ALL'
resultformat = '6' # this downloads as csv
single_api_name = 'http://oasis.caiso.com/oasisapi/SingleZip?'
# group_api_name = 'http://oasis.caiso.com/oasisapi/GroupZip?'
# node = ['JBBLACK2_7_B1'] # enter node names you want to download
version = 1

# group url building. returns only 1 hour of data
#url_group = group_api_name + 'groupid=' + group_id + '&' + 'startdatetime=' + startdatetime + '&' + 'enddatetime=' + enddatetime + '&' + 'version=1' + '&' + 'grp_type=' + grp_type + '&' + 'resultformat=' + resultformat
n_days = {'Jan':31, 'Feb':28, 'Mar':31, 'Apr':30, 'May':31,  'Jun':30, 'Jul':31, 'Aug':31, 'Sep':30, 'Oct':31, 'Nov':30, 'Dec':31}
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep','Oct', 'Nov', 'Dec']

# enter starting and ending year and month that you want to download

y = 2013 # beginning year

# build url and request price data
for index in range(0,len(months)):
    year = y
    item = months[index]
    m = index+1 # month number
    smon = m
    if m < 10:
        smon = '0' + str(m) # starting month <    
    for d in range(0,n_days[item]):
        d += 1 # starting day
        de = d + 1 # ending day
        emon = smon
        if d == n_days[item]:
            de = 1
            emon = m+1
            if emon < 10:
                emon = '0' + str(emon)
        if d < 10:
            d = '0' + str(d) # starting day <10
        if de < 10:
            de = '0' + str(de) # ending day <10
        startdatetime = str(str(y)+str(smon)+str(d)+'T07:00-0000') # start time
        if emon == 13:
            emon = '01'
            de = '01'
            y = y+1
        enddatetime = str(str(y)+str(emon)+str(de)+'T07:00-0000') # start time
        print('now downloading: ' + startdatetime, enddatetime)
        url = single_api_name+'resultformat='+str(resultformat)+'&queryname='+queryname+'&version='+str(version)+'&FUEL_REGION_ID='+FUEL_REGION_ID+'&startdatetime='+startdatetime+'&enddatetime='+enddatetime 
        r = requests.get(url, stream=True, timeout=500) # request price data, single or all
        z = zipfile.ZipFile(StringIO.StringIO(r.content)) # url request returns a zip file
        z.extractall(queryname+'/'+str(year)+'/'+str(item)) # unzip files, you can also specify a directory      
        time.sleep(6) # pause for 6 seconds. CAISO violation less than 5 seconds of requesting