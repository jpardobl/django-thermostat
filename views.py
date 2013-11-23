from django_thermometer.models import Context
from django.shortcuts import render_to_response


def home(request):
    context = Context.objects.get_or_create()

    return render_to_response(
        "home.html",
        {"context": context, },
    )
