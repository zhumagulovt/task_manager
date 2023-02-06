from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path('auth/registration/', views.RegistrationAPIView.as_view(), name='registration'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/change_password/', views.ChangePasswordAPIView.as_view(), name='change_password'),
    path('auth/profile/', views.ProfileAPIView.as_view(), name='profile'),
    path('<str:username>/projects/', views.UserProjectsListAPIView.as_view(), name='user_projects'),
    path('<str:username>/tasks/', views.UserTasksListAPIView.as_view(), name='user_tasks'),
    path('<str:username>/', views.UserRetrieveAPIView.as_view(), name='user_detail'),
    path('', views.UserListAPIView.as_view(), name='user_list')
]
