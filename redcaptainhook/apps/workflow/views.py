# Create your views here.

from django.views import generic
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from redcaptainhook.apps.workflow.models import Project


def convert_redcap_post_data(post_dict):
    """Converts REDCap POST data to better k/v pairs

    Parameters
    ----------
    post_dict: dict, most likely request.POST.dict()

    Returns
    -------
    A dict of the POST data with the following key conversions:
        project_id ----------------> pid (int)
        instrument ----------------> form
        record --------------------> record
        [instrument]_complete -----> status (int)
        redcap_event_name ---------> event
        redcap_data_access_group --> dag
    """
    pid = int(post_dict.get('project_id', 0))
    form = post_dict.get('instrument', '')
    record = post_dict.get('record', '')
    status = post_dict.get('%s_complete' % form, '')
    event = post_dict.get('redcap_event_name', '')
    dag = post_dict.get('redcap_data_access_group', '')
    return {'pid': pid,
            'form': form,
            'record': record,
            'status': status,
            'event': event,
            'dag': dag,
            }


def filter_request_for_trigger(request, site=None):
    """Main function for grabbing a single Trigger from the incoming
    POST"""
    d = convert_redcap_post_data(request.POST.dict())
    d['site'] = site
    try:
        p = Project.objects.get(redcap_pid=d['pid'], site=site, active=True)
    except Project.DoesNotExist:
        # No projects match this request
        # Why are we getting this request?
        return None, d, None
    qs = p.trigger_set.filter(form=d['form'], status=d['status'], active=True)
    if d['event']:
        qs = qs.filter(event=d['event'])
    if d['dag']:
        qs = qs.filter(dag=d['dag'])
    try:
        trigger = qs.all()[0]
    except IndexError:
        return p, d, None
    else:
        return p, d, trigger


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
    should this class implement any unsafe views other than
    handling the POST from REDCap.
    """
    template_name = "workflow/trigger.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(TriggerProcessor, self).dispatch(*args, **kwargs)

    def post(self, request, site):
        project, post_data, trigger = filter_request_for_trigger(request, site)
        if project:
            project.log()
        if trigger:
            trigger.activate(post_data)
        return HttpResponse(content=u'Thank you\n', status=200)
