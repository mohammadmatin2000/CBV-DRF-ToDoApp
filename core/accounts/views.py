from django.views.generic import CreateView
from .models import User
# ======================================================================================================================
class SignUpView(CreateView):
    model = User
    fields = ('email', 'password')
    template_name = "registration/sign_up.html"
    success_url = "/accounts/login/"
# ======================================================================================================================