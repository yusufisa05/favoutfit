from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('kaydol/', views.register, name='register'),
    path('kaydol', views.register, name='register_noslash'),
    path('giris/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('giris', auth_views.LoginView.as_view(template_name='users/login.html'), name='login_noslash'),
    path('cikis/', views.user_logout, name='logout'),
    path('cikis', views.user_logout, name='logout_noslash'),
]