from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts import views

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register-user'),
    path('login/', LoginView.as_view(template_name='accounts/login-user.html'), name='login-user'),
    path('logout/', LogoutView.as_view(), name='logout-user'),
    path('edit/', views.UserEditView.as_view(), name='edit-profile'),
    path('details/', views.UserDetailsView.as_view(), name='profile-details'),
]