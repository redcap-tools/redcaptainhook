from django.contrib import admin

from redcaptainhook.apps.workflow.models import Trigger, Project, Process


admin.site.register(Trigger)
admin.site.register(Project)
admin.site.register(Process)