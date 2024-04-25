import bcchapi, requests, json
from datetime import datetime
from urllib.request import urlopen
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/llamar_converter')
def llamar_converter():
    try:
        response = requests.get()
        if response.status_code == 200:
            print("poto")
            resultado = usd_a_clp(2)
            return resultado[1]
        else:
            print("Error HTTP ", response.status_code)
            return 0.0
    except Exception as e:
        print("Error al procesar la solicitud:", e)
        return 0.0

if __name__ == '__main__':
    app.run(debug=True)

#Funciones
def fecha_de_hoy():
    fecha_actual = datetime.now()
    seteo_fecha = "{0}-{1:02d}-{2}".format(fecha_actual.year, fecha_actual.month, fecha_actual.day)
    return seteo_fecha

def usd_a_clp(usd):
    values = []
    url = 'https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=ai.arenas@duocuc.cl&pass=K20844763-7&function=GetSeries&timeseries=F073.TCO.PRE.Z.D&firstdate='+str(fecha_de_hoy())+'&lastdate='+str(fecha_de_hoy())
    response = urlopen(url)
    data = json.load(response)
    valor = data["Series"]["Obs"][0]["value"]
    clp = float(usd)*float(valor)
    values.append(valor)
    values.append(clp)
    return values

