from rest_framework import serializers
from .models import *
from . import utils


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'contact', 'avatar', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        instance.email = validated_data.get('email').strip().lower()
        instance.is_active = True
        if password:
            instance.set_password(password)
        instance.save()
        # utils.send_phone_verification_code(instance)
        return instance

