from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import CustomUserCreationForm
from accounts.models import CustomUser


# Create your views here.
class UserRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/register-user.html'
    success_url = reverse_lazy('index-page')


# class UserLoginView(LoginView):
#     template_name = 'accounts/login-user.html'
#     redirect_authenticated_user = True
#     success_url = reverse_lazy('index-page')