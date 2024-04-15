from django.urls import path 
from apps.users.api.apy import userAPIView, userDetail #UserAPIView

urlpatterns = [
    #path('usuarios/',UserAPIView.as_view()) #agregamos la urls, luego a urls.py pero del proyecto 
    #al no usar mas la clase se importa la función userAPIView desde apy.py y como es función no se necesita as_view
    path('usuarios/',userAPIView, name= 'usuario-api'),
    path('usuarios/<int:pk>/',userDetail, name= 'usuario-api-detalle'),
]