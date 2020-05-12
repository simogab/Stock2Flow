### Task of this code: get BTC data all the way back from 2009 as list in text file
import time 
from datetime import datetime, timedelta
from coinpaprika import client as Coinpaprika #coinpaprika module library
client = Coinpaprika.Client() #getting data from coinpaprika

class dates_generator: #list of dates in question in callable format for coinpaprika
    def __init__(self):
        print('Generating list of relevant dates...')
    def dates(self,start_date,end_date):
        start = datetime.strptime(start_date,'%Y%m%d')
        end = datetime.strptime(end_date,'%Y%m%d')
        step = timedelta(days=1)
        date_list = []
        while start<=end:
            date_list.append(start.date().strftime("%Y-%m-%d"))
            start += step
        print('success')
        return date_list
dates = dates_generator().dates('20101001','20200512') #call class instance & function 

class data_generator: #list of data - change to numpy for better usability
    def __init__(self):
        print('Generating historical bitcoin data...')
    def data(self,dates):
        data = []
        print('This might take some time due to 10call/s limiter...')
        for i in range(len(dates)):
            data.append(client.historical("btc-bitcoin",start=dates[i]))
            time.sleep(0.105) #where is the limit? 0.1?
        print('success')
        return data
data = data_generator().data(dates)

import pickle
with open("data_coinpaprika_btc.txt","wb") as fp: # saving as .txt
    pickle.dump(data,fp)
