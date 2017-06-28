# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 10:39:23 2016

@author: msdogan
"""
# web scraping module - Mustafa Dogan
# note: you cannot request hourly data from OASIS more than 31 days
import requests, zipfile, StringIO, time

# some example urls
example_url = 'http://oasis.caiso.com/oasisapi/SingleZip?queryname=PRC_HASP_LMP&startdatetime=20130919T07:00-0000&enddatetime=20130919T08:00-0000&version=2&market_run_id=HASP&node=LAPLMG1_7_B2&resultformat=6'
example_url0 = 'http://oasis.caiso.com/oasisapi/GroupZip?groupid=HASP_LMP_GRP&startdatetime=20130919T07:00-0000&version=1&grp_type=ALL_APNODES&resultformat=6'
example_url1 = 'http://oasis.caiso.com/oasisapi/SingleZip?queryname=PRC_LMP&startdatetime=20130919T07:00-0000&enddatetime=20130920T07:00-0000&version=1&market_run_id=RTPD&grp_type=ALL_APNODES&resultformat=6'
example_url2 = 'http://oasis.caiso.com/oasisapi/GroupZip?groupid=HASP_LMP_GRP&startdatetime=20130901T07:00-0000&enddatetime=20130919T07:00-0000&version=1&resultformat=6' # this returns only 1 hour data starting start data. End date does not matter
example_group = 'http://oasis.caiso.com/oasisapi/SingleZip?resultformat=6&queryname=PRC_RTPD_LMP&version=3&startdatetime=20170626T07:00-0000&enddatetime=20170626T08:00-0000&market_run_id=RTPD&grp_type=ALL_APNODES'

# building a url - components
queryname = 'PRC_RTPD_LMP' # download locational marginal price
market_run_id = 'RTPD' # realtime price dispatch
# grp_type = 'ALL_APNODES'
grp_type = 'ALL'
resultformat = '6' # this downloads as csv
single_api_name = 'http://oasis.caiso.com/oasisapi/SingleZip?'
# group_api_name = 'http://oasis.caiso.com/oasisapi/GroupZip?'
# node = ['JBBLACK2_7_B1'] # enter node names you want to download
version = 2

# group url building. returns only 1 hour of data
#url_group = group_api_name + 'groupid=' + group_id + '&' + 'startdatetime=' + startdatetime + '&' + 'enddatetime=' + enddatetime + '&' + 'version=1' + '&' + 'grp_type=' + grp_type + '&' + 'resultformat=' + resultformat
n_days = {'Jan':31, 'Feb':28, 'Mar':31, 'Apr':30, 'May':31,  'Jun':30, 'Jul':31, 'Aug':31, 'Sep':30, 'Oct':31, 'Nov':30, 'Dec':31}
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep','Oct', 'Nov', 'Dec']

# enter starting year you want to download
y = 2016 # beginning year

# build url and request price data
for index in range(0,len(months)):
    item = months[index]
    m = index+1 # month number
    if m < 10:
        m = '0' + str(m) # starting month <10
    for d in range(18,n_days[item]):
        d += 1
        if d < 10:
            d = '0' + str(d) # starting day <10
        for h in range(0,24):
            he = h+1
            if h < 10:
                h = '0' + str(h) # starting hour <10
            startdatetime = str(str(y)+str(m)+str(d)+'T'+str(h)+':00-0000') # start time 
            if he == 24: # ending hour
                he = 0
            if he < 10:
                he = '0' + str(he) # end smonth <10
            enddatetime = str(str(y)+str(m)+str(d)+'T'+str(he)+':00-0000') # start time
            print('now downloading: ' + startdatetime)
            url = single_api_name+'resultformat='+str(resultformat)+'&queryname='+queryname+'&version='+str(version)+'&startdatetime='+startdatetime+'&enddatetime='+enddatetime+'&market_run_id='+market_run_id+'&grp_type='+grp_type
            r = requests.get(url, verify=True, timeout=500) # request price data, single or all
            z = zipfile.ZipFile(StringIO.StringIO(r.content)) # url request returns a zip file
            z.extractall(queryname+'/'+str(y)+'/'+str(item)+'/Day_'+str(d)) # unzip files, you can also specify a directory
            time.sleep(6) # wait for 6 seconds