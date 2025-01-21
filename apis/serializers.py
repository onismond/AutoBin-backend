from rest_framework import serializers
from .models import *
from . import utils


class BinSerializer(serializers.ModelSerializer):
    current_level = serializers.SerializerMethodField()
    class Meta:
        model = Bin
        fields = ['id', 'name', 'serial_number', 'current_level', 'current_weight', 'updated_at']

    def get_current_level(self, bin):
        return f'{((bin.bin_height - bin.current_level) / bin.bin_height) * 100}'


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
        return obj.bin.first().current_level

    def get_latitude(self, obj):
        return obj.bin.first().latitude

    def get_longitude(self, obj):
        return obj.bin.first().longitude
