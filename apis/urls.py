from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

urlpatterns = [
    path('bins/', BinsView.as_view(), name='bins'),
    path('bin/order-pickup/', OrderPickupView.as_view(), name='order_pickup'),
    path('bin/update/', UpdateBinView.as_view(), name='update_bin'),

]
