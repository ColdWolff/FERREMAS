from . import views
from datetime import datetime
import bcchapi, requests, json
from urllib.request import urlopen
from django.shortcuts import render

money_type = [
    ["USD", "Dólar", "Dolares"],
    ["KRW", "Won", "Wones"],
    ["EUR", "Euro", "Euros"],
    ["JPY", "Yen", "Yenes"],
    ["GBP", "Libra", "Libras"]
]

# Funcion
def fecha_de_hoy():
    fecha_actual = datetime.now() 
    # Controlador Finde
    if fecha_actual.weekday() == 5:
        fecha_actual = -timedelta(days=1)
    elif fecha_actual.weekday() == 6:
        fecha_actual = -timedelta(days=2)
    
    seteo_fecha = "{0}-{1:02d}-{2}".format(
        fecha_actual.year, fecha_actual.month, fecha_actual.day
    )
    return seteo_fecha

def usd_a_clp(usd):
    values = []
    url = 'https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=ai.arenas@duocuc.cl&pass=K20844763-7&function=GetSeries&timeseries=F073.TCO.PRE.Z.D&firstdate='+str(fecha_de_hoy())+'&lastdate='+str(fecha_de_hoy())
    #url = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=ai.arenas@duocuc.cl&pass=K20844763-7&function=GetSeries&timeseries=F073.TCO.PRE.Z.D&firstdate=2024-04-26&lastdate=2024-04-26"
    response = urlopen(url)
    data = json.load(response)
    valor = data["Series"]["Obs"][0]["value"]
    clp = round(float(usd) * float(valor),2)
    values.append(valor)
    values.append(clp)
    return values


def valor_a_clp(v,m):
    values = []
    url = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=ai.arenas@duocuc.cl&pass=K20844763-7&function=GetSeries&timeseries=F072.CLP."+str(m)+".N.O.D&firstdate="+str(fecha_de_hoy())+"&lastdate="+str(fecha_de_hoy())
    #url = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=ai.arenas@duocuc.cl&pass=K20844763-7&function=GetSeries&timeseries=F072.CLP."+str(m)+".N.O.D&firstdate=2024-04-26&lastdate=2024-04-26"
    response = urlopen(url)
    data = json.load(response)
    valor = data["Series"]["Obs"][0]["value"]
    clp = round(float(v) * float(valor),2)
    values.append(valor)
    values.append(clp)
    return values

def clp_a_usd(clp):
    values = []
    url = 'https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=ai.arenas@duocuc.cl&pass=K20844763-7&function=GetSeries&timeseries=F073.TCO.PRE.Z.D&firstdate='+str(fecha_de_hoy())+'&lastdate='+str(fecha_de_hoy())
    #url = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=ai.arenas@duocuc.cl&pass=K20844763-7&function=GetSeries&timeseries=F073.TCO.PRE.Z.D&firstdate=2024-04-26&lastdate=2024-04-26"
    response = urlopen(url)
    data = json.load(response)
    valor = data["Series"]["Obs"][0]["value"]
    usd = round(float(clp)/float(valor),2)
    values.append(valor)
    values.append(usd)
    return values


def clp_a_valor(v,m):
    values = []
    url = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=ai.arenas@duocuc.cl&pass=K20844763-7&function=GetSeries&timeseries=F072.CLP."+str(m)+".N.O.D&firstdate="+str(fecha_de_hoy())+"&lastdate="+str(fecha_de_hoy())
    #url = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=ai.arenas@duocuc.cl&pass=K20844763-7&function=GetSeries&timeseries=F072.CLP."+str(m)+".N.O.D&firstdate=2024-04-26&lastdate=2024-04-26"
    response = urlopen(url)
    data = json.load(response)
    valor = data["Series"]["Obs"][0]["value"]
    divisa = round(float(v)/float(valor),2)
    values.append(divisa)
    values.append(clp)
    return values

def convertir_divisa(request):
    if request.method == "GET":
        return render(request, "llama_conversor.html", {"money_type": money_type})
    elif request.method == "POST":
        value_str = request.POST.get("valor")
        tipo_cambio = request.POST.get("moneda")
        if not value_str:
            return render(
                request,
                "llama_conversor.html",
                {"mensaje": "El campo no puede estar vacío."},
                {"money_type": money_type},
            )
        try:
            # Verifica Numero
            value = float(value_str)
        except ValueError:
            return render(
                request,
                "llama_conversor.html",
                {"mensaje": "Por favor, ingrese un número válido."},
                {"money_type": money_type},
            )
        if value < 0:
            # Verifica Positivo
            return render(
                request,
                "llama_conversor.html",
                {"mensaje": "El número no puede ser negativo."},
                {"money_type": money_type},
            )
        if tipo_cambio == "USD":
            values = usd_a_clp(value)
            actual = values[0]
            clp = values[1]
            return render(request, "converter.html", {"convertido": clp, "actual": actual, "moneda" : "Pesos"})
        else:
            for i in range(0, len(money_type)):
                if money_type[i][0] == tipo_cambio:
                    values = valor_a_clp(value,tipo_cambio)
                    actual = values[0]
                    clp = values[1]
            return render(request, "converter.html", {"convertido": clp, "actual": actual, "moneda" : "Pesos"})
    else:
        return HttpResponse(status=405)

def reconvertir_divisa(request):
    if request.method == "GET":
        return render(request, "llama_conversor.html", {"money_type": money_type})
    elif request.method == "POST":
        value_str = request.POST.get("clp")
        tipo_cambio = request.POST.get("moneda_reversa")
        if not value_str:
            return render(
                request,
                "llama_conversor.html",
                {"mensaje": "El campo no puede estar vacío."},
                {"money_type": money_type},
            )
        try:
            # Verifica Numero
            value = float(value_str)
        except ValueError:
            return render(
                request,
                "llama_conversor.html",
                {"mensaje": "Por favor, ingrese un número válido."},
                {"money_type": money_type},
            )
        if value < 0:
            # Verifica Positivo
            return render(
                request,
                "llama_conversor.html",
                {"mensaje": "El número no puede ser negativo."},
                {"money_type": money_type},
            )
        if tipo_cambio == "USD":
            values = clp_a_usd(value)
            actual = values[0]
            divisa = values[1]
            for i in range (len(money_type)):
                if tipo_cambio == money_type[i][0]:
                    moneda = money_type[i][2]
            return render(request, "converter.html", {"convertido": divisa, "actual": actual, "moneda":moneda})
        else:
            for i in range(0, len(money_type)):
                if money_type[i][0] == tipo_cambio:
                    values = valor_a_clp(value,tipo_cambio)
                    actual = values[0]
                    divisa = values[1]
            for i in range (len(money_type)):
                if tipo_cambio == money_type[i][0]:
                    moneda = money_type[i][2]
            return render(request, "converter.html", {"convertido": divisa, "actual": actual, "moneda":moneda})
    else:
        return HttpResponse(status=405) 
    
def index(request):
    return render(
        request,
        "index.html",
    )

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
