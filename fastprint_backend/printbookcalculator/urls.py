from django.urls import path
from . import views

urlpatterns = [
    path('dropdowns/', views.get_dropdowns, name='get_dropdowns'),
    path('bindings/', views.get_bindings_by_trim_and_page_count, name='get_bindings_by_trim_and_page_count'),
    path('calculate/', views.calculate_cost, name='calculate_cost'),
]
