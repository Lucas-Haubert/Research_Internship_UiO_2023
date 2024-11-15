import utils.clean_data as clean_data
import numpy as np
import matplotlib.pyplot as plt

# We will plot each estimators serie separately
def plotEstimatorAtFinalTimeForSeveralLagValues(symbol,priceType,M):
    
    data=clean_data.getData(symbol)
    
    mScale=range(1,M)  
    V_mValues = [V(data,priceType,m) for m in mScale]                
    
    plt.plot(mScale, V_mValues)
    symbolNumbers = {
        "AAPL": 0,
        "AMZN": 1,
        "DJIA": 2,
        "BTC": 3
    }
    inTitles=['Apple shares',
              'Amazon shares',
              'Dow Jones IA index',
              'Bitcoin value']
    plt.title('Final time integrated volatility estimators for {}\nusing different lags (from {} prices)'.format(inTitles[symbolNumbers[symbol]],priceType.lower()))
    plt.xlabel('Lag m')
    plt.ylabel('Value for lag m')
    plt.grid(True)
    plt.show()   

# Computing the value of V_m, that is the lag = m version of the quadratic
# variation estimator of the square integrated volatility
def V(data,priceType,m):
    S=data.getColumn(priceType)
    S=np.array(S)
    logReturns=np.log(S[m:]/S[:-m])  
    s=np.sum(logReturns**2)/m
    return s





                       # # # # # Applications # # # # #





# It is convenient to plot all of the estimators at final time, for
# lag values from 1 to 75. The maximum computed lag is 75 so that we can 
# obtain a large vision of the behaviour of V_m, even if we expect to get a 
# stabilized value for m between 15 and 30 (see Jacod & Aït-Sahalia) 
"""
symbols=["AAPL","AMZN","DJIA","BTC"]
priceTypes=["OPEN","CLOSE","HIGH","LOW"]
for symbol in symbols:
    for priceType in priceTypes:
        plotEstimatorAtFinalTimeForSeveralLagValues(symbol,priceType,75)
"""



   
# For each asset/index, one can notice that the estimator of the integrated 
# volatility at final time decreases when m tends to infinity, that is normal 
# since V_m is defined according time gaps

# To avoid such a decrease, we have to consider m fewer. According to the limit
# relationship between the estimator and the integrated volatility, 
# one would even want to take m as little as possible.
# But there exist some microstructure noise phenomena when the time mesh gets 
# too little when recording experimental data (see Chapter 2 in the report).
# Then we must find an equilibrium value for m, such that the ploted curves
# get stabilized. For this reason, we will work with m=20.

# NB: m=20 is reassuring value, since J. Jacod and Y. Aït-Sahalia suggest to 
# consider a time lag between 15 and 30 minutes (and because we have
# previously cleaned the data so that each jump between two data records
# represents a one-minute jump)
# Hence, giving the shape of our data sets, and the fact that times are almost
# uniformly distributed, one can consider that m=20 matches Jacod and 
# Aït-Sahalia suggestion 

# In file quadratic_vars_estim, we generate a plot for the corresponding 
# estimators with lag m, then we choose m=20





# NB: One can notice that the values for AAPL, AMZN and BTC with OPEN / CLOSE 
# prices are roughly increasing when m tends to 0, that is obvious, 
# regarding the definition of V_m, and kwowing that OPEN et CLOSE columns
# represent "real prices"
# Hence, this is not the case for DJIA. The reason is the following: DJIA is
# an index, while AAPL,AMZN and BTC represent proper assets. DJIA being 
# composed with 30 asset values, from which we extracted a weighted mean, the
# microstructure components of each asset make the DJIA one very close to zero
# (since we are adding a large number for noise processes)





# NB : We can also notice that for high (resp. low) prices, that represent 
# the maximum (resp. minimum) prices over a given trading period of one minute,
# the values of V_m are decreasing when m is little (about less than 5) and m
# goes to 0. This phenomena is not observed in the case of open and close
# prices. The purpose of the project is not to study the different behaviours
# of the estimators of integrated volatility. Hence, it is just convenient
# to note that open/close prices do not belong to the same class of prices as
# high/low prices. It is then not surprising to not some different propoerties
# according to the prices we are working on. Note : In the following, the test
# focuses on open prices. 























