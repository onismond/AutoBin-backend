from rest_framework import serializers
from .models import *
from . import utils


class BinSerializer(serializers.ModelSerializer):
    current_level = serializers.SerializerMethodField()
    updated_at = serializers.DateTimeField(format="%d %b, %Y %I:%M%p", read_only=True)
    pending_pickup = serializers.SerializerMethodField()

    class Meta:
        model = Bin
        fields = ['id', 'name', 'serial_number', 'current_level', 'current_weight', 'updated_at', 'pending_pickup']

    def get_current_level(self, bin):
        return int(((bin.bin_height - bin.current_level) / bin.bin_height) * 100)

    def get_pending_pickup(self, bin):
        if bin.pickups.filter(cleared=False).exists():
            return True
        return False


class PickupSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%d %b, %Y %I:%M%p", read_only=True)
    bin_name = serializers.SerializerMethodField()

    class Meta:
        model = Pickup
        fields = ['id', 'bin_name', 'amount', 'date', 'cleared']

    def get_bin_name(self, pickup):
        return pickup.bin.first().name


class TransactionSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%d %b, %Y %I:%M%p", read_only=True)

    class Meta:
        model = Pickup
        fields = ['id', 'date', 'amount']



class CollectorPickupSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    user_contact = serializers.SerializerMethodField()
    current_level = serializers.SerializerMethodField()
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    class Meta:
        model = Pickup
        fields = ['id', 'user_name', 'user_contact', 'current_level', 'latitude', 'longitude']

    def get_user_name(self, obj):
        return obj.bin.first().owner.name

    def get_user_contact(self, obj):
        return obj.bin.first().owner.contact

    def get_current_level(self, obj):
        bin = obj.bin.first()
        return int(((bin.bin_height - bin.current_level) / bin.bin_height) * 100)

    def get_latitude(self, obj):
        return obj.bin.first().latitude

    def get_longitude(self, obj):
        return obj.bin.first().longitude
