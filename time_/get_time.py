from datetime import datetime, date, timedelta, timezone




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


def getStringTimeold(time):
    try:
        dateNow = datetime.now()
        timeNow = str(dateNow).split()[1]
        date_time = str(time).split("T")
        date_ = date_time[0]
        time_ = date_time[1].split(':')
    except:
        return time
    if date_ == str(date.today()):
        if time_[0] == str(timeNow).split(":")[0]:
            if int(str(timeNow).split(":")[1]) -int(time_[1]) < 10:
                return "Just Now {}m".format(str(int(time_[1])-int(str(timeNow).split(":")[1]))).replace("-", '')
            elif int(str(timeNow).split(":")[1]) -int(time_[1]) < 30:
                return "{}m ago.".format(str(int(time_[1])-int(str(timeNow).split(":")[1]))).replace("-", '')
            else:
                theTime = "today"
        else:
            theTime = "today"
    else:
        theTime = calCulateDate(date_)
    if time_[0][0] == "0" or time_[0] == "10" or time_[0] == "11" or time_[0] == "12":
        oras = "am"
        hour = time_[0][1:]
    else:
        oras = "pm"
        hour = str(int(time_[0]) -12)
    return f"{theTime} {hour}:{time_[1]}{oras}"



def getStringTime(date:str) -> str:
    try:
        date:datetime = datetime.fromisoformat(date.replace('Z', '+00:00'))
    except ValueError:
        return date
    now:datetime = datetime.now(timezone.utc)
    date:datetime = date.astimezone(now.tzinfo)
    diff:timedelta = now - date
    if diff.days >= 365:
        years = diff.days // 365
        if years > 1:
            return f'{years} years ago'
        else:
            return f'{years} year ago'
    elif diff.days >= 30:
        months = diff.days // 30
        if months is 1:
            return f'{months}m'
        else:
            return date.strftime('%b %d')
    elif diff.days >= 7:
        weeks = diff.days // 7
        if weeks is 1:
            return f'{weeks}w'
        else:
            return date.strftime('%b %d')
    elif diff.days > 0:
        day = diff.days
        return f'{day}d'
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f'{hours}h'
    elif diff.seconds > 60:
        minute = diff.seconds // 60
        return f'{minute}m'
    elif diff.seconds < 60 and diff.seconds > 15:
        return f'{diff.seconds}s'
    else:
        return 'just now'
