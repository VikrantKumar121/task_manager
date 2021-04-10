from django.shortcuts import render
from rest_framework_mongoengine.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from base.exception.error_message import DETAILS_NOT_FOUND
from base.exception.base import CustomNotFound
from .models import Task, SubTask
from .serializers import TaskSerializer, SubTaskSerializer, GetSubTaskSerializer, GetTaskSerializer
from user.models import User
from .tasks import send_mail_task
# Create your views here.

class TaskViewSet(APIView):
    """"""
    lookup_field = 'id'
    serializer_class = TaskSerializer
    get_serializer_class = GetTaskSerializer
    sub_task_serializer_class = SubTaskSerializer
    model_name = Task
    sub_task_model_name = SubTask
    # queryset = Task.objects.all()

    # def get_quryset(self):
    #     return model_name.objects.all()

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            ##########MAIL##########
            assignee = serializer.data["assignee"]
            user = User.objects.get(pk = assignee)
            actor_name = user.name()
            recipient_list = [user.email, ]
            send_mail_task.delay( actor_name, recipient_list )
            ##########MAIL##########
            response = {"data": serializer.data}
            task_id = response["data"]["id"]
            parent_task_id = response["data"]["parent_task"]

            sub_task_data = {
                "task": parent_task_id,
            }
            if parent_task_id :
                sub_task_seed = self.get_sub_task(parent_task_id)

                sub_task_data["sub_task"] = [task_object["id"] for task_object in sub_task_seed["sub_task"]]
                sub_task_data["sub_task"].append(task_id)

                sub_task_serializer = self.sub_task_serializer_class(sub_task_seed, data=sub_task_data, partial = True)
                if sub_task_serializer.is_valid():
                    sub_task_serializer.save()
                    response["sub_task_data"] = sub_task_serializer.data
                else:
                    response["sub_task_data"] = []
                    response['message'] = sub_task_serializer.errors
                    return Response(response, status = 422)

            return Response(response)
        else:
            response = {
                'message': serializer.errors,
                'data': []
            }
            return Response(response, status = 422)

    def get_sub_task(self, pk):
        try:
            return self.sub_task_model_name.objects.get(task=pk)
        except self.sub_task_model_name.DoesNotExist:
            raise CustomNotFound(DETAILS_NOT_FOUND)

    def get_object(self, pk):
        try:
            return self.model_name.objects.get(pk=pk)
        except self.model_name.DoesNotExist:
            raise CustomNotFound(DETAILS_NOT_FOUND)

    def get(self, request, pk=0, format=None):
        if pk==0:
            seed = self.model_name.objects.all()
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

class SubTaskViewSet(APIView):
    """"""
    lookup_field = 'id'
    serializer_class = SubTaskSerializer
    get_serializer_class = GetSubTaskSerializer
    model_name = SubTask
    # queryset = SubTask.objects.all()

    # def get_quryset(self):
    #     return model_name.objects.all()

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
            return self.model_name.objects.get(task=pk)
        except self.model_name.DoesNotExist:
            raise CustomNotFound(DETAILS_NOT_FOUND)

    def get(self, request, pk=0, format=None):
        if pk==0:
            seed = self.model_name.objects.all()
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

class ProjectTaskViewSet(APIView):
    """"""
    lookup_field = 'id'
    serializer_class = TaskSerializer
    get_serializer_class = GetTaskSerializer
    sub_task_serializer_class = SubTaskSerializer
    model_name = Task
    sub_task_model_name = SubTask

    # def get_sub_task(self, pk):
    #     try:
    #         return self.sub_task_model_name.objects.get(task=pk)
    #     except self.sub_task_model_name.DoesNotExist:
    #         raise CustomNotFound(DETAILS_NOT_FOUND)

    def get_object(self, pk):
        try:
            return self.model_name.objects.get(pk=pk)
        except self.model_name.DoesNotExist:
            raise CustomNotFound(DETAILS_NOT_FOUND)

    def get(self, request, pk=0, project_id = 0, format=None):
        if project_id == 0:
            if pk==0:
                seed = self.model_name.objects.all()
                serializer = self.get_serializer_class(seed, many=True)
                return Response(serializer.data)
            else:
                seed = self.get_object(pk)
                serializer = self.get_serializer_class(seed)
                return Response(serializer.data)
        else:
            if pk==0:
                seed = self.model_name.objects.filter(project = project_id)
                serializer = self.get_serializer_class(seed, many=True)
                return Response(serializer.data)
            else:
                seed = self.get_object(pk)
                serializer = self.get_serializer_class(seed)
                return Response(serializer.data)

class ProjectRootTaskViewSet(APIView):
    """"""
    lookup_field = 'id'
    serializer_class = TaskSerializer
    get_serializer_class = GetTaskSerializer
    sub_task_serializer_class = SubTaskSerializer
    model_name = Task
    sub_task_model_name = SubTask

    # def get_sub_task(self, pk):
    #     try:
    #         return self.sub_task_model_name.objects.get(task=pk)
    #     except self.sub_task_model_name.DoesNotExist:
    #         raise CustomNotFound(DETAILS_NOT_FOUND)

    def get_object(self, pk):
        try:
            return self.model_name.objects.get(pk=pk)
        except self.model_name.DoesNotExist:
            raise CustomNotFound(DETAILS_NOT_FOUND)

    def get(self, request, pk=0, project_id = 0, format=None):
        if project_id == 0:
            if pk==0:
                seed = self.model_name.objects.all()
                serializer = self.get_serializer_class(seed, many=True)
                return Response(serializer.data)
            else:
                seed = self.get_object(pk)
                serializer = self.get_serializer_class(seed)
                return Response(serializer.data)
        else:
            if pk==0:
                seed = self.model_name.objects.filter(project = project_id, parent_task = None)
                serializer = self.get_serializer_class(seed, many=True)
                return Response(serializer.data)
            else:
                seed = self.get_object(pk)
                serializer = self.get_serializer_class(seed)
                return Response(serializer.data)
