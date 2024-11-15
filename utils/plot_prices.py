import clean_data
import convert
import numpy as np
import matplotlib.pyplot as plt
import time

# Getting the index associated to the biggest moment before t
def binarySearch(t, dates, times, unit):
    start=0
    end=len(dates)-1
    n=-1
    
    while start<=end:
        mid=(start + end) // 2
        midTime=convert.getTimeFromReference(dates[mid],times[mid],unit)
        
        if midTime>t:
            end=mid-1
        else:
            n=mid
            start=mid+1
    
    return n


def plotPrices(startDate,startTime,endDate,endTime,priceType,symbol,unit):
    
    data=clean_data.getData(symbol)
        
    S=data.getColumn(priceType)
            
    dates=data.getColumn("DATE")
    times=data.getColumn("TIME")
    
    startTimeMeasure=convert.getTimeFromReference(startDate,startTime,unit)
    s=binarySearch(startTimeMeasure,dates,times,unit)
    
    endTimeMeasure=convert.getTimeFromReference(endDate,endTime,unit)
    e=binarySearch(endTimeMeasure,dates,times,unit) 
    
    S=S[s:e+1] 
    
    diffTime=endTimeMeasure-startTimeMeasure
    timeLine=np.linspace(0,int(diffTime),e-s+1)
    
    plt.plot(timeLine, S)
    literalStartDateTime=convert.getLiteralDateAndTime(startDate, startTime)
    literalEndDateTime=convert.getLiteralDateAndTime(endDate, endTime)
    plt.xlabel('t: {} from {} to {}'.format(unit,literalStartDateTime,literalEndDateTime))
    symbolNumbers = {
        "AAPL": 0,
        "AMZN": 1,
        "DJIA": 2,
        "BTC": 3
    }
    inTitles=['Apple Share Prices',
              'Amazon Share Prices',
              'Dow Jones Stock Market Performance',
              'Bitcoin Price History']
    plt.title('{} (USD)   ({} prices)'.format(inTitles[symbolNumbers[symbol]],priceType.lower()))
    plt.ylabel('Value at time t')
    plt.grid(True)
    plt.show()
    
    
    
    
    
                    # # # # # Applications # # # # #
                    
                    
                    
startTime=time.time()
plotPrices("20200105","101000","20200415","111000","OPEN","BTC","days")
endTime=time.time()
executionTime=endTime-startTime
print("Execution time:",executionTime,"seconds")





# When start time and end time are too close, the plot is not that convenient 
# with "days" unit, that is quite understandable, regarding the construction 
# of s and e
# However, the plots are all right when one precise "hours" or "min" for unit

# One can choose to work on open, close, high or low prices.
# The results are quite similar, but it is then possible to choose the price 
# type that we want












