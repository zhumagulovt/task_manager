from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import SimpleRouter

from .views import RegistrationAPIView
from .viewsets import UserViewSet

router = SimpleRouter()
router.register('', UserViewSet, 'user')

urlpatterns = [
    path('auth/registration/', RegistrationAPIView.as_view(), name='registration'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls))
]
