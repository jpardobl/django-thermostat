from django.db import models


class Context(models.Model):
    confort_temperature = models.IntegerField(default=22)
    economic_temperature = models.IntegerField(default=18)

    heat_on = models.BooleanField(default=False)

    

