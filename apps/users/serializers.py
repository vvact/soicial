from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import EmailValidator

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            EmailValidator(message="Enter a valid email address.")
        ]
    )
    password = serializers.CharField(
        write_only=True,
        min_length=4, 
        error_messages={"min_length": "Password must be at least 4 characters long."}
    )

    class Meta:
        model = User
        fields = ["id", "email", "password"]

    def validate_email(self, value):
        """Custom email validation"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        
        if not value.endswith("@gmail.com"):
            raise serializers.ValidationError("Only Gmail addresses are allowed.")
        
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"]
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
