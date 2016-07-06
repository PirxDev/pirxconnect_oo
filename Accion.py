import configuracion
import twitter
import codecs
import getopt
import sys
import io
import urllib.request
import urllib.error
import webbrowser
import os
import re
import Connectdb


class accion(object):

    def __init__(self):
        pass

    def save(self, xhtml, output):
        out = codecs.open(output, mode='a', encoding='ascii', errors='xmlcharrefreplace')
        out.write(xhtml)
        out.close()

    def imagen(self, urlpost, id):
        opener1 = urllib.request.build_opener()
        try:
            page1 = opener1.open(urlpost)
        except urllib.error.HTTPError as e:
            print(e.fp.read())
        try:
            pagina = page1.read()
        except urllib.error.HTTPError as e:
            print(e.fp.read())
        busqueda = re.compile('data-resolved-url-large="(.+?):large"')
        resultadobusq = busqueda.findall(pagina)
        if resultadobusq is not None:
            a = 0
            for i in resultadobusq:
                urlencontrada = i
                # print urlencontrada
                opener2 = urllib.request.build_opener()
                page2 = opener2.open(urlencontrada)
                imagen = page2.read()
                filename = id + str(a) + urlencontrada[-6:]
                fout = open(filename, "wb")
                fout.write(imagen)
                fout.close()
                a += 1

    def tweet(self, message):
        token = configuracion.Configuracion()
        consumer_key = token.configsectionmap("Datos")['consumer_key']
        consumer_secret = token.configsectionmap("Datos")['consumer_secret']
        access_key = token.configsectionmap("Datos")['access_token_key']
        access_secret = token.configsectionmap("Datos")['access_token_secret']

        api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token_key=access_key, access_token_secret=access_secret)
        api.PostUpdate(message)

    def busqueda(self, termino, cantidad):
        token = configuracion.Configuracion()
        consumer_key = token.configsectionmap("Datos")['consumer_key']
        consumer_secret = token.configsectionmap("Datos")['consumer_secret']
        access_key = token.configsectionmap("Datos")['access_token_key']
        access_secret = token.configsectionmap("Datos")['access_token_secret']

        api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token_key=access_key, access_token_secret=access_secret)
        resultado = api.GetSearch(termino, count=cantidad)
        print(api.VerifyCredentials())
        # json_size = len(resultado)
        # print json_size
        # print resultado[0]
        # print resultado[1]
        # print type(resultado)
        for s in resultado:
            # print(s)
            sdict = s.AsDict()
            # if s.geo is True:
            # if "geo_enabled" in sdict["user"]:
            #     geo =
            #     print geo

            if "urls" in sdict:
                keys = sdict["urls"].keys()
                i = 0
                for k in keys:
                    sdict["urls"]["url"+str(i)] = sdict["urls"][k]
                    i += 1
                for k in keys:
                    sdict["urls"].pop(k)

            if "retweeted_status" in sdict:
                if "urls" in sdict["retweeted_status"]:
                    keys = sdict["retweeted_status"]["urls"].keys()
                    i = 0
                    for k in keys:
                        sdict["retweeted_status"]["urls"]["url"+str(i)] = sdict["retweeted_status"]["urls"][k]
                        i += 1
                    for k in keys:
                        sdict["retweeted_status"]["urls"].pop(k)
            guardado = Connectdb.Connectdb()
            guardado.guardar(sdict)


            urlpost = "http://twitter.com/" + s.user.screen_name + "/statuses/" + str(s.id)
            # print urlpost
            self.imagen(urlpost, str(s.id))

            TEMPLATE = """
            <div class="twitter">
            <span class="twitter-user"><a href="http://twitter.com/%s">Twitter</a>: </span>
            <span class="twitter-text">%s</span>
            <span class="twitter-relative-created-at"><a href="http://twitter.com/%s/statuses/%s">Posted %s</a></span>
            </div>
            """
            xhtml = TEMPLATE % (s.user.screen_name, s.text, s.user.screen_name, s.id, s.created_at)
            output = "salidaresultado.html"
            self.save(xhtml, output)
