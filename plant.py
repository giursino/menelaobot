import xml.etree.ElementTree as etree

class SystemFunction(object):

    def __init__(self, name):

        # Nome della funzione
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def setAction(self, type, address):
        self.actionType = type
        self.actionAddress = address



# Importa l'impianto da XML
def ImportPlant(xmlfile):
    tree = etree.parse(xmlfile)
    gChAutomazione=tree.findall('configurator/application[@name="Automazione"]/index')
    gChClima=tree.findall('configurator/application[@name="Clima"]/index')

    for gCh in gChAutomazione:
        name = gCh.attrib['label']
        sf = SystemFunction(name)
        print sf.name

        dptxs = gCh.findall('datapointtypes/datapointtype')
        for dptx in dptxs:
            print dptx.attrib['name']


    pass

def main():
    ImportPlant('Casa GG.xml')
    pass

if __name__=="__main__":
    main()