import pickle #getting data from .txt
with open('data_coinpaprika_btc.txt','rb') as fp: 
    data = pickle.load(fp)

import numpy as np
class extractor(): #extracting from data the relevant points
    def __init__(self,data):
        #print('Extracting from price, timestamp & marketcap from data')
        self.data = np.array(data)
    def mlist(self): #makes lists of time & price data
        p = []
        t = []
        m_cap = []
        for i in range(0,len(self.data),2): #data length = days since inception??
            p.append(self.data[i][0]['price'])
            t.append(self.data[i][0]['timestamp'])
            m_cap.append(self.data[i][0]['market_cap'])
        #print('Extraction Completed')
        return p,t,m_cap
p,t,m_cap = extractor(data).mlist() #storin price, timestamp & marketcap as lists
t_yr = list(map(str,[string[:10] for string in t])) #more formatting for timestamp 
#extend t_yr for another 400 days
print(type(t_yr))

import datetime
class blockdate():
    def __init__(self,date):
        self.date = datetime.datetime.strptime(date,'%Y-%m-%d')
        self.third = datetime.datetime(2020,5,12) #12 of May 2020 third halvning
        self.second = datetime.datetime(2016,7,9) #9th of July 2016 second halvning
        self.first = datetime.datetime(2012,11,28) #28th of November 2012 first halvning
        self.start = datetime.datetime(2010,10,1) #beginning of data
        self.blocksize = 210000 #blocks per halving
    def stock(self):
        if self.date > self.third: 
            date_difference = self.date-self.third
            stock = (date_difference.days*900) + self.blocksize*87.5
            #print(stock)
            return stock
        elif self.date > self.second:
            date_difference = self.date-self.second
            stock = (date_difference.days * 1800) + self.blocksize*75
            #print(stock)
            return stock
        elif self.date > self.first:
            date_difference = self.date-self.first
            stock = (date_difference.days * 3600) + self.blocksize*50
            #print(stock)
            return stock
        else:
            date_difference = self.date-self.start
            stock = date_difference.days * 7200 
            #print(stock)
            return stock
    def flow(self):
        if self.date > self.third:
            flow = (self.blocksize/4)*6.25
            #print(flow)
            return flow
        elif self.date > self.second:
            flow = (self.blocksize/4)*12.5
            #print(flow)
            return flow
        elif self.date > self.first:
            flow = (self.blocksize/4)*25
            #print(flow)
            return flow
        else:
            flow = (self.blocksize/4)*50
            #print(flow)
            return flow
def S_F(dates):
    S = []
    F = []
    for i in range(len(dates)):
        S.append(blockdate(dates[i]).stock())
        F.append(blockdate(dates[i]).flow())
    return S,F
S,F = S_F(t_yr)
S2F = np.array(S)/np.array(F)
#how to fit this data as price prediction?

#plotting
import matplotlib.pyplot as plt 
plt.yscale('log')
plt.plot(t_yr,p,S2F)
plt.show()


### adjust model for inflation, initial 'donation' 1M btc & 1% loss annually
#from easymoney.money import EasyPeasy #easmoney module 
#ep = EasyPeasy() #instance
#p_norm = []
#for j in range(len(p)):
#    p_norm.append(ep.normalize(amount=p[j], region="USA",from_year=t_yr[j],to_year=2019,pretty_print=False))