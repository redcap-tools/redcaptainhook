from django.contrib import admin

from redcaptainhook.apps.workflow.models import Trigger, Project, Process

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'redcap_pid','active', 'trigger_url')


class TriggerAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'form', 'event', 'dag', 'active', 'project', )

class ProcessAdmin(admin.ModelAdmin):
    list_display = ('name','qname','fname','active', )


admin.site.register(Trigger, TriggerAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Process, ProcessAdmin)