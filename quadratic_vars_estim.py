import utils.clean_data as clean_data
import numpy as np
import matplotlib.pyplot as plt
import time

# We choose to plot each estimator separately
def plotEstimatorHistoryLag_1(symbol,priceType):
    data=clean_data.getData(symbol)
    
    
    S=data.getColumn(priceType) # List [S(0),S(1),...,S(n)], len n
    S=np.array(S) # Array [S(0) S(1) ... S(n)], len n
    logS=np.log(S) # Array [log(S(0)) log(S(1)) ... log(S(n))], len n
    diff=np.diff(logS)  # Array [log(S(1))-log(S(0)) ... log(S(n))-log(S(n-1))], len n-1
    STild=diff**2 # Array [(log(S(1))-log(S(0)))^2 ... (log(S(n))-log(S(n-1)))^2], len n-1
    cumsumSTild=np.cumsum(STild) # Array [S_tild(0) S_tild(0)+S_tild(1)...sum of the S_tild(k)]
    
    symbolNumbers={
        "AAPL": 0,
        "AMZN": 1,
        "DJIA": 2,
        "BTC": 3
    }

    numberTradingDays=[82,80,82,119]
    xAxis=['t: trading days from 2 Jan 2020 at 09:31 to 1 May at 16:00',
           't: trading days from 6 Jan 2020 at 10:01 to 1 May at 16:00',
           't: trading days from 6 Jan 2020 at 09:31 to 1 May at 16:21',
           't: trading days from 5 Jan 2020 at 00:01 to 2 May at 00:01']
    
    n=len(cumsumSTild) 
    timeLine=np.linspace(0,numberTradingDays[symbolNumbers[symbol]], n)

    plt.plot(timeLine, cumsumSTild)
    plt.xlabel(xAxis[symbolNumbers[symbol]])
    plt.title('Integrated volatility estimator (with lag 1) history for {}\n(from {} prices)'.format(symbol,priceType.lower()))
    plt.ylabel('Value at time t')
    plt.grid(True)
    plt.show()
    
# Plotting estimator curves with a lag m, then to choose m=20
def plotEstimatorHistoryLag_m(symbol,priceType,m):
    data=clean_data.getData(symbol)

    
    S=data.getColumn(priceType) 
    S=np.array(S) 
    logS=np.log(S)  
    
    n=len(logS)
    numWindows=n//m 

    diffM=np.diff(logS[:m*numWindows].reshape(numWindows,m).T,axis=1).T.reshape(-1)
    STildM=diffM**2

    cumsumSTildM=np.cumsum(STildM)
    cumsumSTildM=cumsumSTildM/m

    
    symbolNumbers={
        "AAPL": 0,
        "AMZN": 1,
        "DJIA": 2,
        "BTC": 3
    }

    numberTradingDays=[82, 80, 82, 119]
    xAxis=[
        't: trading days from 2 Jan 2020 at 09:31 to 1 May at 16:00',
        't: trading days from 6 Jan 2020 at 10:01 to 1 May at 16:00',
        't: trading days from 6 Jan 2020 at 09:31 to 1 May at 16:21',
        't: trading days from 5 Jan 2020 at 00:01 to 2 May at 00:01'
    ]

    n_m=len(cumsumSTildM)
    timeLine=np.linspace(0,numberTradingDays[symbolNumbers[symbol]],n_m)

    plt.plot(timeLine,cumsumSTildM)
    plt.xlabel(xAxis[symbolNumbers[symbol]])
    plt.title('Integrated volatility estimator (with lag {}) history for {}\n(from {} prices)'.format(m,symbol, priceType.lower()))
    plt.ylabel('Value at time t')
    plt.grid(True)
    plt.show()    
    
    
    
    
    
                       # # # # # Applications # # # # #
                       

                       
startTime=time.time()
plotEstimatorHistoryLag_m("BTC","OPEN",20)
endTime=time.time()
executionTime=endTime-startTime
print("Execution time:",executionTime,"seconds")

# One can notice that time complexity is realy well optimized, due to the use
# of cumsum function





# It is now convenient to plot all of the estimator histories, for lag 1 and 
# lag m. 
"""
symbols=["AAPL","AMZN","DJIA","BTC"]
priceTypes=["OPEN","CLOSE","HIGH","LOW"]
for symbol in symbols:
    for priceType in priceTypes:
        plotEstimatorHistoryLag_1(symbol,priceType)
        plotEstimatorHistoryLag_m(symbol,priceType, 20)
"""        

# One can first notice that the plots are very similar, from a price type to
# another. It is because the different prices, for a given date/time, are quite
# similar

# We can also notice that plots with lag 1 and lag 20 are similar. In fact, the
# microstructure noise analysis made us choose the value of m=20 to stick as
# much as possible to the "reality", but it is difficult to note a big
# difference when consulting the different plots. Anyway, the plots with 
# lag m = 20 are the most adequate to represent the quadratic variation
# estimator by avoiding microstructure noise phenomena as more as possible. 












    

