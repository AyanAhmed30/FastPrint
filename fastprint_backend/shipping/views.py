# shipping/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ShippingAddress
from .serializers import ShippingAddressSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_shipping_address(request):
    data = request.data.copy()
    data['user'] = request.user.id
    serializer = ShippingAddressSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Shipping address saved successfully'}, status=201)
    return Response(serializer.errors, status=400)
