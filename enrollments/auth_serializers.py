from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from .models import Student

class LoginInputSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class UserMiniSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField(allow_null=True, required=False)
    groups = serializers.ListField(child=serializers.CharField())

class LoginResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserMiniSerializer()

class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)# pylint: disable=no-member
        token["username"] = user.username
        token["groups"] = list(user.groups.values_list("name", flat=True))
        return token

    def validate(self, attrs):
        data = super().validate(attrs) # pylint: disable=no-member
        user = self.user# pylint: disable=no-member
        data["user"] = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
        return data       