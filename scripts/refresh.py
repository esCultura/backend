import requests
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from esdeveniments.models import Esdeveniment, Tematica


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

        # Guardem l'entrada rebuda a la nostra BD. Ho hem de fer abans de definir les foreign keys,
        # perquè si no no troba l'objecte i no ens les permet crear.
        esdev.save()

        # Aconseguim les temàtiques de l'esdeveniment
        # A l'API, hi ha 2 camps amb temàtiques: tags_mbits i tags_categor_es
        # Els camps s'estructuren com: agenda:<tag>/<temàtica>,agenda:<tag>/<temàtica>,... (on <tag> és tags_mbits o tags_categor_es)
        tots_tags = d['tags_mbits'] + ',' + d['tags_categor_es']
        if tots_tags:
            tags = tots_tags.split(",")
            for tag in tags:
                # Processem cada tag, agafant <temàtica>, posant la primera lletra en majúscules i
                # separant les paraules (a la API separades per -)
                tag_name = ' '.join(tag.split("/")[1].capitalize().split("-"))
                # A continuació, busquem si ja tenim registrada la temàtica (per no sobreescriure-li els atributs
                # que pugui tenir ja definits) i l'enllacem amb l'esdeveniment
                tematica = Tematica.objects.get_or_create(nom=tag_name)[0]
                esdev.tematiques.add(tematica)
