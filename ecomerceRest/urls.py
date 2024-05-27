"""
URL configuration for ecomerceRest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include #recuerda, include para enlazar las rutas de las diferentes apps
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from apps.users.api.view.views import Login, Logout, UserToken

schema_view = get_schema_view(
   openapi.Info(
      title="Documentación API",
      default_version='v1',
      description="Documentación publica para proyecto ecomerce",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="cristiamontenegro2001@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Login.as_view(),name='login'),
    path('logout/', Logout.as_view(),name='logout'),
    path('refresh/', UserToken.as_view(),name='refresh'),
    path('usuario/', include('apps.users.api.routers')),
    path('products/', include('apps.products.api.routers')),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'), #swagger json
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'), #swagger, para ver todas las rutas del proyecto
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'), #redo
]
