import utils.clean_data as clean_data
import quadratic_vars_estim_bis
import numpy as np
from scipy.stats import norm
import time


nValues = {"AAPL": 31955,"AMZN": 28794,"DJIA": 33701,"BTC": 167487}

symbols=["AAPL","AMZN","DJIA","BTC"]
logPrices={}
for symbol in symbols:
    data=clean_data.getData(symbol)
    S=data.getColumn("OPEN")
    S=np.array(S)
    logS=np.log(S)
    logPrices[symbol]=logS
   

def f(x):
    if -1<=x and x<=1:
        return (15/16)*(x**2-1)**2
    else:
        return 0
    
    
def delta(symbol):
    n=nValues[symbol]
    return 1/n


def h(symbol,case):
    if case=="nonoise":
        return (delta(symbol)**(1/3))/np.log(1/delta(symbol))
    if case=="noise":
        return delta(symbol)**(1/6)
# Note: Some multiplying factor can be applied in the return lines (cf Chapter
# 3 in the report)


def fDirac(symbol,case,x):
    return (1/h(symbol,case))*f(x/h(symbol,case))


def k(symbol):
    value=int(np.log(1/delta(symbol))/np.sqrt(delta(symbol)))
    if value%2==0:
        return value
    else:
        return value+1
    

def v(symbol,case):
    objects = {"AAPL": clean_data.aaplData,
               "AMZN": clean_data.amznData,
               "DJIA": clean_data.djiaData,
               "BTC" : clean_data.btcData}
    if case=="nonoise":
        gamma=2*np.sqrt(quadratic_vars_estim_bis.V(objects[symbol],"OPEN",1))
        return gamma*np.sqrt(delta(symbol))
    if case=="noise":
        gamma=2*np.sqrt(quadratic_vars_estim_bis.V(objects[symbol],"OPEN",20))
        return gamma*np.sqrt(k(symbol)*delta(symbol))
    

# The power r which regulates the weights of the estimators of U(x,p)
# is given in the arguments of the dedicated functions

def m(p):
    moment=norm.moment(p,loc=0,scale=1)
    return moment


def barY(symbol,i):
    observations=logPrices[symbol]
    kSymbol=k(symbol)
    s=np.sum(observations[i:i+kSymbol])
    result=s/kSymbol
    return result


def tildY(symbol,i):
    observations=logPrices[symbol]
    kSymbol=k(symbol)
    barValueY=barY(symbol,i)
    s=np.sum((observations[i:i+2*kSymbol]-barValueY)**2)
    result=s/(kSymbol**2)
    return result


def estimatorU(symbol,case,x,p):
    threshold=v(symbol,case)
    logS=logPrices[symbol]
    
    if case=="nonoise":
        diff=np.abs(logS[1:]-logS[:-1])  
        indicator=np.where(abs(diff)<=threshold,1,0)
        fDiracVectorized=np.vectorize(lambda value: fDirac(symbol,"nonoise",value))
        s=np.sum(fDiracVectorized(logS[1:]-x)*(diff**p)*indicator) 
        u=(delta((symbol))**(1-p/2))*(1/m(p))*s
        return u
    
    if case=="noise":
        n=nValues[symbol]
        s=0
        if p==0:
            for i in range(1,int(n/(2*k(symbol)))-1):
                dirac=fDirac(symbol,"noise",barY(symbol,2*i*k(symbol))-x)
                diff=barY(symbol,2*i*k(symbol))-barY(symbol,(2*i+1)*k(symbol))
                if abs(diff)<=threshold:
                    s+=dirac
            u=k(symbol)*delta(symbol)*s
            return u
        if p==2:
            for i in range(1,int(n/(2*k(symbol)))-1):
                dirac=fDirac(symbol,"noise",barY(symbol,2*i*k(symbol))-x)
                diff=barY(symbol,2*i*k(symbol))-barY(symbol,(2*i+1)*k(symbol))
                factor=(diff**2)-tildY(symbol,2*i*k(symbol))
                if abs(diff)<=threshold:
                    s+=dirac*factor
            u=3*s
            return u
        if p==4:
            for i in range(1,int(n/(2*k(symbol)))-1):
                dirac=fDirac(symbol,"noise",barY(symbol,2*i*k(symbol))-x)
                diff=barY(symbol,2*i*k(symbol))-barY(symbol,(2*i+1)*k(symbol))
                tild=tildY(symbol,2*i*k(symbol))
                factor=(diff**4)-6*(diff**2)*tild+3*(tild**2)
                if abs(diff)<=threshold:
                    s+=dirac*factor
            u=(3/(k(symbol)*delta(symbol)))*s
            return u

