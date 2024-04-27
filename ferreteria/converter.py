import requests, json
from datetime import datetime
from urllib.request import urlopen

#Funciones
def fecha_de_hoy():
    fecha_actual = datetime.now()
    seteo_fecha = "{0}-{1:02d}-{2}".format(fecha_actual.year, fecha_actual.month, fecha_actual.day)
    return seteo_fecha

def usd_a_clp(usd):
    values = []
    f_hoy = str(fecha_de_hoy())
    url = 'https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=fr.aranedag@duocuc.cl&pass=A20846555-4&firstdate='+f_hoy+'&lastdate='+f_hoy+'&timeseries=F073.TCO.PRE.Z.D&function=GetSeries'
    response = urlopen(url)
    data = json.load(response)
    valor = data["Series"]["Obs"][0]["value"]
    clp = float(usd)*float(valor)
    values.append(valor)
    values.append(clp)
    return values

valores = usd_a_clp(5)
dolar = valores[0]
convertido = valores[1]
print(f"Valor dolar hoy: ${dolar}")
print(f"Convertido: ${round(convertido)}")