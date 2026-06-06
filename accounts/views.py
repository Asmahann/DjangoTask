from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomUserCreationForm

class SignUpView(generic.CreateView):
    """
    Renders the sign-up page and handles user registration.
    """
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class UserLoginView(LoginView):
    """
    Renders the login page and handles user authentication.
    """
    template_name = 'registration/login.html'

class UserLogoutView(LogoutView):
    """
    Handles logging out the user and redirects to the login page.
    """
    next_page = 'login'