# Then, if u0=estimatorU(symbol,case,x,0), and same definition for u2 and u4,
# then one can directly compute and estimator of S^x as 2*(u0*u4-u2**2)

# Finite set Xhi of real numbers containing the range of the process X

# Dictionary with values [minimum log(price),maximum log(price)] 
dictionaryMinMax={}
symbols=["AAPL","AMZN","DJIA","BTC"]
data={"AAPL":clean_data.aaplData,"AMZN":clean_data.amznData, 
      "DJIA":clean_data.djiaData,"BTC":clean_data.btcData}
priceTypes=["OPEN","CLOSE","HIGH","LOW"]
for symbol in symbols:
    dictionaryMinMax[symbol]={}
    for priceType in priceTypes:
        logS=np.log(data[symbol].getColumn(priceType))
        minimum=min(logS)
        maximum=max(logS)
        L=[minimum,maximum]
        dictionaryMinMax[symbol][priceType]=L


def Xhi(symbol,case):
          
    extremeValues=dictionaryMinMax[symbol]["OPEN"]
    start=extremeValues[0]-h(symbol,case)
    end=extremeValues[1]+h(symbol,case)
        
    if (end-start)/(2*h(symbol,case))-int((end-start)/(2*h(symbol,case)))!=0:
        N=int((end-start)/(2*h(symbol,case))) 
    else:
        N=int((end-start)/(2*h(symbol,case)))-1
    alpha=start
    bêta=(end-start)/N
    
    grid=np.array([alpha+i*bêta for i in range(N+1)])
    
    return grid


def estimatorsPhiSigma(symbol,case,r):
    estimatorPhi=0
    estimatorSigma=0
    for x in Xhi(symbol,case): 
        u0=estimatorU(symbol,case,x,0)
        u2=estimatorU(symbol,case,x,2)
        u4=estimatorU(symbol,case,x,4)
        estimatorPhi+=(u2**r)*2*(u0*u4-u2**2)
        estimatorSigma+=u0*(u4**2)*(u2**(2*r))
    squareIntegratedKernelFunction=5/7
    estimatorSigma=(8/3)*squareIntegratedKernelFunction*estimatorSigma
    return [estimatorPhi,estimatorSigma]
    

def T(symbol,case,r):
    if case=="nonoise": 
        squareRoot=np.sqrt(h(symbol,case)/(delta(symbol)))
    if case=="noise": 
        squareRoot=np.sqrt(h(symbol,case)/(k(symbol)*delta(symbol)))
    [estimatorPhi,estimatorSigma]=estimatorsPhiSigma(symbol,case,r)
    ratio=estimatorPhi/np.sqrt(estimatorSigma)
    return squareRoot*ratio

# Alpha-quantile of the law N(0,1) (that is z_{1-alpha/2})
def alphaQuantile(alpha):
    return norm.isf(alpha/2)

# Alternative methods

def barYm(symbol,i,m):
    observations=logPrices[symbol]
    s=np.sum(observations[i:i+m])
    result=s/m
    return result

