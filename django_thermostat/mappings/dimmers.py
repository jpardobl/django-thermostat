
from django_thermostat import settings
from hautomation_restclient.cmds import pl_switch


def salon_on(mo=None):
    print "subir salon"
    print pl_switch(
        settings.HEATER_PROTOCOL,
        settings.SALON_DID,
        "on",
        settings.HEATER_API,
        settings.HEATER_USERNAME,
        settings.HEATER_PASSWORD)
    print "ya hemos subido salon"

def salon_off(mo=None):
    print "bajar ***********************************"
    pl_switch(
        settings.HEATER_PROTOCOL,
        settings.SALON_DID,
        "off",
        settings.HEATER_API,
        settings.HEATER_USERNAME,
        settings.HEATER_PASSWORD)


def pasillo_off(mo=None):
    pl_switch(
        settings.HEATER_PROTOCOL,
        settings.PASILLO_DID,
        "off",
        settings.HEATER_API,
        settings.HEATER_USERNAME,
        settings.HEATER_PASSWORD)


def pasillo_on(mo=None):
    pl_switch(
        settings.HEATER_PROTOCOL,
        settings.PASILLO_DID,
        "on",
        settings.HEATER_API,
        settings.HEATER_USERNAME,
        settings.HEATER_PASSWORD)


def cuarto_oeste_off(mo=None):
    pl_switch(
        settings.HEATER_PROTOCOL,
        settings.CUARTO_OESTE_DID,
        "off",
        settings.HEATER_API,
        settings.HEATER_USERNAME,
        settings.HEATER_PASSWORD)


def cuarto_oeste_on(mo=None):
    pl_switch(
        settings.HEATER_PROTOCOL,
        settings.CUARTO_OESTE_DID,
        "on",
        settings.HEATER_API,
        settings.HEATER_USERNAME,
        settings.HEATER_PASSWORD)


def cuarto_este_off(mo=None):
    pl_switch(
        settings.HEATER_PROTOCOL,
        settings.CUARTO_OESTE_DID,
        "off",
        settings.HEATER_API,
        settings.HEATER_USERNAME,
        settings.HEATER_PASSWORD)


def cuarto_este_on(mo=None):
    pl_switch(
        settings.HEATER_PROTOCOL,
        settings.CUARTO_ESTE_DID,
        "on",
        settings.HEATER_API,
        settings.HEATER_USERNAME,
        settings.HEATER_PASSWORD)


mappings = [
    salon_off,
    salon_on,
    cuarto_este_on,
    cuarto_este_off,
    cuarto_oeste_off,
    cuarto_oeste_on,
    pasillo_on,
    pasillo_off,
    ]
