from django.urls import path

from dashboard.views import dashboard_view, index_view

urlpatterns = [
    path('', index_view, name='index_view'),
    path('dashboard/', dashboard_view, name='dashboard')
]