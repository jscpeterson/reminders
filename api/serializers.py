from rest_framework import serializers

from remind.constants import EVENT_DEADLINES
from remind.models import Deadline, Case
from drf_writable_nested import WritableNestedModelSerializer
from remind.constants import FIRST_REMINDER_DAYS, SECOND_REMINDER_DAYS


class DeadlineSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    first_reminder_days = serializers.SerializerMethodField()
    second_reminder_days = serializers.SerializerMethodField()
    event = serializers.SerializerMethodField()

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

    def get_first_reminder_days(self, obj):
        return FIRST_REMINDER_DAYS[obj.type]

    def get_second_reminder_days(self, obj):
        return SECOND_REMINDER_DAYS[obj.type]

    def get_event(self, obj):
        return obj.type in EVENT_DEADLINES


class CaseSerializer(WritableNestedModelSerializer):
    deadline_set = DeadlineSerializer(many=True)

    class Meta:
        model = Case
        fields = '__all__'
