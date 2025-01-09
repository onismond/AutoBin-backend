from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed, APIException
from rest_framework.permissions import AllowAny
from .serializers import *
from .models import *
from . import utils


class BinsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        bins = Bin.objects.all()
        serializer = BinSerializer(bins, many=True)
        return Response({
            'data': serializer.data,
            'detail': 'Data retrieved successfully',
        })


class AddBinView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        qr_value = request.data['qr_value']
        bin_name = request.data['bin_name']
        bin_color = request.data['bin_color']
        latitude = request.data['latitude']
        longitude = request.data['longitude']
        bin = Bin.objects.filter(serial_number=qr_value).first()
        if bin:
            bin.name = bin_name
            bin.color = bin_color
            bin.latitude = float(latitude)
            bin.longitude = float(longitude)
            bin.save()
        else:
            bin = Bin(serial_number=qr_value, name=bin_name, color=bin_color, latitude=latitude, longitude=longitude)
            bin.save()
        return Response({
            'detail': 'Bin added successfully',
        })


class OrderPickupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        bin_id = request.data['bin_id']
        try:
            bin = Bin.objects.get(pk=bin_id)
            if not bin.pickups.filter(cleared=False).exists():
                bin.pickups.create(amount=10)
                bin.save()
        except Bin.DoesNotExist:
            return Response({'error': 'Invalid bin id'}, status=status.HTTP_404_NOT_FOUND)
        return Response({
            'detail': 'Pickup ordered successfully',
        })


class UpdateBinView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        bin_id = request.GET['id']
        bin_level = request.GET['level']
        bin_weight = request.GET['weight']
        try:
            bin = Bin.objects.get(pk=bin_id)
            if bin_level:
                bin.current_level = bin_level
            if bin_weight:
                bin.current_weight = bin_weight
            bin.save()
        except Bin.DoesNotExist:
            return Response({'error': 'Invalid bin id'}, status=status.HTTP_404_NOT_FOUND)
        return Response({
            'detail': 'Bin updated successfully',
        })


