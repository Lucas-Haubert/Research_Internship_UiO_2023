import time

# Getting spent time in unit "unit" from 2020/01/02 at 09:31:00 for a given data/time
def getTimeFromReference(date,clockTime,unit):
    
    dateStruct=time.strptime(date,"%Y%m%d")
    timeStruct=time.strptime(clockTime,"%H%M%S")
    
    specifiedTime=time.struct_time((dateStruct.tm_year, dateStruct.tm_mon, dateStruct.tm_mday,
                                       timeStruct.tm_hour, timeStruct.tm_min, timeStruct.tm_sec,
                                       timeStruct.tm_wday, timeStruct.tm_yday, timeStruct.tm_isdst))
    
    referenceTime=time.mktime(time.strptime("20200102 093100","%Y%m%d %H%M%S"))
    specifiedTime=time.mktime(specifiedTime)
    
    timeDifference=specifiedTime-referenceTime
    
    if unit=="min":
        secondsPerMin=60
        return timeDifference/secondsPerMin
    elif unit=="hours":
        secondsPerHour=60*60
        return timeDifference/secondsPerHour
    elif unit=="days":
        secondsPerDay=60*60*24
        return timeDifference/secondsPerDay
    else:
        return None

# print(getTimeFromReference("20200102", "103100", "min")) # returns 60.0

# Getting the current date after waiting timeMeasure unit from 2020/01/02 at 09:31:00
def getDate(timeMeasure,unit):

    if unit=="min":
        secondsPerMin=60
        timeMeasure=timeMeasure * secondsPerMin
    elif unit=="hours":
        secondsPerHour=60*60
        timeMeasure=timeMeasure * secondsPerHour
    elif unit=="days":
        secondsPerDay=60*60*24
        timeMeasure=timeMeasure * secondsPerDay
    else:
        return None
    
    referenceTime=time.mktime(time.strptime("20200102 093100", "%Y%m%d %H%M%S"))
    finalTime=referenceTime + timeMeasure
    finalStruct=time.localtime(finalTime)
    finalDate=time.strftime("%Y%m%d", finalStruct)
    
    return finalDate

# Getting the current time after waiting timeMeasure unit from 2020/01/02 at 09:31:00
def getTime(timeMeasure,unit):

    if unit=="min":
        secondsPerMin=60
        timeMeasure=timeMeasure * secondsPerMin
    elif unit=="hours":
        secondsPerHour=60*60
        timeMeasure = timeMeasure * secondsPerHour
    elif unit=="days":
        secondsPerDay=60*60*24
        timeMeasure = timeMeasure * secondsPerDay
    else:
        return None
    
    referenceTime=time.mktime(time.strptime("20200102 093100", "%Y%m%d %H%M%S"))
    finalTime=referenceTime + timeMeasure
    finalStruct=time.localtime(finalTime)
    finalTime=time.strftime("%H%M%S", finalStruct)
    
    return finalTime

# print(getTime(1.0,"days")) # returns "093100"
# print(getDate(1.0,"days")) # returns "20200103"

def getLiteralDateAndTime(DATE,TIME):
    year=DATE[:4]
    month=DATE[4:6]
    day=DATE[6:]
    hours=TIME[:2]
    minutes=TIME[2:4]
    seconds=TIME[4:]

    literalDate = "{:02d} {} {} at {}:{}:{}".format(
        int(day), getMonthName(int(month)), year, hours, minutes, seconds
    )

    return literalDate

def getMonthName(month):
    monthNames=[
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]
    return monthNames[month - 1]

# print(getLiteralDate("15891212","234500")) # returns 12 Dec 1589 at 23:45:00


