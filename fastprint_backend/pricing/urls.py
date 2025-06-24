# pricing/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('calculate/', views.get_price_estimate, name='get-price-estimate'),     # Public price calculator
    path('binding-type/<int:pk>/', views.update_binding_type, name='update-binding-type'),  # Admin only
]
