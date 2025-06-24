from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_book(request):
    serializer = BookSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        book = serializer.save()
        return Response(BookSerializer(book).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_books(request):
    books = Book.objects.filter(user=request.user)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_book_detail(request, pk):
    try:
        book = Book.objects.get(pk=pk, user=request.user)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=404)
    return Response(BookSerializer(book).data)

