from apps.products.models import MeasureUnit,CategoryProduct,Indicator

from rest_framework import serializers

class MeasureUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasureUnit
        exclude = ('state',) #no se retorna porque no se usara

class categoryProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryProduct
        exclude = ('state',) #no se retorna porque no se usara

class indicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator
        exclude = ('state',) #no se retorna porque