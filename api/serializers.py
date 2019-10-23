from rest_framework import serializers

from remind.constants import EVENT_DEADLINES
from cases.models import Case
from remind.models import Deadline
from drf_writable_nested import WritableNestedModelSerializer
from remind.constants import FIRST_REMINDER_DAYS, SECOND_REMINDER_DAYS
from users.models import CustomUser


class DeadlineSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    first_reminder_days = serializers.SerializerMethodField()
    second_reminder_days = serializers.SerializerMethodField()
    event = serializers.SerializerMethodField()
    prosecutor = serializers.SerializerMethodField()

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

    def get_prosecutor(self, obj):
        return str(obj.case.prosecutor)


class CaseSerializer(WritableNestedModelSerializer):
    deadline_set = DeadlineSerializer(many=True)
    defendant = serializers.SerializerMethodField()
    judge = serializers.SerializerMethodField()
    defense_attorney = serializers.SerializerMethodField()
    prosecutor = serializers.SerializerMethodField()
    secretary = serializers.SerializerMethodField()
    paralegal = serializers.SerializerMethodField()
    victim_advocate = serializers.SerializerMethodField()

    class Meta:
        model = Case
        fields = '__all__'

    def get_defendant(self, obj):
        return str(obj.defendant)

    def get_judge(self, obj):
        return str(obj.judge)

    def get_defense_attorney(self, obj):
        return str(obj.defense_attorney)

    def get_prosecutor(self, obj):
        return str(obj.prosecutor)

    def get_secretary(self, obj):
        return str(obj.secretary)

    def get_paralegal(self, obj):
        return str(obj.paralegal)

    def get_victim_advocate(self, obj):
        return str(obj.victim_advocate)


class UserSerializer(WritableNestedModelSerializer):

    class Meta:
        model = CustomUser
        fields = '__all__'
