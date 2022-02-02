from django.contrib.auth.models import User
from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True, 'required': True}}


class UserMiniSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'status', 'size', 'quantity',
                  'toppings', 'address', 'phone_no', 'customer')
