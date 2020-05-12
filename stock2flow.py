import datetime
import numpy as np
import pickle #getting data from .txt
with open('data_coinpaprika_btc.txt','rb') as fp: 
    data = pickle.load(fp)

class extractor(): #extracting from data the relevant points
    def __init__(self,data):
        self.data = np.array(data)
    def mlist(self): #makes lists of time & price data
        p = []
        t = []
        m_cap = []
        for i in range(0,len(self.data),2): #data length = days since inception??
            p.append(self.data[i][0]['price'])
            t.append(self.data[i][0]['timestamp'])
            m_cap.append(self.data[i][0]['market_cap'])
        return p,t,m_cap
p,t,m_cap = extractor(data).mlist() #storin price, timestamp & marketcap as lists
t_yr = list(map(str,[string[:10] for string in t])) #more formatting for timestamp 

def dates(start_date,end_date): #extend t_yr into the future, code from data_coinpaprika.py
    start = datetime.datetime.strptime(start_date,'%Y%m%d')
    end = datetime.datetime.strptime(end_date,'%Y%m%d')
    step = datetime.timedelta(days=1)
    date_list = []
    while start<=end:
        date_list.append(start.date().strftime("%Y-%m-%d"))
        start += step
    return date_list
t_yr_extended = dates('20200513','20211201') #future dates of interes
t_yr_final = t_yr + t_yr_extended 

class blockdate():
    def __init__(self,date):
        self.date = datetime.datetime.strptime(date,'%Y-%m-%d')
        self.third = datetime.datetime(2019,7,12) #adjusted dates for model correction! 12 of May 2020 third halvning
        self.second = datetime.datetime(2015,8,6) #9th of July 2016 second halvning
        self.first = datetime.datetime(2012,3,18) #28th of November 2012 first halvning
        self.start = datetime.datetime(2010,10,1) #beginning of data
        self.blocksize = 210000 #blocks per halving
    def stock(self):
        if self.date > self.third: 
            date_difference = self.date-self.third
            stock = ((date_difference.days*900) + self.blocksize*87.5)*0.97 - 1000000 #adjustment for 3% loss & 1million donation
            return stock
        elif self.date > self.second:
            date_difference = self.date-self.second
            stock = ((date_difference.days * 1800) + self.blocksize*75)*0.97 - 1000000
            return stock
        elif self.date > self.first:
            date_difference = self.date-self.first
            stock = ((date_difference.days * 3600) + self.blocksize*50)*0.97 - 1000000 
            return stock
        else:
            date_difference = self.date-self.start
            stock = date_difference.days * 7200 * 0.97 
            return stock
    def flow(self):
        if self.date > self.third:
            flow = (self.blocksize/4)*6.25
            return flow
        elif self.date > self.second:
            flow = (self.blocksize/4)*12.5
            return flow
        elif self.date > self.first:
            flow = (self.blocksize/4)*25
            return flow
        else:
            flow = (self.blocksize/4)*50
            return flow
def S_F(dates):
    S = []
    F = []
    for i in range(len(dates)):
        S.append(blockdate(dates[i]).stock())
        F.append(blockdate(dates[i]).flow())
    return S,F
S,F = S_F(t_yr_final)
S2F = np.array(S)/np.array(F) 
S2F_model = 0.4 * S2F **3 #model idea BTC price = x*S2F**n

#plotting
import matplotlib.pyplot as plt 
plt.yscale('log')
plt.plot(t_yr,p,S2F_model)
plt.show()

#adjust price for inflation & find regression to S2F_model