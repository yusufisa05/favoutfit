from django.urls import path
from . import views

urlpatterns = [
    path('odeme/',views.order_create,name='order_create'),
    path('gecmis/',views.order_history,name='order_history'),
    path('detay/<int:order_id>/',views.order_detail,name='order_detail'),
]