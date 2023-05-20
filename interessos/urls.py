from rest_framework import routers
from .views import InteresEnEsdevenimentView, InteresEnTematicaView, InteresEnValoracioView

router = routers.DefaultRouter()

router.register('esdeveniments', InteresEnEsdevenimentView, 'InteressosEnEsdeveniments')
router.register('tematiques', InteresEnTematicaView, 'InteressosEnTematiques')
router.register('valoracions', InteresEnValoracioView, 'InteressosEnValoracions')

urlpatterns = router.urls
