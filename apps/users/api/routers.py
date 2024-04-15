from rest_framework.routers import DefaultRouter #importamos el router 
from apps.users.api.view.views import UserViewSet

router = DefaultRouter()

router.register(r'user', UserViewSet)

urlpatterns = router.urls