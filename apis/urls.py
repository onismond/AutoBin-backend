from django.urls import path
from .views import *

urlpatterns = [
    path('bins/', BinsView.as_view(), name='bins'),
    path('bin/detail/', BinDetailView.as_view(), name='bin_detail'),
    path('bin/add/', AddBinView.as_view(), name='add_bin'),
    path('bin/order-pickup/', OrderPickupView.as_view(), name='order_pickup'),

    # Autobin Device
    path('bin/update/', UpdateBinView.as_view(), name='update_bin'),

    # Collector
    path('collector/pickups/', CollectorPickupsView.as_view(), name='collector_pickups'),
    path('collector/pickup/mark-cleared/', MarkPickupClearedView.as_view(), name='mark_pickup_cleared'),
    path('route/', RouteView.as_view(), name='route'),

]
