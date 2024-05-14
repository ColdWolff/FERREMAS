from datetime import datetime, timedelta
import json
from .models import Producto, Categoria, Stock
from urllib.request import urlopen
from django.shortcuts import render

money_type = [
    ["USD", "Dólar", "Dolares"],
    ["KRW", "Won", "Wones"],
    ["EUR", "Euro", "Euros"],
    ["JPY", "Yen", "Yenes"],
    ["GBP", "Libra", "Libras"],
]


def fecha_de_hoy():
    fecha_actual = datetime.now()
    if fecha_actual.weekday() == 5:
        fecha_actual -= timedelta(days=1)
    elif fecha_actual.weekday() == 6:
        fecha_actual -= timedelta(days=2)

    return fecha_actual.strftime("%Y-%m-%d")


def obtener_valor(url):
    response = urlopen(url)
    data = json.load(response)
    return data["Series"]["Obs"][0]["value"]


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
                {"mensaje": "El campo no puede estar vacío.", "money_type": money_type},
            )

        try:
            value = float(value_str)
        except ValueError:
            return render(
                request,
                "llama_conversor.html",
                {
                    "mensaje": "Por favor, ingrese un número válido.",
                    "money_type": money_type,
                },
            )

        if value < 0:
            return render(
                request,
                "llama_conversor.html",
                {
                    "mensaje": "El número no puede ser negativo.",
                    "money_type": money_type,
                },
            )

        url_actual = f"https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=ai.arenas@duocuc.cl&pass=K20844763-7&function=GetSeries&timeseries=F073.TCO.PRE.Z.D&firstdate={fecha_de_hoy()}&lastdate={fecha_de_hoy()}"
        valor_actual = obtener_valor(url_actual)

        if tipo_cambio == "USD":
            url_moneda = f"https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=ai.arenas@duocuc.cl&pass=K20844763-7&function=GetSeries&timeseries=F073.TCO.PRE.Z.D&firstdate={fecha_de_hoy()}&lastdate={fecha_de_hoy()}"
        else:
            url_moneda = f"https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=ai.arenas@duocuc.cl&pass=K20844763-7&function=GetSeries&timeseries=F072.CLP.{tipo_cambio}.N.O.D&firstdate={fecha_de_hoy()}&lastdate={fecha_de_hoy()}"

        valor_moneda = obtener_valor(url_moneda)

        if tipo_cambio == "USD":
            clp = round(float(value) * float(valor_actual), 2)
        else:
            clp = round(float(value) * float(valor_moneda), 2)

        return render(
            request,
            "converter.html",
            {
                "convertido": clp,
                "actual": valor_actual,
                "moneda": "Pesos",
                "valor_moneda": valor_moneda,
            },
        )
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
                {"mensaje": "El campo no puede estar vacío.", "money_type": money_type},
            )

        try:
            value = float(value_str)
        except ValueError:
            return render(
                request,
                "llama_conversor.html",
                {
                    "mensaje": "Por favor, ingrese un número válido.",
                    "money_type": money_type,
                },
            )

        if value < 0:
            return render(
                request,
                "llama_conversor.html",
                {
                    "mensaje": "El número no puede ser negativo.",
                    "money_type": money_type,
                },
            )

        url = f"https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=ai.arenas@duocuc.cl&pass=K20844763-7&function=GetSeries&timeseries=F073.TCO.PRE.Z.D&firstdate={fecha_de_hoy()}&lastdate={fecha_de_hoy()}"
        valor_actual = obtener_valor(url)

        if tipo_cambio == "USD":
            divisa = round(float(value) / float(valor_actual), 2)
        else:
            url = f"https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=ai.arenas@duocuc.cl&pass=K20844763-7&function=GetSeries&timeseries=F072.CLP.{tipo_cambio}.N.O.D&firstdate={fecha_de_hoy()}&lastdate={fecha_de_hoy()}"
            divisa = round(float(value) / float(valor_actual), 2)
        valor_moneda = obtener_valor(url)
        for i in range(len(money_type)):
            if money_type[i][0] == tipo_cambio:
                tipo = money_type[i][2]
        return render(
            request,
            "converter.html",
            {
                "convertido": divisa,
                "actual": valor_actual,
                "moneda": tipo,
                "valor_moneda": valor_moneda,
            },
        )
    else:
        return HttpResponse(status=405)
    
def productoAdd(request):
    if request.method != "POST":
        categorias = Categoria.objects.all()
        context={'categorias':categorias}
        return render(request, 'add_prod.html', context)
    else:
        marca = request.POST["marca"]
        codigo_prod = request.POST["codigo_prod"]
        nombre_prod = request.POST["nombre_prod"]
        desc_prod = request.POST["desc_prod"]
        precio_prod = request.POST["precio_prod"]
        #foto_prod = request.POST["foto_prod"]
        id_categoria = request.POST["id_categoria"]

        objCategoria = Categoria.objects.get(id_categoria = id_categoria)
        obj= Producto.objects.create(   id_categoria= objCategoria,
                                        marca = marca,
                                        codigo_prod = codigo_prod,
                                        nombre_prod = nombre_prod,
                                        desc_prod = desc_prod,
                                        precio_prod = precio_prod)
        obj.save()
        categorias= Categoria.objects.all()
        context= {'categorias':categorias, 'mensaje':"Producto Registrado..."}
        return render(request, 'add_prod.html', context)
    
def productoDel(request, pk):
    context={}
    try:
        producto = Producto.objects.get(id_prod = pk)
        producto.delete()
        productos = Producto.objects.all()
        context = {'productos':productos, 'mensaje':"Producto eliminado"}
        return render(request, 'productos_list.html', context)
    except:
        productos= Producto.objects.all()
        context = {'productos':productos, 'mensaje':"Error"}
        return render(request, 'productos_list.html', context)


def index(request):
    return render(
        request,
        "index.html",
    )

def login(request):
    return render(
        request,
        "login.html",
    )

def signup(request):
    return render(
        request,
        "signup.html",
    )

def carrito(request):
    return render(
        request,
        "carrito.html",
    )

def add_cat(request):
    return render(
        request,
        "add_cat.html",
    )

