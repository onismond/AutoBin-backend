from django.urls import path
from .views import *

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('bins/', BinsView.as_view(), name='bins'),
    path('bin/detail/', BinDetailView.as_view(), name='bin_detail'),
    path('bin/add/', AddBinView.as_view(), name='add_bin'),
    path('bin/order-pickup/', OrderPickupView.as_view(), name='order_pickup'),
    path('user/pickups/', UserPickupsView.as_view(), name='user_pickups'),
    path('user/transactions/', TransactionsView.as_view(), name='transactions'),
    path('user/transactions/amount-due/', AmountDueView.as_view(), name='amount_due'),
    path('user/transactions/pay-now/', PayNowView.as_view(), name='pay_now'),
    path('transaction/confirm-pay/', ConfirmPayView.as_view(), name='confirm_pay'),
    path('transaction/cancel-pay/', CancelPayView.as_view(), name='cancel_pay'),

    # Autobin Device
    path('bin/update/', UpdateBinView.as_view(), name='update_bin'),

    # Collector
    path('collector/pickups/', CollectorPickupsView.as_view(), name='collector_pickups'),
    path('collector/pickup/mark-cleared/', MarkPickupClearedView.as_view(), name='mark_pickup_cleared'),
    path('route/', RouteView.as_view(), name='route'),

]
