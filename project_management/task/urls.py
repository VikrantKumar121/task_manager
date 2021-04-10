from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, SubTaskViewSet, ProjectTaskViewSet, ProjectRootTaskViewSet

# router = DefaultRouter()
# router.register('task', TaskViewSet, basename = 'task')

urlpatterns = [
    # path('',include(router.urls))
    path('subtask',SubTaskViewSet.as_view()),
    path('subtask/',SubTaskViewSet.as_view()),
    path('subtask/<str:pk>',SubTaskViewSet.as_view()),
    path('task',TaskViewSet.as_view()),
    path('task/',TaskViewSet.as_view()),
    path('task/<str:pk>',TaskViewSet.as_view()),
    path('project/<str:project_id>/alltasks',ProjectTaskViewSet.as_view()),
    path('project/<str:project_id>/alltasks/<str:pk>',ProjectTaskViewSet.as_view()),
    path('project/<str:project_id>/task',ProjectRootTaskViewSet.as_view()),
    path('project/<str:project_id>/task/<str:pk>',ProjectRootTaskViewSet.as_view())
]
