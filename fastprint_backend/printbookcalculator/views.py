from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from .utils import get_available_bindings  # make sure it's imported

from decimal import Decimal


# ✅ GET dropdowns — public access
@api_view(['GET'])
@permission_classes([AllowAny])
def get_dropdowns(request):
    trim_sizes = TrimSizeSerializer(TrimSize.objects.all(), many=True).data
    interior_colors = InteriorColorSerializer(InteriorColor.objects.all(), many=True).data
    paper_types = PaperTypeSerializer(PaperType.objects.all(), many=True).data
    cover_finishes = CoverFinishSerializer(CoverFinish.objects.all(), many=True).data

    return Response({
        'trim_sizes': trim_sizes,
        'interior_colors': interior_colors,
        'paper_types': paper_types,
        'cover_finishes': cover_finishes
    })


# ✅ GET bindings based on trim and page count — public access
@api_view(['GET'])
@permission_classes([AllowAny])
def get_bindings_by_trim_and_page_count(request):
    try:
        trim_size_id = int(request.GET.get('trim_size_id'))
        page_count = int(request.GET.get('page_count'))
    except (TypeError, ValueError):
        return Response({'error': 'Invalid or missing parameters.'}, status=status.HTTP_400_BAD_REQUEST)

    # ✅ Get allowed binding names based on page count
    allowed_names = get_available_bindings(page_count)

    # ✅ Filter by trim size, page count range, and allowed names
    bindings = BindingType.objects.filter(
        trim_size_id=trim_size_id,
        min_pages__lte=page_count,
        max_pages__gte=page_count,
        name__in=allowed_names  # ✅ Add this filter
    )

    serialized = BindingTypeSerializer(bindings, many=True)
    return Response(serialized.data)

# ✅ POST cost calculation — public access
@api_view(['POST'])
@permission_classes([AllowAny])
def calculate_cost(request):
    try:
        data = request.data
        page_count = int(data['page_count'])
        quantity = int(data['quantity'])

        binding = BindingType.objects.get(id=data['binding_id'])
        interior = InteriorColor.objects.get(id=data['interior_color_id'])
        paper = PaperType.objects.get(id=data['paper_type_id'])
        cover = CoverFinish.objects.get(id=data['cover_finish_id'])
    except (KeyError, ValueError, BindingType.DoesNotExist, InteriorColor.DoesNotExist,
            PaperType.DoesNotExist, CoverFinish.DoesNotExist) as e:
        return Response({'error': f'Invalid data or missing fields: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    per_book_cost = (
        Decimal(binding.price)
        + Decimal(interior.price_per_page) * page_count
        + Decimal(paper.price_per_page) * page_count
        + Decimal(cover.price)
    )

    total_cost = per_book_cost * quantity

    return Response({
        'cost_per_book': round(per_book_cost, 2),
        'total_cost': round(total_cost, 2)
    })
