from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import SimpleRouter

from . import views
from .viewsets import UserViewSet

router = SimpleRouter()
router.register('', UserViewSet, 'user')

urlpatterns = [
    path('auth/registration/', views.RegistrationAPIView.as_view(), name='registration'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/change_password/', views.ChangePasswordAPIView.as_view(), name='change_password'),
    path('<str:username>/projects/', views.UserProjectsListAPIView.as_view(), name='user_projects'),
    path('', include(router.urls))
]
