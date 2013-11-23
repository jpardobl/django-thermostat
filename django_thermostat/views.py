from django_thermostat.models import Context
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from settings import HEATER_INCREMENT
from django.core.urlresolvers import reverse


def home(request):
    context = Context.objects.get_or_create(pk=1)

    return render_to_response(
        "home.html",
        {"context": context, },
    )


def dim_temp(request, temp):
    context = Context.objects.get()
    if temp == "confort":
        context.confort_temperature = context.confort_temperature - float(HEATER_INCREMENT)
    if temp == "economic":
        context.economic_temperature = context.economic_temperature - float(HEATER_INCREMENT)
    context.save()
    return redirect(reverse("read_heat_status"))


def bri_temp(request, temp):
    context = Context.objects.get()
    if temp == "confort":
        context.confort_temperature = context.confort_temperature + float(HEATER_INCREMENT)
    if temp == "economic":
        context.economic_temperature = context.economic_temperature + float(HEATER_INCREMENT)
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
        "context.json",
        {"data": Context.objects.get().to_json()},
        content_type="application/json",
    )
    response['Cache-Control'] = 'no-cache'
    return response


def context_js(request):
    return render_to_response("context.js", {}, conte)
