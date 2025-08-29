from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

urlpatterns = [
    path('details/', UserView.as_view(), name='user_details'),
    path('login/', LoginView.as_view(), name='login'),
    path('collector/login/', CollectorLoginView.as_view(), name='delivery_login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('send-phone-code/', SendPhoneCodeView.as_view(), name='send_phone_code'),
    path('verify-phone-code/', VerifyPhoneCodeView.as_view(), name='verify_phone_code'),
    path('send-password-change-code/', SendPasswordChangeCodeView.as_view(), name='send_password_change_code'),
    path('verify-password-change-code/', VerifyPasswordChangeCodeView.as_view(), name='verify_password_change_code'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('change-password/authenticated/', ChangePasswordAuthenticatedView.as_view(), name='change_password_authenticated'),
    path('profile/edit/', EditProfileView.as_view(), name='edit_profile'),
    path('collector/update-location/', UpdateCollectorLocation.as_view(), name='update_collector_location'),

]
