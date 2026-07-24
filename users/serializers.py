from django.contrib.auth import get_user_model
from rest_framework import serializers
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth import authenticate





User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
    )

    password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
        min_length=8,
    )

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "phone_number",
            "password",
            "confirm_password",
        )
    
    def validate_email(self, value):
        """
        Ensure email is unique.
        """
        email = value.lower()

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "An account with this email already exists."
            )

        return email
    
    def validate_phone_number(self, value):
        try:
            phone_number = phonenumbers.parse(value, "IN")

            if not phonenumbers.is_valid_number(phone_number):
                raise serializers.ValidationError(
                    "Enter a valid phone number."
                )

            formatted_number = phonenumbers.format_number(
                phone_number,
                phonenumbers.PhoneNumberFormat.E164
            )

            if User.objects.filter(phone_number=formatted_number).exists():
                raise serializers.ValidationError(
                    "Phone number is already registered."
                )

            return formatted_number

        except NumberParseException:
            raise serializers.ValidationError(
                "Invalid phone number format."
            )
        
    def validate_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)

        return value

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError({
                "confirm_password": "Passwords do not match."
            })

        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")

        user = User.objects.create_user(**validated_data)

        return user
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            email=email,
            password=password,
        )

        if user is None:
            raise serializers.ValidationError(
                "Invalid email or password."
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "User account is inactive."
            )

        attrs["user"] = user
        return attrs

