from django.db import models
import simplejson


class Context(models.Model):
    confort_temperature = models.FloatField(default=22)
    economic_temperature = models.FloatField(default=18)

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
        })
