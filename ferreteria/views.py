from . import views
from datetime import datetime
import bcchapi, requests, json
from urllib.request import urlopen
from django.shortcuts import render
from flask import Flask, render_template
from django.http import HttpRequest, HttpResponse


# Funciones
def fecha_de_hoy():
    fecha_actual = datetime.now()
    seteo_fecha = "{0}-{1:02d}-{2}".format(
        fecha_actual.year, fecha_actual.month, fecha_actual.day
    )
    return seteo_fecha


def usd_a_clp(usd):
    values = []
    url = (
        "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=ai.arenas@duocuc.cl&pass=K20844763-7&function=GetSeries&timeseries=F073.TCO.PRE.Z.D&firstdate="
        + str(fecha_de_hoy())
        + "&lastdate="
        + str(fecha_de_hoy())
    )
    response = urlopen(url)
    data = json.load(response)
    valor = data["Series"]["Obs"][0]["value"]
    clp = float(usd) * float(valor)
    values.append(valor)
    values.append(clp)
    return values


def llamar_converter(request):
    if request.method == 'POST':
        usd = float(request.POST.get('usd', 0))
        resultado = usd_a_clp(usd)
        clp = resultado[1]
        return render(request, "converter.html", {'clp': clp})
    else:
        return HttpResponse("Método no permitido", status=405)


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

