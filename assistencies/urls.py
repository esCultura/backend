from rest_framework import routers
from .views import *

router = routers.DefaultRouter()

router.register('', AssistenciaAEsdevenimentView, 'AssistenciaAEsdeveniment')

urlpatterns = router.urls
