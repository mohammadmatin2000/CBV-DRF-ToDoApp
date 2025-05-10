from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# ======================================================================================================================
# Generating API documentation using drf-yasg (Django REST Framework - Yet Another Swagger Generator)
schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",  # API title displayed in Swagger UI
        default_version="v1",  # API version
        description="Test description",  # Description of the API
        terms_of_service="https://www.google.com/policies/terms/",  # Link to terms of service
        contact=openapi.Contact(
            email="contact@snippets.local"
        ),  # API contact information
        license=openapi.License(
            name="BSD License"
        ),  # API license details
    ),
    public=True,  # Makes the API documentation publicly accessible
    permission_classes=(
        permissions.AllowAny,
    ),  # Grants access to any user without authentication
)
# ======================================================================================================================
# Defining URL patterns for the Django application
urlpatterns = [
    # Django Admin Panel
    path("admin/", admin.site.urls),
    # Including routes for the 'app' application
    path("", include("app.urls")),
    # Including authentication-related routes for user management
    path("accounts/", include("accounts.urls")),
    # Django REST framework built-in authentication views (login, logout, etc.)
    path("api-auth/", include("rest_framework.urls")),
    # API documentation routes using Swagger UI and ReDoc
    path(
        "swagger/output.json",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),  # JSON schema output
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),  # Swagger UI
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),  # ReDoc UI
]
# ======================================================================================================================
# Serving media and static files in development mode
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )  # Handles media files
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )  # Handles static files
# ======================================================================================================================
