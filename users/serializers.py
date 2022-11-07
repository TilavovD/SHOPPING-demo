from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import User


class UserDetailSerializer(ModelSerializer):
    def validate(self, attrs):
        if User.objects.filter(phone_number=attrs.phone_number):
            raise serializers.ValidationError({"phone_number": "User with such phone number already exists!"})

    class Meta:
        model = User
        fields = ("first_name", "last_name", "phone_number", "gender", "birth_date", "city", "image", "is_agree")
