from rest_framework import permissions
import uuid
import jwt
from user.models import BlackListedToken
from passlib.context import CryptContext
from mongo_auth.db import jwt_secret, auth_collection
from mongo_auth.db import database

def login_status(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    data = jwt.decode(token, jwt_secret, algorithms=['HS256'])
    user_obj = None
    flag = False
    # print(data)
    user_filter = database[auth_collection].find({"email": data["id"]}, {"password": 0})
    if user_filter.count():
        flag = True
        user_obj = list(user_filter)[0]
    return flag, user_obj

class AuthenticatedOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            flag, user_obj = login_status(request)
            request.user = None
            if flag:
                request.user = user_obj
                return True
            else:
                return False
        except Exception as e:
            return False

class IsTokenValid(permissions.BasePermission):

    def has_permission(self, request, view):
        user_id = request.user["_id"]
        # print(user_id)
        is_allowed_user = True
        token = request.META.get('HTTP_AUTHORIZATION')

        try:
            is_blacklisted = BlackListedToken.objects.get(user=user_id, token=token)
            if is_blacklisted:
                is_allowed_user = False
        except BlackListedToken.DoesNotExist:
            is_allowed_user = True
        return is_allowed_user
