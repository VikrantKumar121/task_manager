from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrganizationViewSet

urlpatterns = [
    path('org',OrganizationViewSet.as_view()),
    path('org/',OrganizationViewSet.as_view()),
    path('org/<str:pk>',OrganizationViewSet.as_view())
]
