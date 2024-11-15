import convert
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class CleanData:
    
    def __init__(self,fileName):
        self.fileName=fileName
        self.df=pd.read_csv(
            fileName,
            header=None,
            names=["TICKER", "PER", "DATE", "TIME", "OPEN", "HIGH", "LOW", "CLOSE", "VOL"],
            dtype={
                "TICKER": str,
                "PER"   : int,
                "DATE"  : str,
                "TIME"  : str,
                "OPEN"  : float,
                "HIGH"  : float,
                "LOW"   : float,
                "CLOSE" : float,
                "VOL"   : int
            }
        )


    def getColumn(self,columnName):
        return self.df[columnName].tolist()
    

    def getCut(self):
        n=len(self.getColumn("DATE")) 
        cut=[0]
        for k in range(n-1):
            if self.getColumn("DATE")[k]!=self.getColumn("DATE")[k+1]:
                cut.append(k+1)
        cut.append(n)

        return cut

aaplData=CleanData("./data/pre_proc/aaplData.csv")
amznData=CleanData("./data/pre_proc/amznData.csv")
djiaData=CleanData("./data/pre_proc/djiaData.csv")
btcData =CleanData("./data/pre_proc/btcData.csv")


def getData(symbol):
   
    if symbol=='AAPL':
        data=aaplData
    elif symbol=='AMZN':
        data=amznData
    elif symbol=='DJIA':
        data=djiaData   
    elif symbol=='BTC':
        data=btcData
    
    return data

def plotDatesFromCutValues(symbol):
    
    data=getData(symbol)   
    cut=data.getCut()
    
    daysLine=range(len(cut)-1)
    datesFromCut=[convert.getTimeFromReference(data.getColumn("DATE")[c],"000000","days") for c in cut[:-1]]
    
    symbolNumbers = {
        "AAPL": 0,
        "AMZN": 1,
        "DJIA": 2,
        "BTC": 3
    }
    xAxis=['trading days from 2 Jan 2020 at 09:31 to 1 May at 16:00\n (clean data time line)',
           'trading days from 6 Jan 2020 at 10:01 to 1 May at 16:00\n (clean data time line)',
           'trading days from 6 Jan 2020 at 09:31 to 1 May at 16:21\n (clean data time line)',
           'trading days from 5 Jan 2020 at 00:01 to 2 May at 00:01\n (clean data time line)']   
    
    plt.plot(daysLine, datesFromCut)
    plt.title('Uniformity plot for {} real and clean data time lines'.format(symbol))
    plt.xlabel(xAxis[symbolNumbers[symbol]])
    plt.ylabel('days spent in the real time line\n (real time line)')
    plt.grid(True)
    plt.show()





                   # # # # # Applications # # # # #
                   



                   
# It is convenient to check whether the clean data gives an almost constant
# time line, ie a time line, given by the columns DATE and TIME, that reflects
# well the real time. With such a property, we can affirm that the trading days
# are uniformy distributed in the real time line. Moreover, we have built 
# the clean data so that the records are also uniformly distributed in each
# trading days. That means that the plots given by the clean data time line 
# are analog to plots that would have been produced with a continuous 
# time line. 

# An efficient way to check this unifomity property is to represent the 
# evolution to the real time, linked with the clean data time line by, for 
# example, plotting the dates represented by the values in the list cut for 
# each asset, with Y axis the real time in days spent since reference time, 
# and X axis the number of trading days spent since the same reference time
# trading days 

# plotDatesFromCutValues("AAPL")
# plotDatesFromCutValues("AMZN")
# plotDatesFromCutValues("DJIA")                                    
# plotDatesFromCutValues("BTC")

# The results: The four plots, for each asset/index, show an almost linear
# relationship between the real spent time, and the spent trading days. That
# shows that with a global point of view, the trading days are uniformly
# distributed. This result was obviously expected, since there is only a few
# number of lacking trading days. 

# The plots for BTC and the other assets/index are different. It is because
# AAPL, AMZN and DJIA are subject to financial markets, then there are not
# trading days during weekends (that explains the little regular jumps of
# the curve), whereas BTC is not submited to financial market, hence there is 
# a perfect linear (and even equality) between real days line and clean data
# time line. 

# Finally, the linear aspect of all of the curves allows us to consider 
# real time line and clean data time line as equivalent, that is convenient 
# to produce plots that stick as more as possible to the "reality".




        

