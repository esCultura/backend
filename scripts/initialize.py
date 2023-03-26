from datetime import date
from . import refresh


def run():
    avui = date.today()
    # Les dates s'estructuren de la següent manera
    data_avui = avui.strftime('%Y-%m-%d') + 'T00:00:00'
    refresh.getEsdevenimentsDadesObertes("data_inici>='" + data_avui + "'")
