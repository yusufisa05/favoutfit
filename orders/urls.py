from django.urls import path
from . import views

urlpatterns = [
    path('odeme/',views.order_create,name='order_create')
]