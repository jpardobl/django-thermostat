from django_thermostat.models import Context
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from settings import HEATER_INCREMENT, INTERNAL_TEMPERATURE_URI
from django.core.urlresolvers import reverse
from django_thermostat.mappings import get_mappings
from django_thermostat.temperature import read_temp
import simplejson


def home(request):
    context = Context.objects.get_or_create(pk=1)

    return render_to_response(
        "therm/home.html",
        {"context": context, },
    )


def temperature(request):
    response = HttpResponse(
        content=simplejson.dumps({"internal": "{0:.2f}".format(read_temp())}),
        content_type="application/json")
    response['Cache-Control'] = 'no-cache'
    return response


def dim_temp(request, temp):
    context = Context.objects.get()
    if temp == "confort":
        context.confort_temperature = float(context.confort_temperature) - float(HEATER_INCREMENT)
    if temp == "economic":
        context.economic_temperature = float(context.economic_temperature) - float(HEATER_INCREMENT)
    context.save()
    return redirect(reverse("read_heat_status"))


def bri_temp(request, temp):
    context = Context.objects.get()
    if temp == "confort":
        context.confort_temperature = float(context.confort_temperature) + float(HEATER_INCREMENT)
    if temp == "economic":
        context.economic_temperature = float(context.economic_temperature) + float(HEATER_INCREMENT)
    context.save()
    return redirect(reverse("read_heat_status"))


def toggle_heat_manual(request):
    context = Context.objects.get()
    context.manual = not context.manual
    context.save()
    return redirect(reverse("read_heat_status"))


def toggle_heat_status(request):
    context = Context.objects.get()
    context.heat_on = not context.heat_on
    context.save()

    return HttpResponse("")


def read_heat_status(request):
    response = render_to_response(
        "therm/context.json",
        {"data": Context.objects.get().to_json()},
        content_type="application/json",
    )
    response['Cache-Control'] = 'no-cache'
    return response


def context_js(request):
    return render_to_response(
        "context.js",
        {"temp_url": INTERNAL_TEMPERATURE_URI, },
        content_type="application/javascript")
