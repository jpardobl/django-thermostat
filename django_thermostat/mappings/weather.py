import requests
from django_thermostat import settings
from hautomation_restclient.cmds import pl_switch
from django_thermostat.models import Context
from django.core.urlresolvers import reverse


def current_internal_temperature(mo=None):
    try:
        ret = requests.get("http://raspberry/therm/temperature")
        return float(ret.json()["internal"])
    except Exception, ex:
        print "Ex eption %s" % ex
        return None


def confort_temperature(mo=None):
    ctxt = Context.objects.get()
    if ctxt.flame:
        return ctxt.confort_temperature + settings.HEATER_MARGIN
    return ctxt.confort_temperature


def economic_temperature(mo=None):
    ctxt = Context.objects.get()
    if ctxt.flame:
        return ctxt.economic_temperature + settings.HEATER_MARGIN
    return ctxt.economic_temperature


def heater_manual(mo=None):
    return 1 if Context.objects.get().manual else 0


def heater_on(mo=None):
    return 1 if Context.objects.get().heat_on else 0


def flame_on():
    return 1 if Context.objects.get().flame else 0


def start_flame():

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
    print "Flame started"

def stop_flame():
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
    print "Flame stopped"


mappings = [
    current_internal_temperature,
    confort_temperature,
    economic_temperature,
    start_flame,
    stop_flame,
    heater_manual,
    heater_on,
    flame_on, ]
