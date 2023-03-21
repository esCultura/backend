from rest_framework import routers
from .views import *

router = routers.DefaultRouter()

router.register('', PerfilView, 'Perfils')

urlpatterns = router.urls
