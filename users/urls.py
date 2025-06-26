from django.urls import path

from users import views

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register-user'),
    path('login/', views.UserLoginView.as_view(), name='login-user')
]