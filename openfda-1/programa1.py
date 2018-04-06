import http.client
import json


headers = {'User-Agent': 'http-client'}

conexion = http.client.HTTPSConnection("api.fda.gov")
conexion.request("GET", "/drug/label.json", None, headers)
resp_obtenida= conexion.getresponse()
print(resp_obtenida.status, resp_obtenida.reason)
info_obtenida= resp_obtenida.read().decode("utf-8")
conexion.close()

info_deseada = json.loads(info_obtenida)
datos_medic=info_deseada['results'][0]

print ('ID: ',datos_medic['id'])
print ('Proposito: ',datos_medic['purpose'][0])

print ('Fabricante: ',datos_medic['openfda']['manufacturer_name'][0])