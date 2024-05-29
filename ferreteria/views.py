from datetime import datetime, timedelta
import json
import random
from .models import Producto, Categoria, Stock, Proveedor
from urllib.request import urlopen
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.conf import settings
from transbank.error.transbank_error import TransbankError
from transbank.webpay.webpay_plus.transaction import Transaction

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
    
#C   
def productoAdd(request):
    if request.method != "POST":
        categorias = Categoria.objects.all()
        marcas = Proveedor.objects.all()
        context = {'categorias': categorias, 'marcas': marcas}
        return render(request, 'add_prod.html', context)
    else:
        marca = request.POST["marca"]
        codigo_prod = request.POST["codigo_prod"]
        nombre_prod = request.POST["nombre_prod"]
        desc_prod = request.POST["desc_prod"]
        precio_prod = request.POST["precio_prod"]
        id_categoria = request.POST["id_categoria"]

        objCategoria = Categoria.objects.get(id_categoria=id_categoria)
        objMarca = Proveedor.objects.get(id_proveedor=marca)
        objMarca = objMarca.nom_prov
        
        try:
            precio_prod = float(precio_prod)
        except ValueError:
            categorias = Categoria.objects.all()
            marcas = Proveedor.objects.all()
            productos = Producto.objects.all()
            context = {
                'categorias': categorias,
                'marcas': marcas,
                'productos': productos,
                'mensaje': "Error: El precio ingresado no es válido. Por favor, ingrese un número decimal."
            }
            return render(request, 'add_prod.html', context)

        obj = Producto.objects.create(marca=objMarca,
                                      codigo_prod=codigo_prod,
                                      nombre_prod=nombre_prod,
                                      desc_prod=desc_prod,
                                      precio_prod=precio_prod,
                                      id_categoria=objCategoria)
        obj.save()
        categorias = Categoria.objects.all()
        marcas = Proveedor.objects.all()
        productos = Producto.objects.all()
        context = {
            'categorias': categorias,
            'marcas': marcas,
            'productos': productos,
            'mensaje': "Producto Registrado..."
        }
        return render(request, 'add_prod.html', context)

#R
def productoRead(request,pk):
    if pk != "":
        productos = Producto.objects.get(id_producto=pk)
        categorias = Categoria.objects.all()
        marcas = Proveedor.objects.all()

        context= {'productos': productos, 'categorias': categorias, 'marcas': marcas}
        if productos:
            return render(request, 'update_prod.html', context)
        else:
            context= {'mensaje': "Error, producto no existe..."}
            return render(request, 'list_prod.html', context)

#U
def productoUpdate(request):
    if request.method == "POST":
        id_producto = request.POST["id_producto"]
        marca = request.POST["marca"]
        codigo_prod = request.POST["codigo_prod"]
        nombre_prod = request.POST["nombre_prod"]
        desc_prod = request.POST["desc_prod"]
        precio_prod = request.POST["precio_prod"]
        id_categoria = request.POST["id_categoria"]

        objCategoria = Categoria.objects.get(id_categoria=id_categoria)
        objMarca = Proveedor.objects.get(id_proveedor=marca)
        objMarca = objMarca.nom_prov

        producto = Producto.objects.get(id_producto=id_producto)
        producto.marca = objMarca
        producto.codigo_prod = codigo_prod
        producto.nombre_prod = nombre_prod
        producto.desc_prod = desc_prod
        
        try:
            precio_prod = float(precio_prod)
        except ValueError:
            productos = Producto.objects.all()
            categorias = Categoria.objects.all()
            marcas = Proveedor.objects.all()
            stocks = Stock.objects.all()
            context = {
                'mensaje': "Error: El precio ingresado no es válido. Por favor, ingrese un número decimal.",
                'productos': productos,
                'categorias': categorias,
                'marcas': marcas,
                'producto': producto,
                'stocks':stocks
            }
            return render(request, 'list_prod.html', context)
        
        producto.precio_prod = precio_prod
        producto.id_categoria = objCategoria
        producto.save()
        
        productos = Producto.objects.all()
        categorias = Categoria.objects.all()
        marcas = Proveedor.objects.all()
        stocks = Stock.objects.all()
        context = {
            'mensaje': "Ok, datos actualizados...",
            'productos': productos,
            'categorias': categorias,
            'marcas': marcas,
            'producto': producto,
            'stocks':stocks
        }
        return render(request, 'list_prod.html', context)
    else:
        productos = Producto.objects.all()
        context = {'productos': productos,'stocks':stocks}
        return render(request, 'list_prod.html', context)  

#D   
def productoDel(request, pk):
    context={}
    try:
        producto = Producto.objects.get(id_producto = pk)
        producto.delete()
        productos = Producto.objects.all()
        context = {'productos':productos, 'mensaje':"Producto eliminado"}
        return render(request, 'list_prod.html', context)
    except:
        productos= Producto.objects.all()
        context = {'productos':productos, 'mensaje':"Error"}
        return render(request, 'list_prod.html', context)

