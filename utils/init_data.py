import convert
import pandas as pd

class InitData:
    
    def __init__(self,fileName):
        self.fileName = fileName
        self.df = pd.read_csv(
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
    
    
    def multColumnFactor(self,columnName,factor):
        col=self.getColumn(columnName)
        col=[value * factor for value in col]
        self.df[columnName]=col

    
    def getCut(self):
        n=len(self.getColumn("DATE")) 
        cut=[0]
        for k in range(n-1):
            if self.getColumn("DATE")[k]!=self.getColumn("DATE")[k+1]:
                cut.append(k+1)
        cut.append(n)

        return cut      
      
        
    def fillMissingMinutes(self,symbol): 
        cut=self.getCut()

        m=len(cut)
        for j in range(m-2, -1, -1):
            for i in range(cut[j+1]-2,cut[j]-1,-1):
                
                date_i=str(self.getColumn("DATE")[i])
                time_i=str(self.getColumn("TIME")[i])
                t_i=int(convert.getTimeFromReference(date_i,time_i,"min"))
                
                date_i_plus_1=str(self.getColumn("DATE")[i+1])
                time_i_plus_1=str(self.getColumn("TIME")[i+1])
                t_i_bis=int(convert.getTimeFromReference(date_i_plus_1,time_i_plus_1,"min"))
                
                if t_i_bis-t_i>1:
                        missingMinutes=range(t_i+1,t_i_bis)
                        missingTimes=[convert.getTime(e,"min") for e in missingMinutes]
                        l=len(missingTimes)
                        
                        tickerList=[getTicker(symbol)] * l
                        perList = [1] * l
                        dateList = [self.getColumn("DATE")[i]] * l
                        timeList = missingTimes
                        openPriceList = [self.getColumn("OPEN")[i]] * l
                        closePriceList = [self.getColumn("CLOSE")[i]] * l
                        highList = [self.getColumn("HIGH")[i]] * l
                        lowList = [self.getColumn("LOW")[i]] * l
                        volList = [0] * l                            
                        
                        new_row = {
                            "TICKER": tickerList,
                            "PER": perList,
                            "DATE": dateList,
                            "TIME": timeList,
                            "OPEN": openPriceList,
                            "CLOSE": closePriceList,
                            "HIGH": highList,
                            "LOW": lowList,
                            "VOL": volList
                        }

                        self.df = self.df.loc[:i].append(pd.DataFrame(new_row), ignore_index=True).append(self.df.loc[i+1:], ignore_index=True)   
            

aaplData = InitData("./data/raw/AAPL.csv")
amznData = InitData("./data/raw/AMZN.csv")
djiaData = InitData("./data/raw/DJIA.csv")
btcData  = InitData("./data/raw/BTC.csv")


def getData(symbol):
   
    if symbol == 'AAPL':
        data=aaplData
    elif symbol == 'AMZN':
        data=amznData
    elif symbol == 'DJIA':
        data=djiaData   
    elif symbol == 'BTC':
        data=btcData
    
    return data


def getTicker(symbol):
    
    if symbol=='AAPL':
        ticker="US1.AAPL"
    elif symbol=='AMZN':
        ticker="US1.AMZN"
    elif symbol=='DJIA':
        ticker="D&J-IND"   
    elif symbol=='BTC':
        ticker="BTSX.BTC/USD"
    
    return ticker  


def getEarliestTradingTime(symbol):

    data=getData(symbol)
    
    dates=data.getColumn("DATE")
    times=data.getColumn("TIME")
        
    minGap=1439 # equivalent to 23:59:00 because 1 day = 1440 min
    n=len(times)
    for k in range(n):
        currentTime=convert.getTimeFromReference(dates[k],times[k],"min")
        midnightTime=convert.getTimeFromReference(dates[k],"000000","min")
        timeGap=currentTime-midnightTime
        if minGap>timeGap:
            minGap=timeGap
    earliestTime=convert.getTime(convert.getTimeFromReference(dates[0],"000000","min")+minGap,"min")
    
    return earliestTime


def getLatestTradingTime(symbol):
    
    data=getData(symbol)
    
    dates=data.getColumn("DATE")
    times=data.getColumn("TIME")   
    
    maxGap=0 # equivalent to 00:00:00
    n=len(times)
    for k in range(n):
        currentTime=convert.getTimeFromReference(dates[k],times[k],"min")
        midnightTime=convert.getTimeFromReference(dates[k],"000000","min")
        timeGap=currentTime-midnightTime
        if maxGap<timeGap:
            maxGap=timeGap
    latestTime=convert.getTime(convert.getTimeFromReference(dates[0],"000000","min")+maxGap,"min")
    
    return latestTime

        
def getNumberTradingDays(symbol):
   return len(getData(symbol).getCut())-1


def getMaxInternTimeGap(symbol):

    data=getData(symbol)
        
    dates=data.getColumn("DATE")
    times=data.getColumn("TIME")
    
    gap=1 # The underlaying unit is "min"
    n=len(dates)
    for k in range(n-1):
        currentTimeMeasure=convert.getTimeFromReference(dates[k],times[k],"min")
        nextTimeMeasure=convert.getTimeFromReference(dates[k+1],times[k+1],"min")
        if nextTimeMeasure-currentTimeMeasure>1 and dates[k]==dates[k+1]:
            gap=nextTimeMeasure-currentTimeMeasure
          
    return gap


def getMaxLeftExternTimeGap(symbol):
    
    data=getData(symbol)
    
    if symbol=="AAPL":
        expectedStartTime='093100'
    elif symbol=="AMZN":
        expectedStartTime='100100'
    elif symbol=="DJIA":
        expectedStartTime='093100'
    elif symbol=="BTC":
        expectedStartTime='000000'

    cut=data.getCut()
    
    maxStartGap=0
    m=len(cut)
    for j in range(m-2,-1,-1):
        
        startIndex=cut[j]
        startDate=str(data.getColumn("DATE")[startIndex])
        startTime=str(data.getColumn("TIME")[startIndex])
        startTimeMeasure=int(convert.getTimeFromReference(startDate,startTime,"min"))    
        diffStart=startTimeMeasure-int(convert.getTimeFromReference(startDate,expectedStartTime,"min"))
            
        if diffStart>maxStartGap:
            maxStartGap=diffStart
        
    return maxStartGap


def getMaxRightExternTimeGap(symbol):
    
    data=getData(symbol)
    
    if symbol=="AAPL":
        expectedEndTime='160000'
    elif symbol=="AMZN":
        expectedEndTime='160100'
    elif symbol=="DJIA":
        expectedEndTime='162100'
    elif symbol=="BTC":
        expectedEndTime='235900' 
    
    cut=data.getCut()
    
    maxEndGap=0
    m=len(cut)
    for j in range(m-2,-1,-1):
        
        if j==m-2: 
            endIndex=cut[j+1]
            endDate=str(data.getColumn("DATE")[endIndex-1])
            endTime=str(data.getColumn("TIME")[endIndex-1])
        else:                
            endIndex=cut[j+1]-1
            endDate=str(data.getColumn("DATE")[endIndex])
            endTime=str(data.getColumn("TIME")[endIndex])   
        endTimeMeasure=int(convert.getTimeFromReference(endDate,endTime,"min"))
        diffEnd=int(convert.getTimeFromReference(endDate,expectedEndTime,"min"))-endTimeMeasure
            
        if diffEnd>maxEndGap:
            maxEndGap=diffEnd
        
    return maxEndGap


def getAlmostCompleteTradingDaysBTC(margin):
    
    data=btcData
    cut=data.getCut()
    
    count=0
    m=len(cut)
    for j in range(m-2, -1, -1):

        startIndex=cut[j]
        startDate=str(btcData.getColumn("DATE")[startIndex])
        startTime=str(btcData.getColumn("TIME")[startIndex])
        
        if j==m-2: 
            endIndex=cut[j+1]
            endDate=str(btcData.getColumn("DATE")[endIndex-1])
            endTime=str(btcData.getColumn("TIME")[endIndex-1])
        else:                
            endIndex=cut[j+1]-1
            endDate=str(btcData.getColumn("DATE")[endIndex])
            endTime=str(btcData.getColumn("TIME")[endIndex])
        
        startTimeMeasure=int(convert.getTimeFromReference(startDate,startTime,"min"))    
        endTimeMeasure=int(convert.getTimeFromReference(endDate,endTime,"min"))
            
        diffStart=startTimeMeasure-int(convert.getTimeFromReference(startDate,"000000","min"))
        diffEnd=int(convert.getTimeFromReference(endDate,"235900","min"))-endTimeMeasure
            
        
        if diffStart+diffEnd>=margin:
            count+=1
        
    return count 





                    # # # # # Several operations # # # # #
                    
                    
                    
                    

# Due to stock splits with Apple and Amazon on 2022, we must adapt the price 
# values in the corresponding tables, thanks to multColumnFactor 
# (see more in the report)

aaplData.multColumnFactor("OPEN",0.2)
aaplData.multColumnFactor("CLOSE",0.2)
aaplData.multColumnFactor("HIGH",0.2)
aaplData.multColumnFactor("LOW",0.2)

amznData.multColumnFactor("OPEN",0.05)
amznData.multColumnFactor("CLOSE",0.05)
amznData.multColumnFactor("HIGH",0.05)
amznData.multColumnFactor("LOW",0.05)





# We can notice that the four tables don't have the same size

# print(len(aaplData.getColumn("OPEN")))
# AAPL 31 837 data records
# AMZN 24 360 data records  
# DJIA 33 701 data records
# BTC 165 299 data records

# AAPL, AMZN and DJIA are subject to financial markets, that are opened during 
# trading days, and closed during weekends. Then the size of BTC table is 
# obviously much larger than other ones.
# We can easily note that some times are not recorded in the tables (for 
# example one can go from a minute t_i to another minute t_i+2, without 
# considering t_i+1)
# It is important to fill those missing values to represent prices and 
# estimators, with acuracy and a good time complexity





# It is first convenient to estimate the maximum number of data records 
# we should have for a complete dataframe.

# Due to the shape of financial markets, we first determine what are the open and close
# times for AAPL, AMZN and DJIA. 
# It is the necessary to evaluate the earliest trade time and the last trade time 
# for each day and for each asset/index among AAPL, AMZN and DJIA

# print(getLatestTradingTime("AAPL"))

# AAPL : trading days beggin at 09:31:00 and end at 16:00:00 
# AMZN : trading days beggin at 10:01:00 and end at 16:01:00
# DJIA : trading days beggin at 09:31:00 and end at 16:21:00

# It is now easy to determine the maximum number of data recods necessary to represent
# each minutes of the trading days

# We just have to get the number of trading days represented for each asset/index

# However, one can easily notice that some trading days are not represented 
# in the data sets (for example Monday 2020/01/20). Thus let us use the 
# function getNumberTradingDays to get this data

# print(getNumberTradingDays('AAPL')) # 82 trading days
# print(getNumberTradingDays('AMZN')) # 80 trading days
# print(getNumberTradingDays('DJIA')) # 82 trading days
# print(getNumberTradingDays("BTC")) # 119 trading days

# AAPL : 82 trading days are represented 
# between 2020/01/02 (Thursday) and 2020/05/01 (Friday)
# and there are 390 minutes from 09:31:00 to 16:00:00
# => 82*390 = 31 980 data records after filling the missing values

# Same method for AMZN and DJIA :
# AMZN : 28 800 data records
# DJIA : 33 620 data records

# BTC is not subject to market cuts (by trading days and weekends)
# In Excel table : time from 2020/01/05, 00:01:00 to 2020/05/02, 00:01:00
# with 119 trading days represented, times 24*60=1440 => 171 360 data records

# Maximum number of data records for each asset/index after filling the missing values
# AAPL : 31 980
# AMZN : 30 600 
# DJIA : 34 850
# BTC : 171 360

# NB: It is indicated that we obtain the maximum number of data records
# It is because for two different trading days for a same asset, one can 
# beggin at 09:31:00, while the other can begin at 09:51:00 for example

# Hence, when filling the missing values for each asset/index, we shall obtain
# a number of records between the beggining values and the maximum value





# It is now time to construct the fillMissingMinutes method that we will apply 
# once, for ex : aaplData.fillMissingMinutes("AAPL") for AAPL, to fill the 
# missing values

# We fill the missing values for a given day, according to the start time
# and last time given
# Then the values, for each represented trading days, are uniformly distributed

aaplData.fillMissingMinutes("AAPL")
amznData.fillMissingMinutes("AMZN")
djiaData.fillMissingMinutes("DJIA")
btcData.fillMissingMinutes("BTC")

# print(len(btcData.getColumn("TIME")))
# btcData.fillMissingMinutes("BTC")
# print(btcData.getColumn("TIME"))
# print(len(btcData.getColumn("TIME")))

# The attributes <TICKER> and <PER> are not changed.
# VOL=0 (to stick as more as possible to the reality)
# DATE and TIME: added date and time values
# OPEN, CLOSE, HIGH and LOW: same prices as the previous one that was already 
# given in the table

# First, we can notice that the number of records for each new data frame is
# convenient (bigger than the first ones, but less than the maximum limit)
# AAPL : 31 956
# AMZN : 28 795 
# DJIA : 33 702
# BTC : 167 488

# To check whether the fillMissingMinutes method is worth, it is convenient to
# use to following function (max_time_gap) that returns the maximum time gap 
# between each data record

# print(getMaxInternTimeGap(symbol)) # returns 1, for every symbol
# That means that the fillMissingMinutes method is worth and we now have a 
# uniformly distributed set of times for each trading day





# It is also important to notice that some minutes are not represented in 
# the given data, between the theoretical start time and the effective start
# time of one trading days among others for the same asset/idex (and analog 
# for end time). Then, the purpose of the functions getMaxLeftExternTimeGap 
# and getMaxRightExternTimeGap is to quantify this effect to establish how 
# should we deal with this issue

# print(getMaxLeftExternTimeGap("AAPL")) # 24
# print(getMaxLeftExternTimeGap("AMZN")) # 1   
# print(getMaxLeftExternTimeGap("DJIA")) # 0 
# print(getMaxLeftExternTimeGap("BTC"))  # 971

# print(getMaxRightExternTimeGap("AAPL")) # 0
# print(getMaxRightExternTimeGap("AMZN")) # 2
# print(getMaxRightExternTimeGap("DJIA")) # 0
# print(getMaxRightExternTimeGap("BTC"))  # 1438

# For AAPL, AMZN and DJIA, the values of max_start and max_end are
# little enough to consider that the global time line is regular
# (that means that each trading day have almost the same number of records)

# Concerning BTC, the values represent about 16 hours and almost 24 hours,
# which means that some trading days are very partially represented
# Then it could be interesting to know the number of trading days, that are almost
# full

# The purpose of function getAlmostCompleteTradingDaysBTC is to evaluate the 
# number of trading days that do not satisfy the property of almost 
# completeness according to the argument margin, that is the number of minutes
# lacking to the trading day

# print(getAlmostCompleteTradingDaysBTC(1)) # returns 7
# print(getAlmostCompleteTradingDaysBTC(60)) # returns 6

# Interpretation : Over about 165 000 data records, only 7 are such that
# their lacking minutes are more than 1
# It means that we can keep the underlaying BTC data frame and consider
# that almost each trading day has the same number of data records, that are 
# strictly uniformly distributed





# After building such a new time line, it is possible to note that prices gaps
# are more important from one trading day to antoher, than between two 
# consecutive minutes in the same trading day
# However, when searching for Apple share or Amazon share charts on the web,
# this phenomena is notable. It is then convenient to know it, but we do not 
# have to change anything about this subject

# Moreover, some trading days, that belong to weeks, are not represented
# in the data sets
# But it would be to brutal to settle constant prices over one whole trading 
# day in order to fill the missing minutes. Then we just work with the given 
# days, expressing time by trading days in the different plots

# There are also some missing minutes between the expected start time of the 
# trading day, and the effective beggining (in the case of AAPL, sometimes
# the moments between 09:31:00 and 09:54:00 are not represented)
# The work with functions getMaxLeftExternTimeGap, getMaxLeftExternTimeGap
# and getAlmostCompleteTradingDaysBTC allows us to ignore this phenomena, 
# representing trading days with the given start and end times
# Hence, the purpose of the method fillMissingMinutes is to make the time 
# distribution, between each given start time and end time for each trading 
# day, uniform so that time line of the plots will be related to the real 
# time line very acurately





# Finally, we can trasnlate the new dataframes into csv files, that will be 
# used the fil clean_data, to define class CleanData

aaplData.df.to_csv("./data/pre_proc/aaplData.csv", index=False)
amznData.df.to_csv("./data/pre_proc/amznData.csv", index=False)
djiaData.df.to_csv("./data/pre_proc/djiaData.csv", index=False)
btcData.df.to_csv("./data/pre_proc/btcData.csv", index=False)

# The attributes of the four tables are <TICKER>,<PER>,<DATE>,<TIME>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>