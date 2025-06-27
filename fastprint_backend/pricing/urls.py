from django.urls import path
from .views import DropdownOptionsView, PricingCalculationView

urlpatterns = [
    path('options/', DropdownOptionsView.as_view(), name='pricing-options'),
    path('calculate/', PricingCalculationView.as_view(), name='pricing-calculate'),
]
