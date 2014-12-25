from django.core.management.base import BaseCommand, CommandError
from django_thermostat.rules import evaluate_non_themp
from time import localtime, strftime, sleep
import logging
from django.conf import settings
import multiprocessing

logger = logging.getLogger("thermostat.rules")
logger.setLevel(settings.LOG_LEVEL)


class Command(BaseCommand):
    args = ''
    help = 'Evaluate rules realted to heater status. The result will start or stop the heater'

    def handle(self, *args, **options):
        try:
            p = multiprocessing.current_process()
            p.name = "non_therm"
            logger.info("Started")

            evaluate_non_themp()
            logger.info("Ended")

        except Exception as ex2:
            logger.error("Error ocurred: %s" % ex2)
            
