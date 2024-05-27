from rest_framework import viewsets, status
from apps.base.api import GeneralListApiView
from apps.products.models import MeasureUnit, Indicator, CategoryProduct
from apps.products.api.serializers.general_serializer import MeasureUnitSerializer, indicatorSerializer, categoryProductSerializer
from django.http import HttpResponse
from rest_framework.response import Response

#aqui estara lo globlar, o en su defecto aquello que es más manejado por el admin de manera interna y que se presenta a los usuarios 
class MeasureUnitViewSet(viewsets.ModelViewSet): #viewsets.ViewSet no define todo los metodos por defecto, con modelViewSet debemos definir el queryset
    #indicar serilizador
    serializer_class = MeasureUnitSerializer #es una forma de definir qué serializador utilizar en una vista de Django Rest Framework para convertir los objetos de Django en JSON y viceversa.
    #convierte lo retornado por get_queryset
    #https://www.cdrf.co/3.1/rest_framework.generics/GenericAPIView.html aqui esta mostrado el flujo de ejecución

    def get_queryset(self):
        return MeasureUnit.objects.filter(state = True) #todo este proceso es similar a relizarlo mediante funcion en el cual identificamos get en apy.py para users
        #retorna en formato json

class IndicatorViewSet(viewsets.ModelViewSet): 
    #indicar serilizador
    serializer_class = indicatorSerializer

    def get_queryset(self):
        return Indicator.objects.filter(state = True) #todo este proceso es similar a relizarlo mediante funcion en el cual identificamos get
        #retorna en formato json

class categoryProductViewSet(viewsets.ModelViewSet): 
    #indicar serilizador

    """Hola comentario de ruta, para agregar datos en funciones especificas como list o delete, se debe generar el método"""

    serializer_class = categoryProductSerializer

    def get_queryset(self):
        return CategoryProduct.objects.filter(state = True)
    
    def list(self, request, *args, **kwargs):
        """
        Retorna todas la categorias de producto
        
        
        Con 2 comentarios el de arriba aparece al lado de la ruta, en caso de solo querer mostar ciertos campos se debe modificar la clase meta en modelos
        """
        queryset = self.get_queryset()
        serializer_data = self.get_serializer(queryset, many = True)
        return Response(serializer_data, status = status.HTTP_200_OK)

#para swagger 

