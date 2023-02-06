from django.urls import path

from . import views


urlpatterns = [
    path('', views.ProjectListCreateAPIView.as_view(), name='projects'),
    path('<int:pk>/', views.ProjectDetailAPIView.as_view(), name='project_detail'),
    path('<int:pk>/users/', views.ProjectUsersAPIView.as_view(), name='project_users'),
    path('<int:pk>/users/<str:username>/', views.delete_user_from_project, name='project_users'),
    path('<int:pk>/tasks/', views.ProjectTasksAPIView.as_view(), name='project_tasks')
]
