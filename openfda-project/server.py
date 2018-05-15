import http.server
import http.client
import json
import socketserver

PORT = 8000


class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    URL_APIOPENFDA = "api.fda.gov"
    EVENT_APIOPENFDA = "/drug/label.json"
    FARMACO_APIOPENFDA = '&search=active_ingredient:'
    COMPANIA_APIOPENFDA = '&search=openfda.manufacturer_name:'

    def pagina_principal(self):
        html = """
            <html>
                <head> 
                    <meta http-equiv="content-type" content="text/html; charset=utf-8">
                    <title>OpenFDA App</title>
                </head>
                <body style='background-color: lavenderblush'>
                    <h1><em>¡BIENVENIDO A OPENFDA CLIENT!</em></h1>
                    <h2><sub> Por favor, seleccione una opción:</sub> </h2>
                    <ol>

                    <form method="get" action="listDrugs">
                        <input type = "submit" value="Lista de farmacos">
                        </input>
                    </form>
                    </ol>

                    <ol>
                    <form method="get" action="searchDrug">
                        <input type = "submit" value="Buscar farmacos">
                        <input type = "text" name="drug"></input>
                        </input>
                    </form>
                    </ol>

                    <ol>
                    <form method="get" action="listCompanies">
                        <input type = "submit" value="Lista de compañias">
                        </input> 
                    </form>
                    </ol>

                    <ol>
                    <form method="get" action="searchCompany">
                        <input type = "submit" value="Buscar compañias">
                        <input type = "text" name="company"></input>
                        </input>
                    </form>
                    </ol>

                    <ol>
                    <form method="get" action="listWarnings">
                        <input type = "submit" value="Lista de advertencias">
                        </input>
                    </form>
                    </ol>


                    <footer> Cristina Salazar Diego, Inegniería Biomédica </footer> 

                </body>
            </html>
                """

        return html

    def pag_web(self, lista):
        list_html = """
                                <html>
                                    <head>
                                        <title>OpenFDA Cool App</title>
                                    </head>
                                    <body>
                                        <ul>
                            """
        for item in lista:
            list_html += "<li>" + item + "</li>"

        list_html += """
                                        </ul>
                                    </body>
                                </html>
                            """
        return list_html

    def obt_resultados(self, limite=10):
        conexion = http.client.HTTPSConnection(self.URL_APIOPENFDA)
        conexion.request("GET", self.EVENT_APIOPENFDA + "?limit=+" + str(limite))
        print(self.EVENT_APIOPENFDA + "?limit=" + str(limite))
        resp_obtenida = conexion.getresponse()
        info_obtenida = resp_obtenida.read().decode("utf8")
        info_deseada = json.loads(info_obtenida)
        resultados = info_deseada['results']
        return resultados

    def do_GET(self):

        lista_de_recursos = self.path.split("?")
        if len(lista_de_recursos) > 1:
            parametros = lista_de_recursos[1]
        else:
            parametros = ""

        limite = 1
        if parametros:
            parse_limit = parametros.split("=")
            if parse_limit[0] == "limit":
                limite = int(parse_limit[1])
        else:
            print("Sin parametros")

        # Write content as utf-8 data
        if self.path == '/':
            self.send_response(200)
            # Send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = self.pagina_principal()
            self.wfile.write(bytes(html, "utf8"))
        elif 'listDrugs' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            lista_medicamentos = []
            resultados = self.obt_resultados(limite)
            for resultado in resultados:
                if ('generic_name' in resultado['openfda']):
                    lista_medicamentos.append(resultado['openfda']['generic_name'][0])
                else:
                    lista_medicamentos.append('DESCONOCIDO')
            resultado_html = self.pag_web(lista_medicamentos)

            self.wfile.write(bytes(resultado_html, "utf8"))

        elif 'listCompanies' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            compañias = []
            resultados = self.obt_resultados(limite)
            for resultado in resultados:
                if ('manufacturer_name' in resultado['openfda']):
                    compañias.append(resultado['openfda']['manufacturer_name'][0])
                else:
                    compañias.append('DESCONOCIDO')
            resultado_html = self.pag_web(compañias)
            self.wfile.write(bytes(resultado_html, "utf8"))

        elif 'listWarnings' in self.path:

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            advertencias_farmacos = []
            resultados = self.obt_resultados(limite)
            for resultado in resultados:
                if ('warnings' in resultado):
                    advertencias_farmacos.append(resultado['warnings'][0])
                else:
                    advertencias_farmacos.append('DESCONOCIDO')
            resultado_html = self.pag_web(advertencias_farmacos)

            self.wfile.write(bytes(resultado_html, "utf8"))

        elif 'searchDrug' in self.path:

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            limite = 10
            farmaco = self.path.split('=')[1]

            farmacos = []
            conexion = http.client.HTTPSConnection(self.URL_APIOPENFDA)
            conexion.request("GET", self.EVENT_APIOPENFDA + "?limit=" + str(limite) + self.FARMACO_APIOPENFDA + farmaco)
            resp_obtenida = conexion.getresponse()
            info1 = resp_obtenida.read()
            info = info1.decode("utf8")
            archivo_info = json.loads(info)
            buscador_de_farmacos = archivo_info['results']
            for resultado in buscador_de_farmacos:
                if ('generic_name' in resultado['openfda']):
                    farmacos.append(resultado['openfda']['generic_name'][0])
                else:
                    farmacos.append('DESCONOCIDO')

            resultado_html = self.pag_web(farmacos)
            self.wfile.write(bytes(resultado_html, "utf8"))


        elif 'searchCompany' in self.path:

            self.send_response(200)

            self.send_header('Content-type', 'text/html')
            self.end_headers()

            limite = 10
            compañia = self.path.split('=')[1]
            compañias = []
            conexion = http.client.HTTPSConnection(self.URL_APIOPENFDA)
            conexion.request("GET",
                             self.EVENT_APIOPENFDA + "?limit=" + str(limite) + self.COMPANIA_APIOPENFDA + compañia)
            resp_obtenida = conexion.getresponse()
            info1 = resp_obtenida.read()
            info = info1.decode("utf8")
            archivo_info = json.loads(info)
            buscador_de_compañias = archivo_info['results']

            for event in buscador_de_compañias:
                compañias.append(event['openfda']['manufacturer_name'][0])
            resultado_html = self.pag_web(compañias)
            self.wfile.write(bytes(resultado_html, "utf8"))
        elif 'redirect' in self.path:
            print("Redirigimos a la página principal.")
            self.send_error(302)
            self.send_header('Location', 'http://localhost:' + str(PORT))
            self.end_headers()
        elif 'secret' in self.path:
            self.send_error(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Mi servidor"')
            self.end_headers()
        else:
            self.send_error(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("I don't know '{}'.".format(self.path).encode())
        return


socketserver.TCPServer.allow_reuse_address = True

Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("PUERTO:", PORT)
httpd.serve_forever()