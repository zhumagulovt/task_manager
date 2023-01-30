from django.urls import path

from . import views


urlpatterns = [
    path('', views.ProjectCreateAPIView.as_view(), name='projects')
]
