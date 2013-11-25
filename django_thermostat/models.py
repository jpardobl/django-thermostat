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
            "time": "%s" % strftime("%I:%M:%S", localtime()),
        })
