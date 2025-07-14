from django.urls import path

from common import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index-page'),
    path('contacts/', views.ContactFormView.as_view(), name='contact-page'),
]