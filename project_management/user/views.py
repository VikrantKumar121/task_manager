from django.shortcuts import render
from rest_framework_mongoengine.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from base.exception.error_message import DETAILS_NOT_FOUND
from base.exception.base import CustomNotFound
from .models import User, BlackListedToken
from .serializers import MyUserSerializer,UserLoginSerializer,GetUserSerializer
from django.http import JsonResponse
from django.contrib.auth import logout
# Create your views here.
from mongo_auth.permissions import AuthenticatedOnly


class UserViewSet(APIView):
    """"""
    # permission_classes = (AllowAny,)
    lookup_field = 'id'
    serializer_class = MyUserSerializer
    get_serializer_class = GetUserSerializer
    model_name = User

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            response = {
                'message': serializer.errors,
                'data': []
            }
            return Response(response, status = 422)

    def get_object(self, pk):
        try:
            return self.model_name.objects.get(pk=pk)
        except self.model_name.DoesNotExist:
            raise CustomNotFound(DETAILS_NOT_FOUND)

    def get(self, request, pk=0, format=None):
        org_id = request.user['organization']
        if pk==0:
            print(request.auth)
            seed = self.model_name.objects.filter(organization = org_id)
            serializer = self.get_serializer_class(seed, many=True)
            return Response(serializer.data)
        else:
            seed = self.get_object(pk)
            serializer = self.get_serializer_class(seed)
            return Response(serializer.data)

    def put(self, request, pk, format=None):
        seed = self.get_object(pk)
        serializer = self.serializer_class(seed, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            response = {
                'message': serializer.errors,
                'data': []
            }
            return Response(response, status = 422)

    def patch(self, request, pk, format=None):
        seed = self.get_object(pk)
        serializer = self.serializer_class(seed, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            response = {
                'message': serializer.errors,
                'data': []
            }
            return Response(response, status = 422)

    def delete(self, request, pk, format=None):
        seed = self.get_object(pk)
        seed.delete()
        response={"message":"Delete Successfully"}
        return Response(response)


from django.contrib.auth import authenticate, login as do_login, logout as do_logout
from .custom_auth import authenticate
from rest_framework.permissions import AllowAny

class SignUpViewSet(APIView):
    """"""
    permission_classes = (AllowAny,)
    lookup_field = 'id'
    serializer_class = MyUserSerializer
    model_name = User
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            response = {
                'message': serializer.errors,
                'data': []
            }
            return Response(response, status = 422)

class LoginViewSet(APIView):
    """"""
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            response = {
                'message': 'User logged in  successfully',
                'data': {
                    'token': serializer.data['token'],
                    'userid':serializer.data['userid']
                }     }
        else:
            response = {
                'message': serializer.errors,
                'data': []
            }
        return Response(response)

class LogoutViewSet(APIView):
    """"""
    # permission_classes = (AllowAny,)

    def get(self,request):
        user_id = request.user["_id"]
        token=request.META.get('HTTP_AUTHORIZATION')
        BlackListedToken.objects.create(user=user_id, token=token)
        logout(request)
        response = {
            'message': 'User logged out  successfully',
            }

        return Response(response)
