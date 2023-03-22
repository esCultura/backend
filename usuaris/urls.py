from rest_framework import routers
from .views import PerfilView

router = routers.DefaultRouter()

router.register('', PerfilView, 'Perfils')

urlpatterns = router.urls
