from rest_framework import routers
from .views import *

router = routers.DefaultRouter()

router.register('esdeveniments', InteresEnEsdevenimentView, 'InteressosEnEsdeveniments')
router.register('tematiques', InteresEnTematicaView, 'InteressosEnTematiques')

urlpatterns = router.urls