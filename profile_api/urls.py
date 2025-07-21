from django.urls import path

from profile_api.views import UserProfileAPIView

urlpatterns = [
    path('profile/', UserProfileAPIView.as_view(), name='api-profile'),
]