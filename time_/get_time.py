from datetime import datetime, date


def calCulateDate(date__):
    date___ = str(date__).split("-")
    now__ = str(date.today()).split("-")
    if int(now__[0]) -1 == int(date___[0]):
        return "A year ago"
    elif int(now__[0]) -2== int(date___[0]):
        return "2 years ago"
    elif int(now__[0]) -3== int(date___[0]):
        return "3 years ago"
    else:
        if int(now__[1]) -1== int(date___[1]):
            return "A month ago"
        elif int(now__[1]) -2== int(date___[1]):
            return "2 months ago"
        elif int(now__[1]) -3== int(date___[1]):
            return "3 months ago"
        elif int(now__[1]) -4== int(date___[1]):
            return "4 months ago"
        elif int(now__[1]) -5== int(date___[1]):
            return "5 months ago"
        elif int(now__[1]) -6== int(date___[1] ):
            return "6 months ago"
        elif int(now__[1]) -7== int(date___[1] ):
            return "7 months ago"
        elif int(now__[1]) -8== int(date___[1] ):
            return "8 months ago"
        elif int(now__[1]) -9== int(date___[1] ):
            return "9 months ago"
        elif int(now__[1]) -10== int(date___[1] ):
            return "10 months ago"
        elif int(now__[1]) -11== int(date___[1] ):
            return "11 months ago"
        else:
            if int(now__[2])-1 == int(date___[2]):
                return "yesterday"
            else:
                day_obj = datetime.strptime(date__, "%Y-%m-%d")
                day = day_obj.strftime('%a')
                return str(day)


def getStringTime(time):
    date_time = str(time).split("T")
    date_ = date_time[0]
    time_ = date_time[1].split(':')
    if date_ == str(date.today()):
        theTime = "today"
    else:
        theTime = calCulateDate(date_)
    if time_[0][0] == "0" or time_[0][0] == "1" or time_[0][0] == "2":
        oras = "am"
        hour = time_[0][1:]
    else:
        oras = "pm"
        hour = time_[0]
    
    return f"{theTime} {hour}:{time_[1]}{oras}"