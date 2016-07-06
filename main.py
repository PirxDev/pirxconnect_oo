# -*- coding: utf-8 -*-

import Obtenertoken
import configuracion
import Accion
import argparse

configurado = configuracion.Configuracion()
if configurado.configsectionmap("Estado")['configurado'] != "1":
    Obtenertoken()

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--tweet", help="Publica Tweet, main.py -t mensaje.")
parser.add_argument("-b", "--buscar", help="Busca cadena, main.py -b palabraclave. Si va a buscar un hashtag, por favor use comillas.")
parser.add_argument("-c", "--cantidad", type=int, help="Cantidad de resultados (Por omision:30), main.py -c cantidad.")
parser.add_argument("-a", "--amigos", help="Lista Amigos.",
                    action="store_true")
args = parser.parse_args()

if args.tweet:
    tweetear = Accion.accion()
    tweetear.tweet(args.tweet)

if args.buscar:
    buscando = Accion.accion()
    if args.cantidad:
        buscando.busqueda(args.buscar, args.cantidad)
    else:
        buscando.busqueda(args.buscar, 30)

if args.amigos:
    listadeamigos = Accion.accion()
    listadeamigos.amigos

# else:
#    print "Para ver ayuda: python main.py -h"
