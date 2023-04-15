from django.urls import path
from rest_framework import routers
from .views import PerfilView, OrganitzadorView, AdmistradorView
from . import views

router = routers.DefaultRouter()

router.register('perfils', PerfilView, 'Perfils')
router.register('organitzadors', OrganitzadorView, 'Organitzadors')
router.register('admins', AdmistradorView, 'Administradors')

urlpatterns = router.urls