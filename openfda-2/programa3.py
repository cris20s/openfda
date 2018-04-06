import http.client
import json

headers = {'User-Agent': 'http-client'}
saltar_num=0
while True:

    conexion = http.client.HTTPSConnection("api.fda.gov")
#conn.request("GET", "/drug/label.json?limit=20&search=active_ingredient:%22acetylsalicylic%22", None, headers)
    conexion.request("GET", '/drug/label.json?search=substance_name:"ASPIRIN"&limit=100&skip='+str(saltar_num), None, headers)

    resp_obtenida = conexion.getresponse()
    print(resp_obtenida.status, resp_obtenida.reason)
    info_obtenida = resp_obtenida.read().decode("utf-8")
    conexion.close()



    info_deseada = json.loads(info_obtenida)
    for i in range (len (info_deseada['results'])):
        datos_medic=info_deseada['results'][i]

        print ('ID: ',datos_medic['id'])
        if (datos_medic['openfda']):
            print('Fabricante: ', datos_medic['openfda']['manufacturer_name'][0])
    if (len(info_deseada['results']))<100:
        break
    saltar_num=saltar_num+100