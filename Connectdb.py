import pymongo
import gridfs


class Connectdb(object):
    def __init__(self):
        self.client = pymongo.MongoClient("192.168.100.224", 27017)

    def guardarimagen(self, archivo):
        imagendb = self.client.pirxconnect
        imagendb.imagenresultado.insert_one(archivo).inserted_id

    def guardar(self, mensaje):
        tweetdb = self.client.pirxconnect
        tweetdb.resultadobusqueda.insert_one(mensaje).inserted_id