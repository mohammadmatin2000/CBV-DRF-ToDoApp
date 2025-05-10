from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import UserSerializer
from ...models import ToDoApp
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .paginations import CustomPagination
from .permissions import IsOwnerOrReadOnly


# ======================================================================================================================
# TaskViewSet: A ModelViewSet for managing tasks in the ToDoApp API
class TaskViewSet(ModelViewSet):
    """
    This ViewSet provides full CRUD (Create, Read, Update, Delete) operations for ToDoApp objects.
    """

    queryset = (
        ToDoApp.objects.all()
    )  # Retrieves all task objects from the database

    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]
    # - `IsAuthenticatedOrReadOnly`: Allows read access for unauthenticated users, but requires authentication for modifications.
    # - `IsOwnerOrReadOnly`: Restricts edits to task owners while allowing read access for others.

    serializer_class = UserSerializer  # Defines the serializer used for transforming tasks into JSON format

    filter_backends = (
        SearchFilter,
        OrderingFilter,
        DjangoFilterBackend,
    )
    # - Enables **search**, **ordering**, and **filtering** functionality.

    filterset_fields = {
        "id": [
            "exact"
        ],  # Enables filtering tasks by an exact ID match
        "content": [
            "exact"
        ],  # Allows exact text matching for task content
        "author": [
            "exact",
            "in",
        ],  # Supports filtering by an exact author or multiple authors
    }

    pagination_class = CustomPagination  # Specifies a custom pagination class for managing paginated responses

    search_fields = [
        "author",
        "content",
    ]  # Enables search functionality across author and content fields

    ordering_fields = [
        "id"
    ]  # Allows tasks to be ordered based on their ID


# ======================================================================================================================
