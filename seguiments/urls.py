from rest_framework import routers
from .views import SeguimentView

router = routers.DefaultRouter()

router.register('', SeguimentView, 'Seguiments')

urlpatterns = router.urls
