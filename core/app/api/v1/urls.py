from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

# ======================================================================================================================
# Creating a DefaultRouter instance, which automatically generates API URL routes for ViewSets
router = DefaultRouter()

# Registering the TaskViewSet with the router
# - This automatically sets up standard API endpoints for task management
# - The basename 'tasks' defines the URL prefix for task-related endpoints (e.g., /tasks/)
router.register("tasks", TaskViewSet, basename="tasks")

# Using router-generated URLs as the urlpatterns
# - Instead of manually defining paths, this simplifies API endpoint creation
urlpatterns = router.urls

# ======================================================================================================================
