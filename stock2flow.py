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
        for i in range(0,len(self.data),10): #change to 1 for better accuracy, slower execution 
            p.append(self.data[i][0]['price'])
            t.append(self.data[i][0]['timestamp'])
            m_cap.append(self.data[i][0]['market_cap'])
        print('Extraction Completed')
        return p,t,m_cap
p,t,m_cap = extractor(data).mlist() #storin price, timestamp & marketcap as lists
circ_supply = np.array(m_cap)/np.array(p) #use price & marketcap to get circulating supply (as numpy array)




### calculate stock to flow model
#(circulating number of btc * pnorm) / annual issuance


#plotting
import matplotlib.pyplot as plt 
plt.yscale('log')
plt.plot(t,p)
plt.show()


### Part 5: adjust model for inflation, initial 'donation' 1M btc & 1% loss annually
#adjusting BTC price for inflation 
#from easymoney.money import EasyPeasy #easmoney module 
#ep = EasyPeasy() #instance
#t_yr = list(map(int,[string[:4] for string in t])) #year to integer transformation
#p_norm = []
#for j in range(len(p)):
#    p_norm.append(ep.normalize(amount=p[j], region="USA",from_year=t_yr[j],to_year=2019,pretty_print=False))