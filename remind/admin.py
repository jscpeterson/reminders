from django.contrib import admin

from cases.models import Case, Motion
from remind.models import Deadline

admin.site.register(Case)
admin.site.register(Deadline)
admin.site.register(Motion)
