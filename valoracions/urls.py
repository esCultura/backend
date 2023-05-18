from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'', views.ValoracionsView, basename='valoracions')

urlpatterns = router.urls
