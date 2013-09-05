from django.contrib import admin

from redcaptainhook.apps.workflow.models import Trigger, Project, Process

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'site', 'redcap_pid', 'hash', 'active',
        'trigger_url')

admin.site.register(Trigger)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Process)