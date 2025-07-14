# shipping/urls.py
from django.urls import path
from .views import save_shipping_address

urlpatterns = [
    path('save-shipping/', save_shipping_address, name='save-shipping'),
]
