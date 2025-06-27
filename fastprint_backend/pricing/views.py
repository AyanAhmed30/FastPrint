from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import *
from .pricing_engine import calculate_book_price
from .serializers import get_option_serializer


class DropdownOptionsView(APIView):
    permission_classes = [AllowAny]  # ✅ No authentication needed

    def get(self, request):
        return Response({
            "binding_types": get_option_serializer(BindingType)(BindingType.objects.all(), many=True).data,
            "spine_types": get_option_serializer(SpineType)(SpineType.objects.all(), many=True).data,
            "exterior_colors": get_option_serializer(ExteriorColor)(ExteriorColor.objects.all(), many=True).data,
            "foil_stampings": get_option_serializer(FoilStamping)(FoilStamping.objects.all(), many=True).data,
            "screen_stampings": get_option_serializer(ScreenStamping)(ScreenStamping.objects.all(), many=True).data,
            "corner_protectors": get_option_serializer(CornerProtector)(CornerProtector.objects.all(), many=True).data,
            "interior_colors": get_option_serializer(InteriorColor)(InteriorColor.objects.all(), many=True).data,
            "paper_types": get_option_serializer(PaperType)(PaperType.objects.all(), many=True).data
        })


class PricingCalculationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            print("📦 Received Data:", request.data)  # <-- Debug log
            result = calculate_book_price(request.data)
            return Response(result)
        except Exception as e:
            print("❌ Error in calculation:", str(e))  # <-- Show error
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

