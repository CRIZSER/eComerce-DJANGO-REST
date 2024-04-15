from rest_framework import generics
from apps.base.api import GeneralListApiView
from apps.products.models import MeasureUnit, Indicator, CategoryProduct
from apps.products.api.serializers.general_serializer import MeasureUnitSerializer, indicatorSerializer, categoryProductSerializer

#aqui estara lo globlar, o en su defecto aquello que es más manejado por el admin de manera interna y que se presenta a los usuarios 
class MeasureUnitListAPIView(generics.ListAPIView): #listApiView lista informacion, reconoce get
    #indicar serilizador
    serializer_class = MeasureUnitSerializer #es una forma de definir qué serializador utilizar en una vista de Django Rest Framework para convertir los objetos de Django en JSON y viceversa.
    #convierte lo retornado por get_queryset
    #https://www.cdrf.co/3.1/rest_framework.generics/GenericAPIView.html aqui esta mostrado el flujo de ejecución

    def get_queryset(self):
        return MeasureUnit.objects.filter(state = True) #todo este proceso es similar a relizarlo mediante funcion en el cual identificamos get en apy.py para users
        #retorna en formato json

class IndicatorListAPIView(generics.ListAPIView): #listApiView lista informacion, reconoce get
    #indicar serilizador
    serializer_class = indicatorSerializer

    def get_queryset(self):
        return Indicator.objects.filter(state = True) #todo este proceso es similar a relizarlo mediante funcion en el cual identificamos get
        #retorna en formato json

class categoryProductListAPIView(GeneralListApiView): #para este caso ocupamos generalListApi de base para no tener que definir siempre get_query set
    #indicar serilizador
    serializer_class = categoryProductSerializer

