from time import strftime, localtime, mktime, strptime


def current_day_of_week(mo=None):

    return strftime("%a", localtime())


def current_time(mo=None):
    lt = localtime()
    st = "%s %s %s %s:%s:%s" %(
        strftime("%d", lt),
        strftime("%m", lt),
        strftime("%Y", lt),
        strftime("%H", lt),
        strftime("%M", lt),
        strftime("%S", lt))
    print "tiempo intermedio: %s " % st
    t = strptime(st, "%d %m %Y %H:%M:%S")
    
    return mktime(t)


def is_weekend(mo=None):
    today = current_day_of_week()
    if today == "Sat" or today == "Sun":
        return 1
    return 0


def gen_comparing_time(hour, minute, second):
    lt = localtime()
    st = "%s %s %s %d:%d:%d" %(
        strftime("%d", lt),
        strftime("%m", lt),
        strftime("%Y", lt),
        hour,
        minute,
        second)
    print "tiempo intermedio: %s " % st
    t = strptime(st, "%d %m %Y %H:%M:%S")
    print "Con %s:%s:%s, generamos: %s" % (hour, minute, second, t)
    return mktime(t)

mappings = [current_day_of_week, current_time, is_weekend, ]
