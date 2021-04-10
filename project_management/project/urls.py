from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet


urlpatterns = [
    path('project',ProjectViewSet.as_view()),
    path('project/',ProjectViewSet.as_view()),
    path('project/<str:pk>',ProjectViewSet.as_view())
]
