from django.core.management.base import BaseCommand, CommandError
from django_thermostat.rules import evaluate
from time import localtime, strftime


class Command(BaseCommand):
    args = ''
    help = 'Evaluate rules realted to heater status. The result will start or stop the heater'

    def handle(self, *args, **options):
        try:
            self.stdout.write("Starting at %s" % strftime("%d.%m.%Y %h:%m:%s", localtime()))
            evaluate()
            self.stdout.write("Ended at %s" % strftime("%d.%m.%Y %h:%m:%s", localtime()))
        except Exception, ex:
