from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import BindingType
from .serializers import BindingTypeSerializer
from .utils import calculate_book_price

# ✅ Anyone can estimate price
@api_view(['POST'])
@permission_classes([AllowAny])
def get_price_estimate(request):
    data = request.data
    try:
        result = calculate_book_price(
            trim_size=data.get('trim_size'),
            binding_type=data.get('binding_type'),
            spine_type=data.get('spine_type', ''),
            exterior_color=data.get('exterior_color', ''),
            foil_stamping=data.get('foil_stamping', ''),
            screen_stamping=data.get('screen_stamping', ''),
            corner_protector=data.get('corner_protector', ''),
            interior_color=data.get('interior_color'),
            paper_type=data.get('paper_type'),
            page_count=int(data.get('page_count', 0)),
            quantity=int(data.get('quantity', 1)),
            state=data.get('state', '')
        )
        if not result:
            return Response({"error": "Invalid pricing configuration."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(result)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ✅ Admin-only API to update BindingType
@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_binding_type(request, pk):
    try:
        binding = BindingType.objects.get(pk=pk)
    except BindingType.DoesNotExist:
        return Response({'error': 'BindingType not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = BindingTypeSerializer(binding, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
