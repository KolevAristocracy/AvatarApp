from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import UserRegisterForm, UserLoginForm
from users.models import User


# Create your views here.
class UserRegisterView(CreateView):
    model = User
    template_name = 'users/register-user.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('index-page')
    context_object_name = 'form'


class UserLoginView(LoginView):
    template_name = 'users/login-user.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('index-page')