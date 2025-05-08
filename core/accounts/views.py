from django.views.generic import CreateView
from .models import User
# ======================================================================================================================
# SignUpView: A class-based view for user registration
class SignUpView(CreateView):
    """
    This view allows users to create an account by signing up.
    """

    model = User  # Specifies the model that this view interacts with (User model)

    fields = ('email', 'password')
    # Defines the fields to be included in the registration form.
    # Note: The password field should be handled securely (e.g., hashed before saving).

    template_name = "registration/sign_up.html"
    # Specifies the HTML template used for rendering the sign-up form.

    success_url = "/"
    # Redirects the user to the homepage upon successful registration.

# ======================================================================================================================