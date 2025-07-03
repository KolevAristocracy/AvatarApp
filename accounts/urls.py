from django.contrib.auth.views import LogoutView
from django.urls import path

from accounts import views
from accounts.views import UserLoginView

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register-user'),
    path('login/', UserLoginView.as_view(),name='login-user'),
    path('logout/', LogoutView.as_view(), name='logout-user'),
    path('edit/', views.UserEditView.as_view(), name='edit-profile'),
    path('details/', views.UserDetailsView.as_view(), name='profile-details'),
    path('delete/', views.UserDeleteView.as_view(), name='delete-account'),
]