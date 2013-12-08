import requests
from django_thermostat import settings
from hautomation_restclient.cmds import pl_switch
from django_thermostat.models import Context
from django.core.urlresolvers import reverse
from time import strftime, localtime
import os


def current_internal_temperature(mo=None):
    try:
        ret = requests.get(os.path.join(settings.INTERNAL_TEMPERATURE_URI))
        return float(ret.json()["internal"])
    except Exception, ex:
        print "Ex eption %s" % ex
        return None


def confort_temperature(mo=None):
    ctxt = Context.objects.get()
    if ctxt.flame:
        return float(ctxt.confort_temperature) + settings.HEATER_MARGIN
    return ctxt.confort_temperature


def economic_temperature(mo=None):
    ctxt = Context.objects.get()
    if ctxt.flame:
        return float(ctxt.economic_temperature) + settings.HEATER_MARGIN
    return ctxt.economic_temperature


def tuned_temperature(mo=None):
    ctxt = Context.objects.get()
    if ctxt.flame:
        return float(ctxt.tuned_temperature) + settings.HEATER_MARGIN
    return ctxt.tuned_temperature


def tune_to_confort(mo=None):
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Tunning to confort"

    ctxt = Context.objects.get()
    ctxt.tuned_temperature = ctxt.confort_temperature
    ctxt.save()


def tune_to_economic(mo=None):
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Tuning to economic"
    ctxt = Context.objects.get()
    ctxt.tuned_temperature = ctxt.economic_temperature
    ctxt.save()


def heater_manual(mo=None):
    return 1 if Context.objects.get().manual else 0


def heater_on(mo=None):
    return 1 if Context.objects.get().heat_on else 0


def flame_on():
    return 1 if Context.objects.get().flame else 0


def start_flame():
    print "Starting flame"

    pl_switch(
        settings.HEATER_PROTOCOL,
        settings.HEATER_DID,
        "on",
        settings.HEATER_API,
        settings.HEATER_USERNAME,
        settings.HEATER_PASSWORD)

    ctxt = Context.objects.get()
    ctxt.flame = True
    ctxt.save()

    print "%s flame started" % strftime("%d.%m.%Y %H:%M:%S", localtime())


def stop_flame():
    print "stoping flame"

    pl_switch(
        settings.HEATER_PROTOCOL,
        settings.HEATER_DID,
        "off",
        settings.HEATER_API,
        settings.HEATER_USERNAME,
        settings.HEATER_PASSWORD)

    ctxt = Context.objects.get()
    ctxt.flame = False
    ctxt.save()
    print "%s flame stopped" % strftime("%d.%m.%Y %H:%M:%S", localtime())


mappings = [
    current_internal_temperature,
    confort_temperature,
    economic_temperature,
    start_flame,
    stop_flame,
    heater_manual,
    heater_on,
    flame_on,
    tune_to_confort,
    tune_to_economic,
    tuned_temperature,
    ]
