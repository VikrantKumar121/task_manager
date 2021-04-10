from rest_framework_mongoengine import serializers as mongoserializers
from rest_framework import serializers
from .models import Organization

class OrganizationSerializer(mongoserializers.DocumentSerializer):
    # id = serializers.CharField(read_only=False)

    class Meta:
        model = Organization
        fields = '__all__'
