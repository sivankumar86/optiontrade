import datetime

from business_calendar import Calendar


def getday(day,numberofdays):
    cal = Calendar()
    date = cal.addbusdays(day, numberofdays)
    return date.strftime("%Y-%m-%d")