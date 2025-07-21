from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('common.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('quiz/', include('quiz_system.urls')),
    path('user/', include('accounts.urls')),
    path('api/', include('profile_api.urls')),


]
