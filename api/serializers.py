from rest_framework import serializers
from remind.models import Deadline, Case
from drf_writable_nested import WritableNestedModelSerializer


class DeadlineSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    deadline_name = serializers.CharField()
    defendant = serializers.CharField()
    case_number = serializers.CharField()
    judge = serializers.CharField()
    defense_attorney = serializers.CharField()

    class Meta:
        model = Deadline
        read_only_fields = (
            'deadline_name',
            'defendant',
            'case_number',
            'judge',
            'defense_attorney',
        )
        fields = '__all__'

    def get_type(self, obj):
        the_type = obj.get_type_display()
        return the_type.replace(' ', '-').lower()

    def get_status(self, obj):
        status = obj.get_status_display()
        return status.replace(' ', '-').lower()


class CaseSerializer(WritableNestedModelSerializer):
    deadline_set = DeadlineSerializer(many=True)

    class Meta:
        model = Case
        fields = '__all__'
