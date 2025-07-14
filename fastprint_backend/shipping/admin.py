from django.contrib import admin
from .models import ShippingAddress


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'first_name',
        'last_name',
        'company',
        'address',
        'apt_floor',
        'country',
        'state',
        'city',
        'postal_code',
        'phone_number',
        'created_at',
    )
    search_fields = (
        'first_name',
        'last_name',
        'city',
        'country',
        'user__username',
        'user__email',
        'postal_code',
        'phone_number',
    )
    list_filter = ('country', 'city', 'state', 'created_at')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
