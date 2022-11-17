from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import authenticate

from users.models import User


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "phone_number", "gender", "birth_date", "city", "image")
        read_only_fields = ('phone_number', )


class UserRegisterSerializer(ModelSerializer):
    password = serializers.CharField(
        min_length=6, write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "first_name", "last_name", "password", "phone_number", "gender", "birth_date", "city", "image", "is_agree")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class SecretCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("phone_number", "secret_key")


class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """
    phone_number = serializers.CharField(
        label="Phone number",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take username and password from request
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        if phone_number and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                phone_number=phone_number, password=password)
            if user:
                if not user.is_verified:
                    msg = 'Access denied: phone_number is not verified.'
                    raise serializers.ValidationError(msg, code='authorization')
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong phone_number or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "phone_number" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs
