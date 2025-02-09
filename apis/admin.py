from django.contrib import admin
from .models import *


class BinAdmin(admin.ModelAdmin):
    list_display = ['id', 'serial_number', 'name', 'current_level', 'current_weight', 'bin_height']
    list_display_links = ['id', 'serial_number']
    list_filter = ['bin_height']


class PickupAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'amount', 'cleared']
    list_filter = ['date', 'cleared']
    readonly_fields = ['date']


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'amount']
    list_filter = ['date']
    readonly_fields = ['date']


admin.site.register(Bin, BinAdmin)
admin.site.register(Pickup, PickupAdmin)
admin.site.register(Transaction, TransactionAdmin)

