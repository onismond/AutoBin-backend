import requests
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


class HomeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user = User.objects.get(id=1)
        # bins = Bin.objects.all()
        bins = user.bin.all()
        pickup_amount = 0
        uncleared_pickups = []
        total_paid = 0
        for bin in bins:
            for pickup in bin.pickups.all():
                if pickup.cleared:
                    pickup_amount += pickup.amount
                else:
                    uncleared_pickups.append(pickup)
            for transaction in bin.transactions.all():
                total_paid += transaction.amount
        bin_serializer = BinSerializer(bins, many=True)
        pickups_serializer = PickupSerializer(uncleared_pickups, many=True)
        transaction_serializer = TransactionSerializer(user.transactions.filter(cleared=True)[5], many=True)
        return Response({
            'due_amount': (pickup_amount - total_paid),
            'bins': bin_serializer.data,
            'pickups': pickups_serializer.data,
            'transactions': transaction_serializer.data,
            'detail': 'Data retrieved successfully',
        })


class PayNowView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        contact = request.data['contact']
        amount = request.data['amount']
        user = User.objects.get(id=1)
        # bins = Bin.objects.all()
        bins = user.bin.all()
        transaction = user.transactions.create(amount=amount, contact=contact, cleared=False)
        transaction.save()
        pay_success = utils.send_pay_request(transaction, amount, user.name, user.email, contact)
        if not pay_success:
            return Response({'error': 'Error processing payment request'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'detail': 'Payment request sent successfully',
        })


class ConfirmPayView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user = User.objects.get(id=1)
        id = request.GET.get('id')
        invoice = request.GET.get('invoice')
        try:
            transaction = Transaction.objects.get(id=id)
        except Transaction.DoesNotExist:
            return Response({'error': 'Transaction not found'}, status=status.HTTP_400_BAD_REQUEST)
        if (not (transaction in user.transactions.all())) and (transaction.serial_number != invoice):
            return Response({'error': 'Transaction not found'}, status=status.HTTP_400_BAD_REQUEST)
        pay_success = utils.check_pay_success(transaction)
        if pay_success:
            transaction.cleared = True
            transaction.save()
        else:
            return Response({'error': 'Payment not completed'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'detail': 'Payment confirmed successfully'
        })


class CancelPayView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user = User.objects.get(id=1)
        id = request.GET.get('id')
        invoice = request.GET.get('invoice')
        try:
            transaction = Transaction.objects.get(id=id)
        except Transaction.DoesNotExist:
            return Response({'error': 'Transaction not found'}, status=status.HTTP_400_BAD_REQUEST)
        if (not (transaction in user.transactions.all())) and (transaction.serial_number != invoice):
            return Response({'error': 'Transaction not found'}, status=status.HTTP_400_BAD_REQUEST)
        transaction.delete()
        return Response({
            'detail': 'Payment canceled successfully'
        })


class BinsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # user = User.objects.get(id=1)
        # bins = user.bins.all().order_by('-id')
        bins = Bin.objects.all().order_by('-id')
        serializer = BinSerializer(bins, many=True)
        return Response({
            'data': serializer.data,
            'detail': 'Bins retrieved successfully',
        })


class TransactionsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user = User.objects.get(id=1)
        serializer = TransactionSerializer(user.transactions.filter(cleared=True), many=True)
        return Response({
            'data': serializer.data,
            'detail': 'Transactions retrieved successfully',
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
        user = User.objects.get(id=1)
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
            bin = Bin(serial_number=qr_value, name=bin_name, owner=user, color=bin_color, latitude=latitude, longitude=longitude)
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


class UserPickupsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user = User.objects.get(pk=1)
        bins = user.bin.all()
        pickups = []
        for bin in bins:
            for pickup in bin.pickups.all():
                pickups.append(pickup)
        serializer = PickupSerializer(pickups, many=True)
        return Response({
            'data': serializer.data,
            'detail': 'Data retrieved successfully',
        })


class UpdateBinView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        bin_id = request.GET['id']
        bin_level = int(request.GET['level'])
        bin_weight = int(request.GET['weight'])
        try:
            bin = Bin.objects.get(pk=bin_id)
            if (bin_level > bin.bin_height):
                return Response({'error': 'Invalid bin level'}, status=status.HTTP_400_BAD_REQUEST)
            bin.current_level = bin_level
            bin.current_weight = bin_weight
            if (bin.bin_height - int(bin_level)) / bin.bin_height <= 0.25:
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


class MarkPickupClearedView(APIView):
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
        bin.current_level = bin.bin_height
        bin.current_weight = 0
        bin.save()
        return Response({
            'detail': 'Pickup successfully marked as cleared',
        })


class RouteView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        start = request.data['start']
        end = request.data['end']
        osrm_url = f"https://router.project-osrm.org/route/v1/driving/{start};{end}?overview=full&geometries=polyline"
        response = requests.get(osrm_url)
        if response.status_code == 200:
            return Response(response.json())
        else:
            return Response({"error": "Failed to fetch route data"}, status=response.status_code)






