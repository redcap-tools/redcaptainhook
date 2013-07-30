# Create your views here.

from django.views import generic
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from redcaptainhook.apps.workflow.models import Project


class IndexView(generic.ListView):
    template_name = "workflow/index.html"
    context_object_name = "project_list"

    def get_queryset(self):
        """Return all projects"""
        return Project.objects.order_by('-redcap_pid')


class TriggerProcessor(generic.TemplateView):
    """ Class-based view for handling incoming data entry triggers from
    REDCap.

    This entire class has been csrf_exempted. Under no circumstances
    should this class implement any other views other than handling the POST
    from REDCap.
    """
    template_name = "workflow/trigger.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(TriggerProcessor, self).dispatch(*args, **kwargs)

    def post(self, request, site):
        pd = request.POST
        pid = int(pd['project_id'][0])
        try:
            project = Project.objects.filter(redcap_pid=pid)[0]
            print "Searching triggers from %s" % project
        except IndexError:
            # Alert for request that we don't have project?
            pass
        finally:
            return HttpResponse(content='Thank you\n', status=200)
