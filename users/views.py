from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed, APIException
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, logout
from django.utils import timezone
from .serializers import *
from .models import *
from . import utils


class UserView(APIView):

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user, context={'request': request})
        return Response({
            'user': serializer.data,
        })


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data['email'].strip().lower()
        password = request.data['password']
        is_email = utils.is_email(email)
        if is_email:
            user = authenticate(request, email=email, password=password)
        else:
            return Response({'error': 'Email not valid'}, status=status.HTTP_401_UNAUTHORIZED)
        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        token = str(RefreshToken.for_user(user).access_token)
        serializer = UserSerializer(user, context={'request': request})
        return Response({
            'user': serializer.data,
            'token': token,
            'detail': 'Logged in successfully',
        })


class CollectorLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data['email'].strip().lower()
        password = request.data['password']
        is_email = utils.is_email(email)
        if is_email:
            user = authenticate(request, email=email, password=password)
        else:
            return Response({'error': 'Email not valid'}, status=status.HTTP_401_UNAUTHORIZED)
        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        if user.role != 'collector':
            return Response({'error': 'Only Collector accounts can sign in'}, status=status.HTTP_401_UNAUTHORIZED)
        token = RefreshToken.for_user(user).access_token
        return Response({
            'detail': 'Logged in successfully',
            'user': UserSerializer(user, context={'request': request}).data,
            'token': str(token),
        })


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data['email'].strip().lower()
        user = User.objects.filter(email=email).first()
        if user:
            if user.is_active:
                return Response({'error': 'Email already used. Please enter a different email'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # utils.send_phone_verification_code(user)  # user is yet to verify account
                return Response({
                    'success': True,
                    'detail': 'Account created successfully'
                })
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            # print(serializer.errors)
            return Response({'error': 'Please provide all necessary details'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'detail': 'Account created successfully'
        })


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        logout(request)
        return Response({
            'detail': 'Logged out successfully',
        })


class SendPhoneCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Please provide an email'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email.strip().lower())
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        utils.send_phone_verification_code(user)
        return Response({
            'detail': 'Verification code sent successfully',
        })


class VerifyPhoneCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', None)
        code = request.data.get('code', None)
        if not email:
            return Response({'error': 'Please provide an email'}, status=status.HTTP_400_BAD_REQUEST)
        if not code:
            return Response({'error': 'Please provide a code'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email.strip().lower())
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        verified = utils.verify_phone_code(user, code)
        if not verified:
            return Response({'error': 'The code you entered is invalid'}, status=status.HTTP_400_BAD_REQUEST)
        user.is_active = True
        user.phone_verification_code = ''
        user.save()
        return Response({
            'detail': 'Your phone number has been verified',
        })


class SendPasswordChangeCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', None)
        if not email:
            return Response({'error': 'Please provide an email'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email.strip().lower())
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        utils.send_password_change_verification_code(user)
        return Response({
            'detail': 'Verification code sent successfully',
        })


class VerifyPasswordChangeCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', None)
        code = request.data.get('code', None)
        if not email:
            return Response({'error': 'Please provide an email'}, status=status.HTTP_400_BAD_REQUEST)
        if not code:
            return Response({'error': 'Please provide a code'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email.strip().lower())
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        verified = utils.verify_password_change_code(user, code)
        if not verified:
            return Response({'error': 'The code you entered is invalid'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'detail': 'Code verified',
        })


class ChangePasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', None)
        code = request.data.get('code', None)
        password = request.data.get('password', None)
        if not email:
            return Response({'error': 'Please provide an email'}, status=status.HTTP_400_BAD_REQUEST)
        if not code:
            return Response({'error': 'Please provide a code'}, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return Response({'error': 'Please provide a password'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=request.data.get('email').strip().lower())
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        code = request.data.get('code')
        password = request.data.get('password')
        if user.password_change_verification_code == code:
            user.set_password(password)
            user.password_change_verification_code = ''
            user.save()
            return Response({
                'detail': 'Password changed successfully',
            })
        return Response({'error': 'Password reset code is invalid'}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAuthenticatedView(APIView):

    def post(self, request):
        old_password = request.data.get('old_password', None)
        new_password = request.data.get('new_password', None)
        if not (new_password and old_password):
            return Response({'error': 'Please provide new and old password'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(email=request.user.email, password=old_password)
        if user is None:
            return Response({'error': 'Old password is incorrect'}, status=status.HTTP_401_UNAUTHORIZED)
        user = request.user
        user.set_password(new_password)
        user.save()
        return Response({
            'detail': 'Password changed successfully',
        })


class EditProfileView(APIView):

    def post(self, request):
        name = request.data.get('name', None)
        user_name = request.data.get('user_name', None)
        contact = request.data.get('contact', None)
        user = request.user
        if name:
            user.name = name
        if user_name:
            user.username = user_name
        if contact:
            user.contact = contact
        user.save()
        return Response({
            'detail': 'Profile updated successfully',
        })







