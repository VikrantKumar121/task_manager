from rest_framework_mongoengine import serializers as mongoserializers
from rest_framework import serializers
from .models import User
from organization.models import Organization

# class UserSerializer(mongoserializers.DocumentSerializer):
#     """"""
#     class Meta:
#         model = User
#         fields = '__all__'

class MyUserSerializer(mongoserializers.DocumentSerializer):
    """"""
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):

        if "organization" not in validated_data.keys():
            validated_data["organization"] = None

        if validated_data["organization"] is None:
            user_domain = validated_data["email"].split("@")[-1]
            try:
                validated_data["organization"] = Organization.objects.get(domain = user_domain)["id"]
            except Organization.DoesNotExist:
                validated_data["organization"] = None
            user = User.objects.create(**validated_data)
            return user

class GetUserSerializer(mongoserializers.DocumentSerializer):
    """"""
    organization_name=serializers.ReadOnlyField(source='organization.name')

    class Meta:
        model = User
        fields = ('id','email','first_name','last_name','phone_number','recovery_phone','is_active','is_staff','is_superuser','organization','organization_name')

from .custom_auth import authenticate
from rest_framework_jwt.settings import api_settings
from calendar import timegm
from datetime import datetime
from rest_framework.decorators import api_view
from mongo_auth.utils import create_unique_object_id, pwd_context
from mongo_auth.db import database, auth_collection, fields, jwt_life, jwt_secret, secondary_username_field
import jwt
import datetime
from mongo_auth import messages
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    userid = serializers.CharField(max_length=50, read_only=True)
    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        try:
            # user = database[auth_collection].find_one({"email": email}, {"_id": 0})
            token = jwt.encode({'id':user['email'],
                                    'exp': datetime.datetime.now() + datetime.timedelta(
                                        days=jwt_life)},
                                   jwt_secret, algorithm='HS256').decode('utf-8')
        # update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        # token, created = Token.objects.get_or_create(user=user)
        return {
            'email': user.email,
            'token': token,
            'userid':user.id

        }