#L
def productoList(request):
    productos = Producto.objects.all()
    stocks = Stock.objects.all()
    context={'productos':productos, 'stocks':stocks}
    return render(request,"list_prod.html",context)

#C
def stockAdd(request):
    if request.method != "POST":
        productos = Producto.objects.all()
        context={'productos':productos}
        return render(request, 'add_stock.html', context)
    else:
        cantidad = request.POST["cantidad"]
        id_producto = request.POST["id_producto"]

        # Verificar si ya existe un registro de stock para este producto
        if Stock.objects.filter(id_producto=id_producto).exists():
            productos = Producto.objects.all()
            stocks = Stock.objects.all()
            context= {'stocks':stocks, 'productos':productos,'mensaje':"Ya existe un registro de stock para este producto.",}
        else:
            objProducto = Producto.objects.get(id_producto=id_producto)
            obj = Stock.objects.create(
                cantidad=cantidad,
                id_producto=objProducto
            )
            obj.save()
            productos = Producto.objects.all()
            stocks = Stock.objects.all()
            context= {'stocks':stocks, 'productos':productos,'mensaje':"Stock Registrado...",}
    return render(request, 'add_stock.html', context)

#R
def stockRead(request,pk):
    if pk != "":
        productos = Producto.objects.all()
        stocks = Stock.objects.get(id_stock=pk)

        context= {'productos': productos, 'stocks': stocks}
        if stocks:
            return render(request, 'update_stock.html', context)
        else:
            context= {'mensaje': "Error, stock no existe..."}
            return render(request, 'list_stock.html', context)

#U
def stockUpdate(request):
    if request.method == "POST":
        id_stock = request.POST["id_stock"]
        cantidad = int(request.POST["cantidad"])

        stock = Stock.objects.get(id_stock = id_stock)
        stock.cantidad += cantidad 
        stock.save()

        productos = Producto.objects.all()
        stocks = Stock.objects.all()
        context = {'mensaje': "Ok, datos actualizados...", 'productos': productos, 'stocks': stocks, 'stock': stock}
        return render(request, 'update_stock.html', context)
    else:
        stocks = Stock.objects.all()
        context={'stocks': stocks}
        return render(request, 'list_stock.html',context)

#D   
def stockDel(request, pk):
    context={}
    try:
        stock = Stock.objects.get(id_stock = pk)
        stock.delete()
        stocks = Stock.objects.all()
        context = {'stocks':stocks, 'mensaje':"Stock eliminado"}
        return render(request, 'list_stock.html', context)
    except:
        stocks = Stock.objects.all()
        context = {'stocks':stocks, 'mensaje':"Error"}
        return render(request, 'list_stock.html', context)
            
#L
def stockList(request):
    stocks = Stock.objects.all()
    context={'stocks': stocks}
    return render(request,"list_stock.html",context)

#TRANSBANK
def webpay_plus_create(request: HttpRequest) -> HttpResponse:
    buy_order = str(random.randrange(1000000, 99999999))
    session_id = str(random.randrange(1000000, 99999999))
    amount = random.randrange(10000, 1000000)
    return_url = request.build_absolute_uri('/webpay/plus/commit/')

    create_request = {
        "buy_order": buy_order,
        "session_id": session_id,
        "amount": amount,
        "return_url": return_url
    }
    
    response = Transaction().create(buy_order, session_id, amount, return_url)
    return render(request, 'webpay/plus/create.html', {'request': create_request, 'response': response})

def webpay_plus_commit(request: HttpRequest) -> HttpResponse:
    token = request.GET.get("token_ws")
    response = Transaction().commit(token=token)
    return render(request, 'webpay/plus/commit.html', {'token': token, 'response': response})

def webpay_plus_commit_error(request: HttpRequest) -> HttpResponse:
    token = request.POST.get("token_ws")
    response = {"error": "Transacción con errores"}
    return render(request, 'webpay/plus/commit.html', {'token': token, 'response': response})

def webpay_plus_refund(request: HttpRequest) -> HttpResponse:
    token = request.POST.get("token_ws")
    amount = request.POST.get("amount")
    try:
        response = Transaction().refund(token, amount)
        return render(request, "webpay/plus/refund.html", {'token': token, 'amount': amount, 'response': response})
    except TransbankError as e:
        return HttpResponse(e.message)

def webpay_plus_refund_form(request: HttpRequest) -> HttpResponse:
    return render(request, "webpay/plus/refund-form.html")

def status_form(request: HttpRequest) -> HttpResponse:
    return render(request, 'webpay/plus/status-form.html')

def status(request: HttpRequest) -> HttpResponse:
    token_ws = request.POST.get('token_ws')
    response = Transaction().status(token_ws)
    return render(request, 'webpay/plus/status.html', {'response': response, 'token': token_ws, 'req': request.POST})


#PAGINAS
def index(request):
    productos = Producto.objects.all()
    context={'productos': productos}
    return render(request,"index.html",context)

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