# Getting the log-prices with lag m and the pre-averaged log-prices
symbols=["AAPL","AMZN","DJIA","BTC"]
lagM=20
preAveragedLogPricesWithK={}
preAveragedLogPricesWithLagM={}
preAveragedLogPricesOneByOne={}
logPricesWithLagM={}
for symbol in symbols:
    n=nValues[symbol]
    preAveragedLogPricesWithK[symbol]=np.array([barY(symbol,i*k(symbol)) for i in range(0,int(n/k(symbol))+1)])
    preAveragedLogPricesWithLagM[symbol]=np.array([barYm(symbol,i*20,20) for i in range(0,int(n/lagM)+1)])
    preAveragedLogPricesOneByOne[symbol]=np.array([barY(symbol,i) for i in range(0,int(n)+1)])   


def estimatorUNoise(symbol,x,p,method):
    threshold=v(symbol,"nonoise")
    if method=="1a":
        P=preAveragedLogPricesWithK[symbol] 
        diff=np.abs(P[1:]-P[:-1])
        indicator=np.where(abs(diff)<=threshold,1,0)
        fDiracVectorized=np.vectorize(lambda value: fDirac(symbol,"nonoise",value))
        s=np.sum(fDiracVectorized(P[1:]-x)*(diff**p)*indicator) 
        u=(delta((symbol))**(1-p/2))*(1/m(p))*s
        return u
    elif method=="1b":
        P=preAveragedLogPricesWithLagM[symbol] 
        diff=np.abs(P[1:]-P[:-1])
        indicator=np.where(abs(diff)<=threshold,1,0)
        fDiracVectorized=np.vectorize(lambda value: fDirac(symbol,"nonoise",value))
        s=np.sum(fDiracVectorized(P[1:]-x)*(diff**p)*indicator) 
        u=(delta((symbol))**(1-p/2))*(1/m(p))*s
        return u
    elif method=="2":
        P=logPrices[symbol]
        diff=np.abs(P[lagM:]-P[:-lagM])
        indicator=np.where(abs(diff)<=threshold,1,0)
        fDiracVectorized=np.vectorize(lambda value: fDirac(symbol,"nonoise",value))
        s=np.sum(fDiracVectorized(P[:-lagM]-x)*(diff**p)*indicator) 
        u=(delta((symbol))**(1-p/2))*(1/m(p))*s
        return u/lagM    
    
        
def estimatorsPhiSigmaNoise(symbol,r,method):
    estimatorPhi=0
    estimatorSigma=0  
    for x in Xhi(symbol,"nonoise"): 
        u0=estimatorUNoise(symbol,x,0,method)
        u2=estimatorUNoise(symbol,x,2,method)
        u4=estimatorUNoise(symbol,x,4,method)
        estimatorPhi+=(u2**r)*2*(u0*u4-u2**2)
        estimatorSigma+=u0*(u4**2)*(u2**(2*r))
    squareIntegratedKernelFunction=5/7
    estimatorSigma=(8/3)*squareIntegratedKernelFunction*estimatorSigma
    return [estimatorPhi,estimatorSigma]


def TNoise(symbol,r,method):
    squareRoot=np.sqrt(h(symbol,"nonoise")/(delta(symbol)))
    [estimatorPhi,estimatorSigma]=estimatorsPhiSigmaNoise(symbol,r,method)
    ratio=estimatorPhi/np.sqrt(estimatorSigma)
    return squareRoot*ratio    





                       # # # # # Applications # # # # #
                       
                      
                       
                      

# One of the most important points, in the definition of the tuning parameters
# is to deal with the so-called "delta_n" time lag, which theoretically tends
# to 0 when n (that is the number of observations) tends to infinity. In fact, 
# the best we can do is to consider the consecutive times that are recorded in
# the objects of the class CleanData. 

# Note : Filling the missing values was a great idea. Indeed, in addition to 
# obtain more accurate results when it comes to displaying charts or 
# studying the estimators of the square integrated volatility, it is possible 
# to get as close as possible to the modeling proposed by J. Jacod and 
# Y. AÏt-Sahalia.

# In this situation, we have to settle this so-called "delta_n" equal to 1 min. 

