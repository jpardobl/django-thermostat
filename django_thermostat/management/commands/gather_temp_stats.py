from django.core.management.base import BaseCommand, CommandError
from django_thermostat.models import ThermometerData, Thermometer
#from django_thermostat import settings
import requests
from time import strftime, localtime
from django.core.urlresolvers import reverse
import simplejson
import logging
from django.conf import settings
import multiprocessing


logger = logging.getLogger("thermostat.stats")
logger.setLevel(settings.LOG_LEVEL)

class Command(BaseCommand):
    args = ''
    help = 'retrieve temperature stats'

    def __init__(self):
	p = multiprocessing.current_process()
        p.name = "temp_stats"

    def handle(self, *args, **options):
        try:
            logger.info("Starting at %s" % strftime("%d.%m.%Y %H:%M:%S", localtime()))

            if not settings.LIST_THERMOMETERS_API is None:
                ret = requests.get("http://localhost%stemperatures=True" % reverse("temperatures"))
                therms = ret.json()
            else:
                therms = simplejson.loads(read_temperatures())

            for therm in therms:
                try:
                    thermometro = Thermometer.objects.get(caption=therm)
                    value = therms[therm]["temp"]["celsius"]
                    logger.debug("Thermometer: %s; value: %s" % (therm, value))
                    ThermometerData(thermometer=thermometro, value=value).save()
                except Exception as ex:
                    logger.error("Error gathering %s data: %s" % (therm, ex))
                    continue
            logger.info("Ended at %s" % strftime("%d.%m.%Y %H:%M:%S", localtime()))
        except Exception as et:
            self.stderr.write("Error gathering temp stats: %s" % et)
            logger.error("Error gathering temp stats: %s" % et)
