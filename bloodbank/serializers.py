from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import DonorProfile
from .models import PatientProfile,BloodStock

# =====================
# User Registration
# =====================
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )


# =====================
# User Login
# =====================
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid username or password")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")

        return {"user": user}


# =====================
# Donor Profile
# =====================


# serializers.py


class DonorProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)  # new field

    class Meta:
        model = DonorProfile
        fields = '__all__'
        read_only_fields = ['user', 'username'] 
class PatientProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)  # new field

    class Meta:
        model = PatientProfile
        fields = '__all__'
        read_only_fields = ['user', 'username']


# serializers.py
class BloodStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodStock
        fields = "__all__"
