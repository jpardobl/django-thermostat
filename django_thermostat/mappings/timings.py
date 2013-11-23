from time import strftime, localtime, mktime, strptime


def current_day_of_week(mo=None):

    return strftime("%a", localtime())


def current_hour(mo=None):
    return "%f" % mktime(localtime())


def is_weekend(mo=None):
    today = current_day_of_week()
    if today == "Sat" or today == "Sun":
        return 1
    return 0


def gen_comparing_time(hour, minute, second):
    return mktime(strptime("%s %s %s %d:%d:%d" %(
        strftime("%d", localtime()),
        strftime("%m", localtime()),
        strftime("%Y", localtime()),
        hour,
        minute,
        second), "%d %m %Y %H:%M:%S"))

mappings = [current_day_of_week, current_hour, is_weekend, ]
