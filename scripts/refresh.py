import requests
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from datetime import date, timedelta
from esdeveniments.models import Esdeveniment, Tematica


def run():
    getEsdevenimentsDadesObertes()


def getDates(d, esdev):
    # Tractem les dates per separat, perquè cal passar l'string que rebem a DateTime i definir-li la timezone
    data_ini = d.get('data_inici', None)
    if data_ini:
        esdev.dataIni = timezone.make_aware(parse_datetime(data_ini), timezone.get_current_timezone())
    data_fi = d.get('data_fi', None)
    if data_fi:
        esdev.dataFi = timezone.make_aware(parse_datetime(data_fi), timezone.get_current_timezone())


def getProvinciaComarcaMunicipi(d, esdev):
    # Aconseguim província, comarca i municipi
    # A l'API, aquest camp s'estructura com: agenda:ubicacions/<provincia>/<comarca>/<municipi>
    # Peeero pot ser que no tingui tots els camps!
    com_i_mun = d.get('comarca_i_municipi', None)
    if com_i_mun:
        comarca_i_municipi = com_i_mun.split("/")
        if len(comarca_i_municipi) >= 4:
            esdev.municipi = comarca_i_municipi[3]
            if len(comarca_i_municipi) >= 3:
                esdev.comarca = comarca_i_municipi[2]
                if len(comarca_i_municipi) >= 2:
                    esdev.provincia = comarca_i_municipi[1]


def getTematiques(d, esdev):
    # Guardem l'entrada rebuda a la nostra BD. Ho hem de fer abans de definir les foreign keys,
    # perquè si no no troba l'objecte i no ens les permet crear.
    esdev.save()

    # Aconseguim les temàtiques de l'esdeveniment
    # A l'API, hi ha 2 camps amb temàtiques: tags_mbits i tags_categor_es
    # Els camps s'estructuren com: agenda:<tag>/<temàtica>,agenda:<tag>/<temàtica>,... (on <tag> és tags_mbits o tags_categor_es)
    tags_ambits = d.get('tags_mbits', '')
    tags_categories = d.get('tags_categor_es', '')
    tots_tags = tags_ambits + ',' + tags_categories
    if tots_tags != ',':
        tags = tots_tags.split(",")
        for tag in tags:
            if tag != '':
                # Processem cada tag, agafant <temàtica>, posant la primera lletra en majúscules i
                # separant les paraules (a la API separades per -)
                tag_name = ' '.join(tag.split("/")[1].capitalize().split("-"))
                # A continuació, busquem si ja tenim registrada la temàtica (per no sobreescriure-li els atributs
                # que pugui tenir ja definits) i l'enllacem amb l'esdeveniment
                tematica = Tematica.objects.get_or_create(nom=tag_name)[0]
                esdev.tematiques.add(tematica)


def getEsdevenimentsDadesObertes(where=None):
    if not where:
        ahir = date.today() - timedelta(days=1)
        # Els codis dels esdeveniments s'estructuren de la següent manera
        codi_ahir = ahir.strftime('%Y%m%d') + '000'
        where = 'codi>=' + codi_ahir
    url = "https://analisi.transparenciacatalunya.cat/resource/rhpv-yr4f.json?" \
          "$where=" + where
    response = requests.get(url)
    data = response.json()

    for d in data:
        try:
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
            getDates(d, esdev)
            getProvinciaComarcaMunicipi(d, esdev)
            getTematiques()
        except:
            try:
                print("No s'ha pogut carregar l'esdeveniment " + d['codi'])
            except:
                print("No s'ha pogut carregar un esdeveniment")
