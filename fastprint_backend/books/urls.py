from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_book, name='create-book'),
    path('my/', views.my_books, name='my-books'),
    path('<int:pk>/', views.get_book_detail, name='book-detail'),
]
