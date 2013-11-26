from django.db import models
import simplejson
from time import localtime, strftime


class Context(models.Model):
    confort_temperature = models.DecimalField(default=22, decimal_places=2, max_digits=4)
    economic_temperature = models.DecimalField(default=18, decimal_places=2, max_digits=4)
    tuned_temperature = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=4)

    heat_on = models.BooleanField(default=False)
    manual = models.BooleanField(default=True)
    flame = models.BooleanField(default=False)


    def to_json(self, ):

        return simplejson.dumps({
            "status": "ON" if self.heat_on else "OFF",
            "confort": self.confort_temperature,
            "economic": self.economic_temperature,
            "manual": self.manual,
            "flame": self.flame,
            "tuned": self.tuned_temperature,
            "time": "%s" % strftime("%H:%M:%S", localtime()),
        })


class Day(models.Model):
    name = models.CharField(max_length=10)
    value = models.CharField(max_length=3)

    def __unicode__(self, ):
        return u"%s" % self.name

    def to_pypelib(self, ):
        return u"(current_day_of_week = %s)" % self.value


class TimeRange(models.Model):
    start = models.TimeField()
    end = models.TimeField()


    def to_pypelib(self, ):
        pass
        #return u"(%s > current_time && current_time < %s)" % (gen_comparing_time(self.start, self.end,


TEMP_CHOICES = (
    ("confort_temperature", "Confort"),
    ("economic_temperature", "Economic"),
)


class Rule(models.Model):

    days = models.ManyToManyField(Day)
    ranges = models.ManyToManyField(TimeRange)
    action = models.CharField(max_length=15, choices=TEMP_CHOICES)
    active = models.BooleanField(default=True)

    def to_pypelib(self, ):
        out = "if ("
        for day in self.days:
            out = "%s || %s" % (out, day.to_pypelib())
        out = "%s)" % out
        if self.ranges.all().count():
            out = "%s && ("
            for trang in ranges:
                out = trang.to_pypelib()
            out = "%s ) " % out
