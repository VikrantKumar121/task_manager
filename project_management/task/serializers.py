from rest_framework_mongoengine import serializers as mongoserializers
from rest_framework import serializers
from .models import Task, SubTask

class SubTaskSerializer(mongoserializers.DocumentSerializer):
    # id = serializers.CharField(read_only=False)

    class Meta:
        model = SubTask
        fields = '__all__'

class TaskSerializer(mongoserializers.DocumentSerializer):
    # id = serializers.CharField(read_only=False)

    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        parent_task_id = validated_data["parent_task"]
        Task_ID = Task.objects.create(**validated_data)
        if parent_task_id is not None :
            sub_task_ID = SubTask.objects.create(task = Task_ID, task_parent = parent_task_id, sub_task = [])
        else:
            sub_task_ID = SubTask.objects.create(task = Task_ID, sub_task = [])
        return Task_ID

class GetSubTaskSerializer(mongoserializers.DocumentSerializer):
    # id = serializers.CharField(read_only=False)
    task_name=serializers.ReadOnlyField(source='task.name')
    # task_parent_name = None
    task_parent_name=serializers.ReadOnlyField(source='task_parent.name')
    class Meta:
        model = SubTask
        fields = ('id','task','created_on','modified_on','task_parent','sub_task','task_name','task_parent_name')

class GetTaskSerializer(mongoserializers.DocumentSerializer):
    # id = serializers.CharField(read_only=False)
    project_name=serializers.ReadOnlyField(source='project.name')
    assignee_name=serializers.ReadOnlyField(source='assignee.name')
    reporter_name=serializers.ReadOnlyField(source='reporter.name')
    parent_task_name=serializers.ReadOnlyField(source='parent_task.name')

    class Meta:
        model = Task
        fields = ('id','name','description','start_date','end_date','phase','project','assignee','reporter','comments','created_on','modified_on','parent_task','project_name','assignee_name','reporter_name','parent_task_name')
