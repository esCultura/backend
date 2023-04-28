from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'', views.XatsView, basename='xats')
router.register(r'(?P<xat_id>\d+)/missatges', views.MissatgesView, basename='missatges')

urlpatterns = router.urls
