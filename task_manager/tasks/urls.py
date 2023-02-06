from django.urls import path

from . import views

urlpatterns = [
    path('', views.CreateTaskAPIView.as_view(), name='task_create'),
    path('<int:pk>/', views.TaskRetrieveAPIView.as_view()),
    path('<int:pk>/completed/', views.TaskCompletedAPIView.as_view())
]
