from . import views
from datetime import datetime
import bcchapi, requests, json
from urllib.request import urlopen
from django.shortcuts import render


# Funciones
def fecha_de_hoy():
    fecha_actual = datetime.now()
    seteo_fecha = "{0}-{1:02d}-{2}".format(
        fecha_actual.year, fecha_actual.month, fecha_actual.day
    )
    return seteo_fecha

def index(request):
    return render(
        request,
        "index.html",
    )

def hnf(request):
    return render(
        request,
        "hnf.html",
    )

def c(request):
    return render(
        request,
        "carrito.html",
    )

def converter(request):
    return render(
        request,
        "converter.html",
    )

