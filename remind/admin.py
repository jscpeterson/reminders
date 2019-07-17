from django.contrib import admin

from .models import Case, Deadline, Motion

admin.site.register(Case)
admin.site.register(Deadline)
admin.site.register(Motion)
