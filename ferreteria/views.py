from . import views
from datetime import datetime
import bcchapi, requests, json
from urllib.request import urlopen
from django.shortcuts import render

money_type = [
    ["USD", "Dólar"],
    ["SAR", "Rial saudita"],
    ["ARS", "Peso argentino"],
    ["AUD", "Dólar australiano"],
    ["BSP", "Dólar de las Bahamas"],
    ["BMD", "Dólar de bermudas"],
    ["BOL", "Boliviano"],
    ["BRL", "Real"],
    ["CAD", "Dólar canadiense"],
    ["QAR", "Riyal catarí"],
    ["CNY", "Yuan Renminbi"],
    ["COP", "Peso colombiano"],
    ["KRW", "Won"],
    ["CRC", "Colón"],
    ["CUP", "Peso cubano"],
    ["DEG", "DEG (FMI)"],
    ["DKK", "Corona Danesa"],
    ["EGP", "Libra egipcia"],
    ["AED", "Dírham"],
    ["EUR", "Euro"],
    ["PHP", "Peso filipino"],
    ["FJD", "Dolár de Fiji"],
    ["XPF", "Franco"],
    ["GTQ", "Quetzal guatemalteco"],
    ["HKD", "Dólar hongkonés"],
    ["HUF", "Forint"],
    ["INR", "Rupia India"],
    ["IDR", "Rupia de Indonesia"],
    ["IRR", "Rial iraní"],
    ["ISK", "Corona de islandia"],
    ["KYD", "Dólar de Islas Caimán"],
    ["ILS", "Shekel israelí"],
    ["JPY", "Yen"],
    ["KZT", "Tenge"],
    ["MYR", "Ringgit"],
    ["MAD", "Dírham"],
    ["MXN", "Peso mexicano"],
    ["NOK", "Corona noruega"],
    ["NZD", "Dólar neozelandés"],
    ["PKR", "Rupia Paquistaní"],
    ["PAB", "Balboa"],
    ["PYG", "Guaraní"],
    ["PEN", "Nuevo sol peruano"],
    ["PLN", "Zloty"],
    ["GBP", "Libra esterlina"],
    ["CZK", "Corona Checa"],
    ["DOP", "Peso de República Dominicana"],
    ["RON", "Leu rumano"],
    ["RUR", "Rublo ruso"],
    ["SGD", "Dólar de Singapur"],
    ["ZAR", "Rand"],
    ["SEK", "Corona sueca"],
    ["CHF", "Franco suizo"],
    ["THB", "Baht tailandés"],
    ["TWD", "Dólar taiwanés"],
    ["TRY", "Nueva lira turca"],
    ["UAH", "Hryvnia"],
    ["UYU", "Peso uruguayo"],
    ["VEB", "Bolívar"],
    ["VND", "Dong"],
]


# Funcion
def fecha_de_hoy():
    fecha_actual = datetime.now()
    seteo_fecha = "{0}-{1:02d}-{2}".format(
        fecha_actual.year, fecha_actual.month, fecha_actual.day
    )
    return seteo_fecha


def usd_a_clp(usd):
    values = []
    # url = 'https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=ai.arenas@duocuc.cl&pass=K20844763-7&function=GetSeries&timeseries=F073.TCO.PRE.Z.D&firstdate='+str(fecha_de_hoy())+'&lastdate='+str(fecha_de_hoy())
    url = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=ai.arenas@duocuc.cl&pass=K20844763-7&function=GetSeries&timeseries=F073.TCO.PRE.Z.D&firstdate=2024-04-26&lastdate=2024-04-26"
    response = urlopen(url)
    data = json.load(response)
    valor = data["Series"]["Obs"][0]["value"]
    clp = float(usd) * float(valor)
    values.append(valor)
    values.append(clp)
    return values


def valor_a_clp(v,m):
    values = []
    # url = 'https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=ai.arenas@duocuc.cl&pass=K20844763-7&function=GetSeries&timeseries=F072.CLP."+str()+"".N.O.D&firstdate='+str(fecha_de_hoy())+'&lastdate='+str(fecha_de_hoy())
    url = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=ai.arenas@duocuc.cl&pass=K20844763-7&function=GetSeries&timeseries=F072.CLP."+str(m)+".N.O.D&firstdate=2024-04-26&lastdate=2024-04-26"
    response = urlopen(url)
    data = json.load(response)
    valor = data["Series"]["Obs"][0]["value"]
    clp = float(v) * float(valor)
    values.append(valor)
    values.append(clp)
    return values


def convertir(request):
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
            return render(request, "converter.html", {"clp": clp, "actual": actual})
        else:
            for i in range(0, len(money_type)):
                if money_type[i][0] == tipo_cambio:
                    values = valor_a_clp(value,tipo_cambio)
                    actual = values[0]
                    clp = values[1]
            return render(request, "converter.html", {"clp": clp, "actual": actual})
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
