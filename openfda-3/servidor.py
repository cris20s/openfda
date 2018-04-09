import http.server
import socketserver
import http.client
import json

# Puerto donde lanzar el servidor, utilizamos uno cualquiera superior a 1024
PORT = 2025


def obtener_list():
    lista = []
    headers = {'User-Agent': 'http-client'}

    conexion= http.client.HTTPSConnection("api.fda.gov")
    conexion.request("GET", "/drug/label.json?limit=11", None, headers)

    resp_obtenida = conexion.getresponse()
    print(resp_obtenida.status, resp_obtenida.reason)
    info_obtenida = resp_obtenida.read().decode("utf-8")
    conexion.close()

    info_deseada = json.loads(info_obtenida)
    for i in range(len(info_deseada['results'])):
        datos_medic = info_deseada['results'][i]
        if (datos_medic['openfda']):
            print('Fabricante: ', datos_medic['openfda']['generic_name'][0])
            lista.append(datos_medic['openfda']['generic_name'][0])

    return lista

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    # GET. Metodo para realizar la peticion. Se encuentra en self.path

    def do_GET(self):
        # 200 OK --> funciona correctamente
        self.send_response(200)

        # Cabeceras con el contenido
        # Empleamos distintas etiquetas de html para crear la pagina web
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        contenido="<html><body style='background-color: pink'> <p> <h1> LISTA DE MEDICAMENTOS </h1></p>"
        lista=obtener_list ()

        for e in lista:
            contenido += "<li>" + e + "</li>" "<br>"
        contenido+="</body></html>"

        self.wfile.write(bytes(contenido, "utf8"))
        return



#  Servidor

Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("Sirviendo en el puerto: ", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass

httpd.server_close()
print("")
print("¡Se ha parado el servidor! ¡Revíselo!")