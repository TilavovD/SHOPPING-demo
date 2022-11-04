from rest_framework.serializers import ModelSerializer

from users.models import User


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "phone_number", )
