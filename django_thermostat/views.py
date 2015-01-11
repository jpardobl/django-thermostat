from django_thermostat.models import Context, Thermometer, ThermometerData
from django.shortcuts import render_to_response, redirect, render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.conf import settings
from django.core.urlresolvers import reverse
from django_thermostat.mappings import get_mappings
from django_thermometer.temperature import read_temperatures
import simplejson, logging, requests
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta

logger = logging.getLogger("thermostat.web")
logger.setLevel(settings.LOG_LEVEL)


def dumy_stats(request):
    return render_to_response(
        "therm/dummy_stats.json",{})

def temp_data_show(request):
    return render_to_response(
        "therm/stats.html",
        {}
    )

def temp_data(request, grouping=None):

    if grouping in (None, "day"):
        data = ThermometerData.objects.get_last_n_days(3)
    if grouping == "week":
        data = ThermometerData.objects.get_last_n_weeks(2)
    if grouping == "month":
        data = ThermometerData.objects.get_last_n_months()
    if grouping == "year":
        data = ThermometerData.objects.get_last_year()

    response = HttpResponse(
        content=simplejson.dumps(data),
        content_type="application/json")

    response['Cache-Control'] = 'no-cache'

    return response


def set_external_reference(request, tid):
    try:
        therm = Thermometer.objects.get(is_external_reference=True)
        if therm.tid == tid or therm.caption == tid:
            return HttpResponse("")
        therm.is_external_reference = None
        therm.save()
    except ObjectDoesNotExist:
        #no previously selected thermostat
        pass
    except Exception as err:
        logger.error("set_external_reference: %s" % err)

    try:
        therm = Thermometer.objects.get(Q(tid=tid) | Q(caption=tid))
        therm.is_external_reference = True
        therm.save()
        return HttpResponse("OK")
    except ObjectDoesNotExist:
        return HttpResponseBadRequest("Thermostats %s not found" % tid)
    except Exception as ex:
        logger.error("set_external_reference: %s" % ex)
        return HttpResponseServerError(ex)


def set_internal_reference(request, tid):

    try:
        therm = Thermometer.objects.get(is_internal_reference=True)
        if therm.tid == tid or therm.caption == tid:
            return HttpResponse("")
        therm.is_internal_reference = None
        therm.save()
    except ObjectDoesNotExist:
	    #no previously selected thermostat
	    pass
    except Exception as err:
        logger.error("set_internal_reference: %s" % err)

    try:
        therm = Thermometer.objects.get(Q(tid=tid) | Q(caption=tid))
        therm.is_internal_reference = True
        therm.save()
        return HttpResponse("OK")
    except ObjectDoesNotExist:
        return HttpResponseBadRequest("Thermostats %s not found" % tid)
    except Exception as ex:
        logger.error("set_internal_reference: %s" % ex)
        return HttpResponseServerError(ex)


def home(request):
    context = Context.objects.get_or_create(pk=1)

    return render_to_response(
        "therm/home.html",
        {"context": context,
         },
    )


def temperatures(request):
    if not settings.LIST_THERMOMETERS_API is None:
        ret = requests.get("%stemperatures=True" % settings.LIST_THERMOMETERS_API)
        therms = ret.json()
    else:
        therms = read_temperatures()
    known_therms = {}
    for x in Thermometer.objects.all():
        known_therms[x.tid] = [x.caption, x.is_internal_reference, x.is_external_reference]
    out = {}
    for tid, data in therms.items():
        try:
            out[known_therms[tid][0]] = {
                    "temp": data, 
                    "is_internal": known_therms[tid][1],
                    "is_external": known_therms[tid][2]}
        except KeyError:
            out[tid] = [data, False]

    response = HttpResponse(
        content=simplejson.dumps(out),
        content_type="application/json")
    response['Cache-Control'] = 'no-cache'
    return response


def dim_temp(request, temp):
    context = Context.objects.get()
    if temp == "confort":
        context.confort_temperature = float(context.confort_temperature) - float(settings.HEATER_INCREMENT)
    if temp == "economic":
        context.economic_temperature = float(context.economic_temperature) - float(settings.HEATER_INCREMENT)
    context.save()
    return redirect(reverse("read_heat_status"))


def bri_temp(request, temp):
    context = Context.objects.get()
    if temp == "confort":
        context.confort_temperature = float(context.confort_temperature) + float(settings.HEATER_INCREMENT)
    if temp == "economic":
        context.economic_temperature = float(context.economic_temperature) + float(settings.HEATER_INCREMENT)
    context.save()
    return redirect(reverse("read_heat_status"))


def put_heat_manual(request):
    context = Context.objects.get()
    context.manual = True
    context.save()
    return redirect(reverse("read_heat_status"))


def put_heat_program(request):
    context = Context.objects.get()
    context.manual = False
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
        {"temperatures_uri": settings.LIST_THERMOMETERS_API, },
        content_type="application/javascript")


def gradient(request):

    try:
        import redis, dateutil.parser

        r = redis.Redis(settings.GRADIENT_REDIS_HOST)
        data = []
        maps = {}
        for t in Thermometer.objects.all():
            maps[t.tid] = t.caption

        for t in r.keys("temp_*"):
            pref, termo, fecha = t.split("-")
            termo = "28-%s" % termo
            data.append({"termo": maps[termo], "i_t": fecha, "ct": r.get(t)})

        mx = int(r.get("gradient_sec"))
        logger.debug("gradient_sec: %s" % mx)

        for i in range(0, mx + 1):
            d = r.lrange("g_%s:e" % i, 0, 6)
            if len(d) == 0:
                continue
            di = r.lrange("g_%s:i" % i, 0, 4)

            data.append({
                "i_t": dateutil.parser.parse(di[0]).strftime("%d.%m%Y %H:%M:%S"),
                "i_cit": di[1],
                "i_cet": di[2],
                "i_tt": di[3],
                "e_t": dateutil.parser.parse(d[0]).strftime("%d.%m%Y %H:%M:%S"),
                "e_cit": d[1],
                "e_cet": d[2],
                "e_tt": d[3],
                "e_ds": d[4],
                "e_d": d[5],
                "e_eg": d[6],
            })

        if "format" in request.GET and request.GET["format"] == "html":
            response = render_to_response(
                "therm/gradient.html",
                {"data": data},
                content_type="text/html"
            )
        if "format" in request.GET and request.GET["format"] == "json":
            response = render_to_response(
                "therm/context.json",
                {"data": simplejson.dumps(data)},
                content_type="application/json"
            )
        if "format" in request.GET and request.GET["format"] == "csv":
            response = render_to_response(
                "therm/gradient.csv",
                {"data": simplejson.dumps(data)},
                content_type="text/csv"
            )
        response['Cache-Control'] = 'no-cache'
        return response
    except Exception as ex:
        logger.error(ex)
        return HttpResponseServerError(ex)

