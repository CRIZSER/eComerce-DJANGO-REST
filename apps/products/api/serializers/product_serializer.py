from apps.products.models import Products
from apps.products.api.serializers.general_serializer import MeasureUnitSerializer, categoryProductSerializer
from rest_framework import serializers

#creamos este archivo ya que products al ser el model mas grande y especifico el mismo puede ser variado muchas veces, por lo tanto es meojkr tener su propio archivo

class ProductSerializer(serializers.ModelSerializer):
    #primera forma para mostar los datos de las llaves foraneas
    #mesureUnit = MeasureUnitSerializer() #de esta manera nos muestra todo el contenido de unidad de medida
    #categoryProduct =categoryProductSerializer()

    #segunda forma para mostar los datos de las llaves foraneas
    #mesureUnit = serializers.StringRelatedField() #de esta manera nos muestra el contenido del metodo __str__
    #categoryProduct =serializers.StringRelatedField()


    class Meta: 
        model = Products
        exclude = ('state',)
    
    #tercera forma para mostar los datos de las llaves foraneas
    def to_representation(self, instance : Products): 
        data = super().to_representation(instance) #obtenmos los datos
 
        filtered_data = {
                'id': instance.id, 
                'name': instance.name,
                'description': instance.description,
                'image': instance.image or '',#para casos en los que la imagen sea opcional 
                'measure_unit': instance.mesureUnit.description if instance.mesureUnit is not None else '', #lo ideal es hacer esto para cada relación que se tenga
                'category_product': instance.categoryProduct.description if instance.categoryProduct is not None else '',     
            }
        return filtered_data