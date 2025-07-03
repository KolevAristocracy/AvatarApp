from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView

from accounts.forms import CustomUserCreationForm, EditUserForm
from accounts.models import CustomUser, Profile
from accounts.utils import get_customuser


# Create your views here.
class UserRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/register-user.html'
    success_url = reverse_lazy('index-page')

    # Uses signal to create the profile


class UserLoginView(LoginView):
    template_name = 'accounts/login-user.html'
    redirect_authenticated_user = True

class UserEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = EditUserForm
    template_name = 'accounts/edit-profile.html'
    context_object_name = 'form'
    success_url = reverse_lazy('profile-details')

    def get_object(self, queryset = ...):
        return self.request.user.profile



class UserDetailsView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'accounts/profile-details.html'

    def get_object(self, queryset = ...):
        return get_customuser(self.request.user.pk)


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'accounts/delete-account.html'
    success_url = reverse_lazy('index-page')

    def get_object(self, queryset = ...):
        return get_customuser(self.request.user.pk)