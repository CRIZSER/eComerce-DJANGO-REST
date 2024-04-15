from django.urls import path 
from apps.products.api.views.general_views import MeasureUnitListAPIView, IndicatorListAPIView, categoryProductListAPIView
from apps.products.api.views.products_views import ProductListApiView, ProductCreateApiView, ProductListCreateApiView, ProductRetriveApiView, ProductDestroyApiView, ProductUpdateApiView, ProductRetrieveUpdate, ProductRetriveDestroy,ProductRetrieveUpdataDestroy

urlpatterns = [
    #path('usuarios/',UserAPIView.as_view()) #agregamos la urls, luego a urls.py pero del proyecto 
    #al no usar mas la clase se importa la función userAPIView desde apy.py y como es función no se necesita as_view
    path('measure_unit/',MeasureUnitListAPIView.as_view(), name= 'measure_unit-api'), #as_view porque es clase
    path('indicator/',IndicatorListAPIView.as_view(), name= 'indicator-api'), #as_view porque es clase


    #el view set al tener todo el crud no necesita de las url de debajo
    #path('category_product/',categoryProductListAPIView.as_view(), name= 'category-api'), #as_view porque es clase
    #path('product/list/',ProductListApiView.as_view(), name= 'product-api'),
    #path('product/create/',ProductCreateApiView.as_view(), name= 'product-create-api'),
    #path('product/retrieve/<int:pk>',ProductRetriveApiView.as_view(), name= 'product-retrive-api'),
    #path('product/destroy/<int:pk>',ProductDestroyApiView.as_view(), name= 'product-destroy-api'),
    #path('product/update/<int:pk>',ProductUpdateApiView.as_view(), name= 'product-update-api'),

    #path('product/retrive-destroy/<int:pk>',ProductRetriveDestroy.as_view(), name= 'product-retrive-destroy-api'),
    #path('product/retrive-update/<int:pk>',ProductRetrieveUpdate.as_view(), name= 'product-retrive-update-api'),

    #path('product/list/create/',ProductListCreateApiView.as_view(), name= 'product-list-create-api'), #los 2 mas importantes, ya que resumen todos los anteriores de productos
    #path('product/retrive-update-destroy/<int:pk>',ProductRetrieveUpdataDestroy.as_view(), name= 'product-retrive-update-destroy-api'),
]