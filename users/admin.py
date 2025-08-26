from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'contact', 'role', 'is_active')
    list_display_links = ('id', 'name')
    fieldsets = (
        (None, {'fields': ('name', 'email', 'contact', 'role', 'collector_pickups')}),
        ('Advanced options', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',
                                         'date_joined', 'last_login', 'latitude', 'longitude', 'address_updated_at',
                                         'avatar')}),
    )
    search_fields = ('name', 'email', 'contact')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')


admin.site.register(User, UserAdmin)
