from rest_framework import routers

from django.urls import re_path

from .views import PerfilView, OrganitzadorView, AdmistradorView, SignUpPerfilsView, LoginPerfilsView, GoogleSignIn

router = routers.DefaultRouter()

router.register('perfils', PerfilView, 'Perfils')
router.register('organitzadors', OrganitzadorView, 'Organitzadors')
router.register('admins', AdmistradorView, 'Administradors')
router.register('login/perfils', LoginPerfilsView, 'Log_in_Perfils')
router.register('sign_up/perfils', SignUpPerfilsView, 'Sign_Up_Perfils')

urlpatterns = router.urls + [re_path('sign_in/(?P<backend>[^/]+)/$', GoogleSignIn)]