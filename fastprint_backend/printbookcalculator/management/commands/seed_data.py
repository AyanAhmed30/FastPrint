from django.core.management.base import BaseCommand
from printbookcalculator.models import *

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Trim Sizes
        a4 = TrimSize.objects.get_or_create(name="A4")[0]
        novella = TrimSize.objects.get_or_create(name="Novella (5 x 8 in)")[0]

        # Interior Colors
        InteriorColor.objects.get_or_create(name="Standard Black & White", price_per_page=0.01)
        InteriorColor.objects.get_or_create(name="Premium Black & White", price_per_page=0.02)
        InteriorColor.objects.get_or_create(name="Standard Color", price_per_page=0.03)
        InteriorColor.objects.get_or_create(name="Premium Color", price_per_page=0.10)

        # Paper Types
        PaperType.objects.get_or_create(name="60# Cream-Uncoated", price_per_page=0.01)
        PaperType.objects.get_or_create(name="80# White-Coated", price_per_page=0.02)

        # Cover Finishes
        CoverFinish.objects.get_or_create(name="Gloss", price=0.20)
        CoverFinish.objects.get_or_create(name="Matte", price=0.20)

        # Binding Types for A4
        BindingType.objects.get_or_create(name="Perfect Bound", price=2.00, trim_size=a4, min_pages=32, max_pages=470)
        BindingType.objects.get_or_create(name="Saddle Stitch", price=3.82, trim_size=a4, min_pages=4, max_pages=48)
        BindingType.objects.get_or_create(name="Case Wrap", price=9.75, trim_size=a4, min_pages=24, max_pages=470)
        BindingType.objects.get_or_create(name="Coil Bound", price=6.18, trim_size=a4, min_pages=3, max_pages=470)
        BindingType.objects.get_or_create(name="Linen Wrap", price=13.80, trim_size=a4, min_pages=32, max_pages=470)

        # ✅ Binding Types for Novella
        BindingType.objects.get_or_create(name="Perfect Bound", price=1.90, trim_size=novella, min_pages=32, max_pages=470)
        BindingType.objects.get_or_create(name="Saddle Stitch", price=3.60, trim_size=novella, min_pages=4, max_pages=48)
        BindingType.objects.get_or_create(name="Case Wrap", price=9.00, trim_size=novella, min_pages=24, max_pages=470)
        BindingType.objects.get_or_create(name="Coil Bound", price=6.00, trim_size=novella, min_pages=3, max_pages=470)
        BindingType.objects.get_or_create(name="Linen Wrap", price=13.00, trim_size=novella, min_pages=32, max_pages=470)

        self.stdout.write(self.style.SUCCESS("✅ Sample data for A4 and Novella seeded successfully!"))
