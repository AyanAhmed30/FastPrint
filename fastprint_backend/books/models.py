from django.db import models
from django.conf import settings

class Book(models.Model):
    STATUS_CHOICES = [("Draft", "Draft"), ("Submitted", "Submitted"), ("Approved", "Approved")]
    ACCOUNT_CHOICES = [("individual", "Individual"), ("enterprise", "Enterprise")]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    language = models.CharField(max_length=50)
    trim_size = models.CharField(max_length=50)
    page_count = models.PositiveIntegerField()
    binding_type = models.CharField(max_length=100)
    interior_type = models.CharField(max_length=100)
    paper_type = models.CharField(max_length=100)
    cover_finish = models.CharField(max_length=100)
    interior_file = models.TextField()
    cover_file = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Draft")

    # New fields
    account_type = models.CharField(max_length=20, choices=ACCOUNT_CHOICES, default='individual')
    shipping_state = models.CharField(max_length=2)
    resale_cert_uploaded = models.BooleanField(default=False)

    price_per_unit = models.FloatField(default=0)
    tax_rate = models.FloatField(default=0)
    tax_amount = models.FloatField(default=0)
    total_price = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
