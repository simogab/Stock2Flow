import pickle #getting data from .txt
with open('data_coinpaprika_btc.txt','rb') as fp: 
    data = pickle.load(fp)

import numpy as np
class extractor(): #extracting from data the relevant points
    def __init__(self,data):
        print('Extracting from price, timestamp & marketcap from data')
        self.data = np.array(data)
    def mlist(self): #makes lists of time & price data
        p = []
        t = []
        m_cap = []
        for i in range(0,len(self.data),2): #data length = days since inception??
            p.append(self.data[i][0]['price'])
            t.append(self.data[i][0]['timestamp'])
            m_cap.append(self.data[i][0]['market_cap'])
        print('Extraction Completed')
        return p,t,m_cap
p,t,m_cap = extractor(data).mlist() #storin price, timestamp & marketcap as lists
circ_supply = np.array(m_cap)/np.array(p) #use price & marketcap to get circulating supply (as numpy array)
t_yr = list(map(str,[string[:10] for string in t])) #more formatting

annual_issuance = [] #list same size m_cap
import datetime
for i in range(len(t_yr)):
    x = datetime.datetime.strptime(t_yr[i],'%Y-%m-%d')
    if x > datetime.datetime(2020,5,12): #12th of May 2020 third halvning
        annual_issuance.append(900*p[i])
    elif x > datetime.datetime(2016,7,9): #9th of July 2016 second halvning
        annual_issuance.append(1800*p[i])
    elif x > datetime.datetime(2012,11,28): #28th of November 2012 first halvning
        annual_issuance.append(3600*p[i])
    else:
        annual_issuance.append(7200*p[i])

s2f = np.array(m_cap)/np.array(annual_issuance)
print(s2f)


#need to get better data, from blockchain.com https://github.com/blockchain/api-v1-client-python

#plotting
import matplotlib.pyplot as plt 
plt.yscale('log')
plt.plot(t,p,s2f)
plt.show()


### adjust model for inflation, initial 'donation' 1M btc & 1% loss annually
#from easymoney.money import EasyPeasy #easmoney module 
#ep = EasyPeasy() #instance
#p_norm = []
#for j in range(len(p)):
#    p_norm.append(ep.normalize(amount=p[j], region="USA",from_year=t_yr[j],to_year=2019,pretty_print=False))