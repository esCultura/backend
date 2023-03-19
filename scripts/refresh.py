import requests
from esdeveniments.models import Esdeveniment


def run():
    getEsdevenimentsDadesObertes()


def getEsdevenimentsDadesObertes():
    url = "https://analisi.transparenciacatalunya.cat/resource/rhpv-yr4f.json?" \
          "$where=data_inici between '2023-03-19T12:00:00' and '2023-03-20T12:00:00'"
    response = requests.get(url)
    data = response.json()
    for d in data:
        esdev = Esdeveniment(
            codi=d['codi'],
            nom=d['denominaci'],
        )
        esdev.save()

