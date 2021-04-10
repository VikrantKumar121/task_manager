from django.shortcuts import render
from rest_framework_mongoengine.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from base.exception.error_message import DETAILS_NOT_FOUND
from base.exception.base import CustomNotFound
from .models import Project
from .serializers import ProjectSerializer, GetProjectSerializer
# Create your views here.

class ProjectViewSet(APIView):
    """"""
    lookup_field = 'id'
    serializer_class = ProjectSerializer
    get_serializer_class = GetProjectSerializer
    model_name = Project

    def post(self, request, format=None):
        org_id = request.user['organization']

        data_with_org = request.data
        data_with_org["organization"] = org_id
        serializer = self.serializer_class(data=data_with_org)
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
