from . import views
from datetime import datetime
import requests, json
from urllib.request import urlopen
from django.shortcuts import render
from django.http import JsonResponse
from .converter import usd_a_clp


# Funciones
def fecha_de_hoy():
    fecha_actual = datetime.now()
    seteo_fecha = "{0}-{1:02d}-{2}".format(
        fecha_actual.year, fecha_actual.month, fecha_actual.day
    )
    return seteo_fecha

def convertir_usd_a_clp(request):
    if request.method == 'POST' and 'usd' in request.POST:
        usd = float(request.POST['usd'])
        values = usd_a_clp(usd)
        response_data = {'usd': usd, 'clp': values[1]}  # Devuelve los valores de USD y CLP
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Se esperaba un valor de USD en la solicitud.'}, status=400)


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