# BUT : One have to be careful when it comes to define some tuning parameters, 
# like "h_n". J and Y suggest something asymptoticaly similar to 
# (delta_n)^1/3 / log(1/delta_n). It is obvious that it is impossible to use 
# such a definition with delta_n equal to 1. In fact, one minute is 
# represented by the relative time 1/n, since n minutes are represented in the 
# asset / index data set and the observation time line [0,T] is equal to [0,1] 
# (relative times)




# Some comments about the choice of the tuning parameters

# f: Explicit translation of Jacod and Aït-Sahalia's suggestion
# The kernel function f is useful in the definition of the estimator of U(x,p)

# h: Also directly given by J. and A-S.
# NB: Denote g_n=(delta_n**(1/3))/np.log(1/delta_n) in the "noise" case, 
# and delta_n**(1/6) in the "nonoise" case. In fact, Jacod and AÏt-Sahalia
# define h_n as asymptotically equivalent to g_n, given a multiplying
# constant, i.e. : h_n=O(g_n) and g_n=O(h_n). We must then multiply g_n
# in the function h (for example by writing 0.1*delta(symbol)**(1/6) instead
# of delta(symbol)**(1/6), in order to multiply by approximatively 10 the
# number of elements in Xhi)

# fDirac: Dirac mass on 0 from the kernel function f. Depending on the 
# bandwidth h, the function fDirac is useful to give importance to the 
# proximity between the process value and x in Xhi

# k: Useful to manage with microstructure noise. J and A-S only give a real
# term to definie k. However, it must be even, in order to construct the 
# estimators for U in the "noise" case. Hence, the definition of k is a little
# bit changed. In fact, this is the following even integer after
# log(1/delta_n)/sqrt(delta_n). However, such a new definition keeps the 
# limit properties (more details in the report)

# v: The threshold, given by v, is important to deal with an hypothetical 
# "lack of continuity" of the process X. In fact, it is useful when it comes
# to deal with jumps (big jumps with low intensity). The shape of v depends on 
# the case (with or without noise). The value of gamma is given as a function 
# of the estimator of the integrated volatility (more details in the report)

# Xhi: Xhi is defined as a grid with respect to the constraints given by 
# J. and A-S. It is also interesting to notice the number of elements of Xhi
# depending on each symbol and each case

# One can notice that there are a lot of elements in the "nonoise" case
# In fact, it is due to the condition of minimum distance between two 
# consecutive points in the grid, defined according to the bandwidth, that 
# depends itself on the case (h being bigger in the noise case, in order to 
# deal with microstructure noise phenomena). Hence, there are much more points 
# in the grid Xhi in the "nonoise" case. 





# Results of the test (values of the test statistic T)


# In the "nonoise" case (without considering micro-structure noise) :
    
"""
startTime=time.time()
print("Test statistics for each asset/index in the non noisy case :")
print("")
print("AAPL with ",len(Xhi("AAPL","nonoise"))," elements in Xhi :",T("AAPL","nonoise",0))
print("AMZN with ",len(Xhi("AMZN","nonoise"))," elements in Xhi :",T("AMZN","nonoise",0))
print("DJIA with ",len(Xhi("DJIA","nonoise"))," elements in Xhi :",T("DJIA","nonoise",0))
print(" BTC with ",len(Xhi("BTC","nonoise"))," elements in Xhi  :",T("BTC","nonoise",0))
print("")
print("Xhi of AAPL goes from ",dictionaryMinMax["AAPL"]["OPEN"][0]-h("AAPL","nonoise")," to ",dictionaryMinMax["AAPL"]["OPEN"][1]-h("AAPL","nonoise"))
print("Xhi of AMZN goes from ",dictionaryMinMax["AMZN"]["OPEN"][0]-h("AMZN","nonoise")," to ",dictionaryMinMax["AMZN"]["OPEN"][1]-h("AMZN","nonoise"))
print("Xhi of DJIA goes from ",dictionaryMinMax["DJIA"]["OPEN"][0]-h("DJIA","nonoise")," to ",dictionaryMinMax["DJIA"]["OPEN"][1]-h("DJIA","nonoise"))
print("Xhi of BTC  goes from ",dictionaryMinMax["BTC"]["OPEN"][0]-h("BTC","nonoise")," to ",dictionaryMinMax["BTC"]["OPEN"][1]-h("BTC","nonoise"))
print("")
endTime=time.time()
executionTime=endTime-startTime
print("Execution time:", executionTime, "seconds")
"""
    
