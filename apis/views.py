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


class BinDetailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        bin_id = request.data.get('bin_id')
        try:
            bin = Bin.objects.get(id=bin_id)
        except Bin.DoesNotExist:
            return Response({'error': 'Invalid bin id'}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': 'An error occurred'}, status=status.HTTP_404_NOT_FOUND)
        return Response({
            'id': bin.id,
            'name': bin.name,
            'current_level': int(((bin.bin_height - bin.current_level) / bin.bin_height) * 100),
            'current_weight': bin.current_weight,
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
            bin = Bin(serial_number=qr_value, name=bin_name, owner=User.objects.get(pk=1), color=bin_color, latitude=latitude, longitude=longitude)
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
            bin.current_level = bin_level
            bin.current_weight = bin_weight
            if (bin.bin_height - bin_level) / bin.bin_height <= 0.25:
                if not bin.pickups.filter(cleared=False).exists():
                    bin.pickups.create(amount=10)
            bin.save()
        except Bin.DoesNotExist:
            return Response({'error': 'Invalid bin id'}, status=status.HTTP_404_NOT_FOUND)
        return Response({
            'detail': 'Bin updated successfully',
        })


class CollectorPickupsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        pickups = Pickup.objects.filter(cleared=False).all()
        serializer = CollectorPickupSerializer(pickups, many=True)
        return Response({
            'data': serializer.data,
            'detail': 'Data retrieved successfully',
        })


class MarkPickupCleared(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serial_number = request.data['serial_number']
        try:
            bin = Bin.objects.get(serial_number=serial_number)
        except Bin.DoesNotExist:
            return Response({'error': 'Bin not found'}, status=status.HTTP_404_NOT_FOUND)
        if bin.pickups.filter(cleared=False).exists():
            for pickup in bin.pickups.filter(cleared=False).all():
                pickup.cleared = True
                pickup.save()
        # bin.current_level = 0
        # bin.current_weight = 0
        bin.save()
        return Response({
            'detail': 'Pickup successfully marked as cleared',
        })







