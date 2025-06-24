from .models import *
from decimal import Decimal

def calculate_book_price(trim_size, binding_type, spine_type, exterior_color,
                         foil_stamping, screen_stamping, corner_protector,
                         interior_color, paper_type, page_count, quantity, state):
    try:
        total = Decimal('0.00')

        # ✅ Validate trim size
        if not TrimSize.objects.filter(name=trim_size).exists():
            raise ValueError(f"Invalid Trim Size: {trim_size}")

        total += BindingType.objects.get(name=binding_type).price
        if spine_type:
            total += SpineType.objects.get(name=spine_type).price
        if exterior_color:
            total += ExteriorColor.objects.get(name=exterior_color).price
        if foil_stamping:
            total += FoilStamping.objects.get(name=foil_stamping).price
        if screen_stamping:
            total += ScreenStamping.objects.get(name=screen_stamping).price
        if corner_protector:
            total += CornerProtector.objects.get(name=corner_protector).price

        total += InteriorColor.objects.get(name=interior_color).price_per_page * Decimal(page_count)
        total += PaperType.objects.get(name=paper_type).price_per_page * Decimal(page_count)

        total_cost = total * Decimal(quantity)
        tax = total_cost * Decimal('0.0825') if state == 'TX' else Decimal('0.00')
        final_amount = total_cost + tax

        return {
            'cost_per_book': round(total, 2),
            'total_cost': round(total_cost, 2),
            'tax': round(tax, 2),
            'final_amount': round(final_amount, 2)
        }

    except Exception as e:
        print("Error in pricing logic:", e)
        return None
