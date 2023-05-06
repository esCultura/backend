from rest_framework import routers

from django.urls import re_path

from .views import PerfilView, OrganitzadorView, AdmistradorView, SignUpPerfilsView, SignUpOrganitzadorsView, SignUpAdminsView, LoginPerfilsView, LoginOrganitzadorsView, LoginAdminView, GoogleSignIn, OrganitzadorsPendentsDeConfirmacioView

router = routers.DefaultRouter()

router.register('perfils', PerfilView, 'Perfils')
router.register('organitzadors', OrganitzadorView, 'Organitzadors')
router.register('admins', AdmistradorView, 'Administradors')
router.register('login/perfils', LoginPerfilsView, 'Log_in_Perfils')
router.register('login/organitzadors', LoginOrganitzadorsView, 'Log_in_Organitzadors')
router.register('login/admins', LoginAdminView, 'Log_in_Admins')
router.register('sign_up/perfils', SignUpPerfilsView, 'Sign_Up_Perfils')
router.register('sign_up/organitzadors', SignUpOrganitzadorsView, 'Sign_Up_Organitzadors')
router.register('sign_up/admins', SignUpAdminsView, 'Sign_Up_Admins')
router.register('organitzadorspendents', OrganitzadorsPendentsDeConfirmacioView, 'Organitzadors pendents de confirmació')

urlpatterns = router.urls + [re_path('sign_in/(?P<backend>[^/]+)/$', GoogleSignIn)]