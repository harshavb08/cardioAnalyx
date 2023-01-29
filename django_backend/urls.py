from django.contrib import admin
from django.urls import include, path
from dashboard.views import register, login, forgot_password, logout
urlpatterns = [
    path('', include('home.urls')),
    path('api/', include('api.urls')),
    path('client/', include('client.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('register/', register),
    path('login/', login),
    path('logout/', logout),
    path('accounts/', include('allauth.urls')),
    path('accounts/login/', login),
    path('forgot/', forgot_password),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
