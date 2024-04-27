from . import views
from datetime import datetime
import bcchapi, requests, json
from urllib.request import urlopen
from django.shortcuts import render

# Funcion
def fecha_de_hoy():
    fecha_actual = datetime.now()
    seteo_fecha = "{0}-{1:02d}-{2}".format(
        fecha_actual.year, fecha_actual.month, fecha_actual.day
    )
    return seteo_fecha

def usd_a_clp(usd):
    values = []
    #url = 'https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=ai.arenas@duocuc.cl&pass=K20844763-7&function=GetSeries&timeseries=F073.TCO.PRE.Z.D&firstdate='+str(fecha_de_hoy())+'&lastdate='+str(fecha_de_hoy())
    url = 'https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=ai.arenas@duocuc.cl&pass=K20844763-7&function=GetSeries&timeseries=F073.TCO.PRE.Z.D&firstdate=2024-04-26&lastdate=2024-04-26'
    response = urlopen(url)
    data = json.load(response)
    valor = data["Series"]["Obs"][0]["value"]
    clp = float(usd)*float(valor)
    values.append(valor)
    values.append(clp)
    return values

def euro_a_clp(euro):
    values = []
    #url = 'https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=ai.arenas@duocuc.cl&pass=K20844763-7&function=GetSeries&timeseries=F072.CLP.EUR.N.O.D&firstdate='+str(fecha_de_hoy())+'&lastdate='+str(fecha_de_hoy())
    url = 'https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=ai.arenas@duocuc.cl&pass=K20844763-7&function=GetSeries&timeseries=F072.CLP.EUR.N.O.D&firstdate=2024-04-26&lastdate=2024-04-26'
    response = urlopen(url)
    data = json.load(response)
    valor = data["Series"]["Obs"][0]["value"]
    clp = float(euro)*float(valor)
    values.append(valor)
    values.append(clp)
    return values

def libra_a_clp(libra):
    values = []
    #url = 'https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=ai.arenas@duocuc.cl&pass=K20844763-7&function=GetSeries&timeseries=F072.CLP.GBP.N.O.D&firstdate='+str(fecha_de_hoy())+'&lastdate='+str(fecha_de_hoy())
    url = 'https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=ai.arenas@duocuc.cl&pass=K20844763-7&function=GetSeries&timeseries=F072.CLP.GBP.N.O.D&firstdate=2024-04-26&lastdate=2024-04-26'
    response = urlopen(url)
    data = json.load(response)
    valor = data["Series"]["Obs"][0]["value"]
    clp = float(libra)*float(valor)
    values.append(valor)
    values.append(clp)
    return values

def convertir(request):
    if request.method == "GET":
        return render(request, "llama_conversor.html")
    elif request.method == "POST":
        value_str = request.POST.get("usd")
        tipo_cambio = request.POST.get("moneda")
        if not value_str:
            return render(request, "llama_conversor.html", {"mensaje": "El campo no puede estar vacío."})        
        try:
            #Verifica Numero
            value = float(value_str)
        except ValueError:
            return render(request, "llama_conversor.html", {"mensaje": "Por favor, ingrese un número válido."})
        if value < 0:
            #Verifica Positivo
            return render(request, "llama_conversor.html", {"mensaje": "El número no puede ser negativo."})  
        if tipo_cambio == "USD":
            values = usd_a_clp(value)
            actual = values[0]
            clp = values[1]
        elif tipo_cambio == "Euro":
            values = euro_a_clp(value)
            actual = values[0]
            clp = values[1]
        elif tipo_cambio == "Libra":
            values = libra_a_clp(value)
            actual = values[0]
            clp = values[1]
        return render(request, "converter.html", {"clp": clp,"actual": actual})
    else:
        return HttpResponse(status=405)

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

def carrito(request):
    return render(
        request,
        "carrito.html",
    )
