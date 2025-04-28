from django.urls import path
from .views import CreateTaskView, TaskListView, DeleteTaskView, UpdateTaskView
# ======================================================================================================================
app_name = 'app'
urlpatterns = [
    path('',TaskListView.as_view(), name='task-list'),
    path('create-task/', CreateTaskView.as_view(), name='create-task'),

    path('delete-task/<int:pk>/', DeleteTaskView.as_view(), name='delete-task'),

    path('update-task/<int:pk>/', UpdateTaskView.as_view(), name='update-task'),
]
# ======================================================================================================================