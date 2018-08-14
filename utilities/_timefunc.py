#-*-coding:utf-8-*-
import time
import datetime
from dateutil.relativedelta import relativedelta
import dateutil.parser


start = time.time()

def RunTime():
    d = relativedelta(seconds = time.time() - start)
    run_time = "{0.hours:02}:{0.minutes:02}:{0.seconds:02}".format(d.normalized())
    return run_time

def TimeCurrent():
    now = datetime.datetime.now()
    return now

def UnixTimeCurrent():
    unixime = time.time()
    return unixime

def TimeParse(str_time):
    d = dateutil.parser.parse(str_time)
    return d


if __name__=='__main__':
    print(RunTime())
    time.sleep(61)
    print(RunTime())