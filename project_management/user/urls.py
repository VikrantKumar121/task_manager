from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet,LoginViewSet, SignUpViewSet, LogoutViewSet


urlpatterns = [
    path('user',UserViewSet.as_view()),
    path('user/',UserViewSet.as_view()),
    path('user/<str:pk>',UserViewSet.as_view()),
    path('login',LoginViewSet.as_view()),
    path('logout',LogoutViewSet.as_view()),
    path('signup',SignUpViewSet.as_view()),
]
