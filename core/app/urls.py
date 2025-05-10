from django.urls import path, include
from .views import (
    CreateTaskView,
    TaskListView,
    DeleteTaskView,
    UpdateTaskView,
)

# ======================================================================================================================
# Setting the application namespace to 'app' for URL reversibility
app_name = "app"

# Defining URL patterns for task-related views
urlpatterns = [
    # Maps '/' to TaskListView, displaying a list of tasks
    path("", TaskListView.as_view(), name="task-list"),
    # Maps '/create-task/' to CreateTaskView, allowing users to create new tasks
    path(
        "create-task/", CreateTaskView.as_view(), name="create-task"
    ),
    # Maps '/delete-task/<int:pk>/' to DeleteTaskView, enabling task deletion by primary key (pk)
    path(
        "delete-task/<int:pk>/",
        DeleteTaskView.as_view(),
        name="delete-task",
    ),
    # Maps '/update-task/<int:pk>/' to UpdateTaskView, handling task updates by primary key (pk)
    path(
        "update-task/<int:pk>/",
        UpdateTaskView.as_view(),
        name="update-task",
    ),
    # Includes API version 1 URLs from the 'app.api.v1.urls' module
    path("api/v1/", include("app.api.v1.urls")),
]

# ======================================================================================================================
