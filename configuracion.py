import configparser


class Configuracion(object):

    def __init__(self):
        self.configurar = configparser.ConfigParser()
        self.configurar.read("../config")

    def configsectionmap(self, section):
        dict1 = {}
        options = self.configurar.options(section)
        for option in options:
            try:
                dict1[option] = self.configurar.get(section, option)
                if dict1[option] == -1:
                    DebugPrint("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

    def grabar(self, section, parametro, valor):
        cfgfile = open("config", 'w')
        self.configurar.set(section, parametro, valor)
        self.configurar.write(cfgfile)
        cfgfile.close()
