from django.urls import path
from . import views

urlpatterns = [
    path('dropdowns/', views.get_comic_dropdowns),
    path('bindings/', views.get_comic_bindings),
    path('calculate/', views.calculate_comic_cost),
]