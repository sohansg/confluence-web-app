from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=validated_data['username']
        )
        return user

# ✅ Add this below to allow listing users
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']
# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField()
#
#     def validate(self, data):
#         user = authenticate(email=data['email'], password=data['password'])
#         if not user:
#             raise serializers.ValidationError("Invalid credentials")
#         return {'user': user}
