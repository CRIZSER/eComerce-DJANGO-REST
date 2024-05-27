from rest_framework.routers import DefaultRouter #importamos el router 
from apps.products.api.views.products_views import ProductViewSet #importamos el viewset
from apps.products.api.views.general_views import * #importamos el viewset

router = DefaultRouter()

router.register(r'product', ProductViewSet, basename='product')
router.register(r'measure-unit', MeasureUnitViewSet, basename='measure-unit')
router.register(r'indicators', IndicatorViewSet, basename='indicators')
router.register(r'category-products', categoryProductViewSet, basename='category-products')

urlpatterns = router.urls