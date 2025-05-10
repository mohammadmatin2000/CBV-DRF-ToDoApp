from django.urls import path, include
from .views import SignUpView

# ======================================================================================================================
# Setting the application namespace to 'accounts' for better URL reversibility and organization
app_name = "accounts"

# Defining URL patterns for user authentication
urlpatterns = [
    # Maps '/signup/' to the SignUpView class-based view, handling user registration
    path("api/v1/", include("accounts.api.v1.urls")),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("", include("django.contrib.auth.urls")),
]
# ======================================================================================================================
