from rest_framework import serializers
from remind.models import Deadline, Case


class DeadlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deadline
        fields = '__all__'


class CaseSerializer(serializers.ModelSerializer):
    deadline_set = DeadlineSerializer(many=True)

    class Meta:
        model = Case
        fields = '__all__'
