from django.urls import include, path
from .views import (RegisterApiView, CustomAuthToken, CustomProfileView, CustomChangePasswordView,
                    CustomActivationView, CustomActivationResendView, CustomResetPasswordView,CustomDeleteToken)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# ======================================================================================================================
# Setting the application namespace for URL reversibility and organization
app_name = 'api-v1'

# Defining URL patterns for authentication and user account management
urlpatterns = [
    # User Registration
    path("register/", RegisterApiView.as_view(), name="register"),
    # - Maps '/register/' to the **RegisterApiView** handling user sign-up.

    # Account Activation
    path('activate/<str:token>', CustomActivationView.as_view(), name="activate"),
    # - Maps '/activate/<token>' to **CustomActivationView**, activating a user account via a unique token.

    # Resend Activation Email
    path('activate/resend/', CustomActivationResendView.as_view(), name="resend"),
    # - Maps '/activate/resend/' to **CustomActivationResendView**, allowing users to resend the activation link.

    # Change Password
    path('change_password/', CustomChangePasswordView.as_view(), name="change-password"),
    # - Maps '/change_password/' to **CustomChangePasswordView**, handling password updates.

    # Reset Password
    path('reset/password/', CustomResetPasswordView.as_view(), name="reset-password"),
    # - Maps '/reset/password/' to **CustomResetPasswordView**, allowing users to reset passwords via email verification.

    # Login using Custom Auth Token
    path("login/token/", CustomAuthToken.as_view(), name="login"),
    # - Maps '/login/token/' to **CustomAuthToken**, handling authentication via token-based login.
    path('logout/token/', CustomDeleteToken.as_view(), name="delete-token"),

    # JWT Authentication Routes
    path('jwt/token/create/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # - Generates **access & refresh tokens** using **TokenObtainPairView**.

    path('jwt/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # - Refreshes **access tokens** using **TokenRefreshView**.

    path('jwt/token/verify/', TokenObtainPairView.as_view(), name='token_verify'),
    # - Verifies a JWT token for authentication.

    # Profile Information
    path('profile/', CustomProfileView.as_view(), name='profile'),
    # - Maps '/profile/' to **CustomProfileView**, displaying user account details.

]
# ======================================================================================================================