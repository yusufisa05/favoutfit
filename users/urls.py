from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('kaydol', views.register,name='register'),
    path('giris', auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('cikis', auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout')
]