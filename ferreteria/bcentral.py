import json, requests
from datetime import datetime
from urllib.request import urlopen

#Funciones
def fecha_de_hoy():
    fecha_actual = datetime.now()
    set_fecha = "{0}-{1:02d}-{2}".format(fecha_actual.year, fecha_actual.month, fecha_actual.day)
    return set_fecha

def usd_clp(precio):
    f_hoy = str(fecha_de_hoy())
    url = 'https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=fr.aranedag@duocuc.cl&pass=A20846555-4&firstdate='+f_hoy+'&lastdate='+f_hoy+'&timeseries=F073.TCO.PRE.Z.D&function=GetSeries'
    response = requests.get(url)
    data = json.loads(response.text.encode("utf-8"))
    usd = data["Series"]["Obs"][0]["value"]
    return usd

data = prueba()
print(data)