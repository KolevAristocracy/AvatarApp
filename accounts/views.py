from django.contrib.auth.views import LoginView, UserModel
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from accounts.forms import CustomUserCreationForm, EditUserForm
from accounts.models import CustomUser
from accounts.utils import get_profile


# Create your views here.
class UserRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/register-user.html'
    success_url = reverse_lazy('index-page')


# class UserLoginView(LoginView):
#     template_name = 'accounts/login-user.html'
#     redirect_authenticated_user = True
#     success_url = reverse_lazy('index-page')

class UserEditView(UpdateView):
    model = CustomUser
    form_class = EditUserForm
    template_name = 'accounts/edit-profile.html'
    context_object_name = 'form'
    success_url = reverse_lazy('profile-details')

    def get_object(self, queryset = ...):
        return get_profile(self.request.user.pk)


class UserDetailsView(DetailView):
    model = CustomUser
    template_name = 'accounts/profile-details.html'

    def get_object(self, queryset = ...):
        return get_profile(self.request.user.pk)