import http.client
import json

headers = {'User-Agent': 'http-client'}

conexion= http.client.HTTPSConnection("api.fda.gov")
conexion.request("GET", "/drug/label.json?limit=10", None, headers)
resp_obtenida = conexion.getresponse()
print(resp_obtenida.status, resp_obtenida.reason)
info_obtenida= resp_obtenida.read().decode("utf-8")
conexion.close()




info_deseada = json.loads(info_obtenida)
for i in range (len (info_deseada['results'])):
    datos_medic=info_deseada['results'][i]

    print ('ID: ',datos_medic['id'])