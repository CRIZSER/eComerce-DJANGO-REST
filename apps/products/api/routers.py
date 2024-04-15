from rest_framework.routers import DefaultRouter #importamos el router 
from apps.products.api.views.products_views import ProductViewSet #importamos el viewset

router = DefaultRouter()

router.register(r'product', ProductViewSet)

urlpatterns = router.urls