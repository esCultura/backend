from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'', views.EsdevenimentsView, basename='esdeveniments')

urlpatterns = router.urls
