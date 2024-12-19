from rest_framework import serializers
from .models import *
from . import utils


class BinSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bin
        fields = ['id', 'name', 'serial_number', 'current_level', 'current_weight']


