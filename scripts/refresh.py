import requests
from django.utils import timezone
from django.utils.dateparse import parse_datetime
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
            descripcio=d.get('descripcio', None),
            entrades=d.get('entrades', None),
            horari=d.get('horari', None),
            enllacos=d.get('enlla_os', None),
            imatges=d.get('imatges', None),
            latitud=d.get('latitud', None),
            longitud=d.get('longitud', None),
            espai=d.get('espai', None),
            email=d.get('email', None),
            telefon=d.get('telefon', None),
            url=d.get('url', None)
        )

        # Tractem les dates per separat, perquè cal passar l'string que rebem a DateTime i definir-li la timezone
        if d['data_inici']:
            esdev.dataIni = timezone.make_aware(parse_datetime(d['data_inici']), timezone.get_current_timezone())
        if d['data_fi']:
            esdev.dataFi = timezone.make_aware(parse_datetime(d['data_fi']), timezone.get_current_timezone())

        # Aconseguim província, comarca i municipi
        # A l'API, aquest camp s'estructura com: agenda:ubicacions/<provincia>/<comarca>/<municipi>
        if d['comarca_i_municipi']:
            comarca_i_municipi = d['comarca_i_municipi'].split("/")
            esdev.provincia = comarca_i_municipi[1]
            esdev.comarca = comarca_i_municipi[2]
            esdev.municipi = comarca_i_municipi[3]

        # Aconseguim les temàtiques de l'esdeveniment
        # ToDo

        # Guardem l'entrada rebuda a la nostra BD
        esdev.save()

