from django.contrib import admin
from django.db.models.functions import TruncDate
from django.db.models import Count
from django.template.response import TemplateResponse
from datetime import date, timedelta
from .models import *


def custom_index(request):
    today = date.today()
    last_week = today - timedelta(days=6)
    qs = User.objects.filter(date_joined__date__gte=last_week)
    data = (qs.annotate(day=TruncDate('date_joined'))
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day'))
    labels = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in reversed(range(7))]
    chart_data = {d['day'].strftime('%Y-%m-%d'): d['count'] for d in data}
    counts = [chart_data.get(day, 0) for day in labels]

    context = admin.site.each_context(request)
    context.update({
        'app_list': admin.site.get_app_list(request),
        'labels': labels,
        'data': counts,
        'total_pickups': Pickup.objects.count(),
        'total_bins': Bin.objects.count(),
        'total_drivers': User.objects.filter(role='collector').count(),
        'total_customers': User.objects.filter(role='user').count(),
    })
    return TemplateResponse(request, 'admin/index.html', context)

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


admin.site.index = custom_index
admin.site.register(Bin, BinAdmin)
admin.site.register(Pickup, PickupAdmin)
admin.site.register(Transaction, TransactionAdmin)

