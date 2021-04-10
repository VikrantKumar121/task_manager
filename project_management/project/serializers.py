from rest_framework_mongoengine import serializers as mongoserializers
from rest_framework import serializers
from organization.models import Organization
from user.models import User
from .models import Project

class ProjectSerializer(mongoserializers.DocumentSerializer):
    """"""
    class Meta:
        model = Project
        fields = '__all__'

    # def create(self, validated_data):
    #     user_id = validated_data['maintainer']
    #     try:
    #         user_org = User.objects.get(pk = user_id)['organization']
    #         validated_data["organization"] = user_org
    #     except User.DoesNotExist:
    #         raise serializers.ValidationError('maintainer id not found')
    #     return Project.objects.create(**validated_data)

class GetProjectSerializer(mongoserializers.DocumentSerializer):
    """"""
    organization_name=serializers.ReadOnlyField(source='organization.name')
    maintainer_name=serializers.ReadOnlyField(source='maintainer.name')

    class Meta:
        model = Project
        fields = ('id','name','description','maintainer','organization','start_date','end_date','created_on','modified_on','time','organization_name','maintainer_name')
