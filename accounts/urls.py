from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('api/auth/register/', views.RegisterView.as_view(), name='api_register'),
    path('api/auth/login/', views.login_view, name='api_login'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='api_refresh'),
    path('api/auth/logout/', views.logout_view, name='api_logout'),
    path('api/auth/me/', views.me_view, name='api_me'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
]