# As stated in the report (see Chapter 4), the values of T are sufficient 
# to reject the null hypothesis

# NB : The number of elements in Xhi is big enough to consider that the 
# statistical test is accurate


# BUT, since the time distance between two data records is one minute, it is 
# relevant to consider that we are facing micro-structure noise (indeed, the 
# plots of the diffent values of the estimators of the integrated volatility,
# according to a lag m, can show it)

# Alternative method 1 in the "noise" case : pre-average the data, 
# then process with the "nonoise" formula (by using barY(i*k) for 1a, 
# barY(i*k) for b and barYm(i*m) for 1b)
  

# Alternative method 2 in the "noise" case : Consider a lag m, and then use
# the "nonoise" process by defining the estimators of U(x,p)_n as the mean
# of the objects U(x,p)_n depending on k (integer between 0 and m-1) that 
# represent the estimators according to a limiting number of data records

#Jacod's suggestion
"""
startTime=time.time()
print("Test statistics for each asset/index in the noisy case with T:")
print("")
print("AAPL with ",len(Xhi("AAPL","noise"))," elements in Xhi :",T("AAPL","noise",0))
print("AMZN with ",len(Xhi("AMZN","noise"))," elements in Xhi :",T("AMZN","noise",0))
print("DJIA with ",len(Xhi("DJIA","noise"))," elements in Xhi :",T("DJIA","noise",0))
print(" BTC with ",len(Xhi("BTC","noise"))," elements in Xhi  :",T("BTC","noise",0))
print("")
print("Xhi of AAPL goes from ",dictionaryMinMax["AAPL"]["OPEN"][0]-h("AAPL","noise")," to ",dictionaryMinMax["AAPL"]["OPEN"][1]-h("AAPL","noise"))
print("Xhi of AMZN goes from ",dictionaryMinMax["AMZN"]["OPEN"][0]-h("AMZN","noise")," to ",dictionaryMinMax["AMZN"]["OPEN"][1]-h("AMZN","noise"))
print("Xhi of DJIA goes from ",dictionaryMinMax["DJIA"]["OPEN"][0]-h("DJIA","noise")," to ",dictionaryMinMax["DJIA"]["OPEN"][1]-h("DJIA","noise"))
print("Xhi of BTC  goes from ",dictionaryMinMax["BTC"]["OPEN"][0]-h("BTC","noise")," to ",dictionaryMinMax["BTC"]["OPEN"][1]-h("BTC","noise"))
print("")
endTime=time.time()
executionTime=endTime-startTime
print("Execution time:", executionTime, "seconds")
"""

# Use of one alternative method  
"""
startTime=time.time()
print("Test statistics for alternative method 2:")
print("")
print("AAPL with ",len(Xhi("AAPL","nonoise"))," elements in Xhi :",TNoise("AAPL",0,"2"))
print("AMZN with ",len(Xhi("AMZN","nonoise"))," elements in Xhi :",TNoise("AMZN",0,"2"))
print("DJIA with ",len(Xhi("DJIA","nonoise"))," elements in Xhi :",TNoise("DJIA",0,"2"))
print(" BTC with ",len(Xhi("BTC","nonoise"))," elements in Xhi  :",TNoise("BTC",0,"2"))
endTime=time.time()
executionTime=endTime-startTime
print("Execution time:", executionTime, "seconds")
"""

# In Sections 4.2 and 4.3 of the report, reasonings on the values of T and the
# mathematical framework on the test can lead to the following conclusion :
# the null hypothesis is rejected


        
    


