from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class UserSerializer1(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username','email')

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = User
        fields = ('id', 'username', 'password','email')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self,validated_data):
        user=User.objects.create_user(**validated_data)
        return user


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'status', 'size','quantity','flavour')
