from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, FormView
from accounts.forms import CustomUserCreationForm, EditUserForm, ChangePasswordForm, CustomAuthenticationForm
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
    form_class = CustomAuthenticationForm
    redirect_authenticated_user = True

class UserEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = EditUserForm
    template_name = 'accounts/edit-profile.html'
    context_object_name = 'form'
    success_url = reverse_lazy('profile-details')

    def get_object(self, queryset = ...):
        return self.request.user.profile


class ChangePasswordView(LoginRequiredMixin, FormView):
    template_name = 'accounts/change-password.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy('login-user') # after changing password, need to login again

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.request.user.set_password(form.cleaned_data['new_password1'])
        self.request.user.save()
        change_successfully_msg = "Password changed successfully. Please log in again."
        messages.success(self.request, message=change_successfully_msg)
        return super().form_valid(form)


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





