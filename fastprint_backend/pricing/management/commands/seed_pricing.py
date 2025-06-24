from django.core.management.base import BaseCommand
from pricing.models import BindingType, InteriorColor, PaperType, Spine, ExteriorColor, FoilStamping, ScreenStamping, CornerProtector, TrimSize

class Command(BaseCommand):
    help = 'Seeds the pricing tables'

    def handle(self, *args, **kwargs):
        # Binding types
        BindingType.objects.get_or_create(name="Leather Case Wrap", defaults={'price': 79.00})
        BindingType.objects.get_or_create(name="Faux Leather Case Wrap", defaults={'price': 69.00})
        BindingType.objects.get_or_create(name="Polythin Rexine Case Wrap", defaults={'price': 59.00})

        # Interior Colors
        InteriorColor.objects.get_or_create(name="Premium Color", defaults={'price': 0.19})
        InteriorColor.objects.get_or_create(name="Premium Black & white", defaults={'price': 0.03})

        # Paper Types
        PaperType.objects.get_or_create(name="60# Cream-Uncoated", defaults={'price': 0.01})
        PaperType.objects.get_or_create(name="60# White-uncoated", defaults={'price': 0.01})
        PaperType.objects.get_or_create(name="70# White-Uncoated", defaults={'price': 0.02})
        PaperType.objects.get_or_create(name="80# White-Coated", defaults={'price': 0.03})

        # Spine
        Spine.objects.get_or_create(name="Round", defaults={'price': 5.00})
        Spine.objects.get_or_create(name="Flat", defaults={'price': 0.00})

        # Exterior Color
        ExteriorColor.objects.get_or_create(name="Black", defaults={'price': 5.00})
        ExteriorColor.objects.get_or_create(name="Brown", defaults={'price': 3.00})
        ExteriorColor.objects.get_or_create(name="Maroon", defaults={'price': 5.00})
        ExteriorColor.objects.get_or_create(name="Dark Blue", defaults={'price': 5.00})

        # Foil Stamping
        FoilStamping.objects.get_or_create(name="Golden", defaults={'price': 10.00})
        FoilStamping.objects.get_or_create(name="Silver", defaults={'price': 15.00})

        # Screen Stamping
        ScreenStamping.objects.get_or_create(name="Golden", defaults={'price': 10.00})
        ScreenStamping.objects.get_or_create(name="Silver", defaults={'price': 15.00})

        # Corner Protector
        CornerProtector.objects.get_or_create(name="Gold Sharp Corner", defaults={'price': 4.00})
        CornerProtector.objects.get_or_create(name="Gold Round Corner", defaults={'price': 4.00})
        CornerProtector.objects.get_or_create(name="Vintage Designs Corner", defaults={'price': 6.00})

        # Trim Sizes
        TrimSize.objects.get_or_create(name="A4", defaults={'price': 0.00})
        TrimSize.objects.get_or_create(name="Comic Book", defaults={'price': 0.00})
        TrimSize.objects.get_or_create(name="US Letter", defaults={'price': 0.00})

        self.stdout.write(self.style.SUCCESS('✅ Pricing data seeded successfully!'))
