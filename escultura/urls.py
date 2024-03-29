"""escultura URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from scripts.views import refresh_script

schema_view = get_schema_view(
   openapi.Info(
      title="esCultura API",
      default_version='v1',
      description="Posant els ESdeveniments CULTURAls a l'abast de tothom",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('refresh/', refresh_script, name='Refresh'),
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('usuaris/', include('usuaris.urls'), name='Usuaris'),
    path('esdeveniments/', include('esdeveniments.urls'), name='Esdeveniments'),
    path('interessos/', include('interessos.urls'), name='Interessos'),
    path('assistencies/', include('assistencies.urls'), name='Assistencies'),
    path('xats/', include('xats.urls'), name='Assistencies'),
    path('seguiments/', include('seguiments.urls'), name='Seguiments'),
    path('valoracions/', include('valoracions.urls'), name='Valoracions')
]
