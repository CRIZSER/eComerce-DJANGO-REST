from django.contrib import admin
from apps.products.models import Products, CategoryProduct, Indicator, MeasureUnit

# Register your models here.
class MeasureUnitAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')

class CategoryProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')

admin.site.register(Products)
admin.site.register(CategoryProduct, CategoryProductAdmin)
admin.site.register(Indicator)
admin.site.register(MeasureUnit, MeasureUnitAdmin)