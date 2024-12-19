from django.contrib import admin
from .models import *


class PickupAdmin(admin.ModelAdmin):
    fields = ['bin', 'date']
    list_display = ['bin', 'date']
    readonly_fields = ['date']


admin.site.register(Bin)
admin.site.register(Pickup, PickupAdmin)

