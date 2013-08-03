"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import RequestFactory

from redcaptainhook.apps.workflow.models import Project, Process, Trigger
from redcaptainhook.apps.workflow.views import TriggerProcessor, \
    filter_request_for_trigger, convert_redcap_post_data


def add_objects():
    # Projects
    proj1 = Project.objects.create(name="Test1", site="site1", redcap_pid=1, hash="foo")
    proj2 = Project.objects.create(name="Test2", site="site1", redcap_pid=2, hash="foo")
    proj3 = Project.objects.create(name="Test3", site="site2", redcap_pid=1, hash="foo")
    # Triggers
    t1 = Trigger.objects.create(status=2, form='demographics', project=proj1)
    t2 = Trigger.objects.create(status=1, form='imaging', project=proj1)
    t3 = Trigger.objects.create(status=2, form='imaging', project=proj1)
    t4 = Trigger.objects.create(status=2, form='demographics', project=proj2)
    t5 = Trigger.objects.create(status=2, form='demographics', project=proj3)
    # Processes
    proc1 = Process.objects.create(name='Process1', qname='default', fname='foo.bar.bat')
    proc2 = Process.objects.create(name='Process2', qname='default', fname='foo.bar.bar')
    proc3 = Process.objects.create(name='Process3', qname='default', fname='foo.bar.foo')
    proc4 = Process.objects.create(name='Process4', qname='default', fname='foo.bat.bar')
    proc5 = Process.objects.create(name='Process5', qname='default', fname='bar.bat.foo')

    # Set some relationships
    t1.processes.add(proc1, proc2)
    t2.processes.add(proc3)
    t3.processes.add(proc2)
    t4.processes.add(proc4)
    t5.processes.add(proc5)


def clear_objects():
    Project.objects.all().delete()
    Trigger.objects.all().delete()
    Process.objects.all().delete()


def get_det(pid=1, form='demographics', status=2, event='', dag='', record=1):
    """Simple method to transform normal field names to keys found in REDCap
    POST data"""
    status_key = '%s_complete' % form
    return {'project_id': pid,
            'instrument': form,
            status_key: status,
            'record': record,
            'redcap_event_name': event,
            'redcap_data_access_group': dag}


class WorkflowModelTest(TestCase):

    def setUp(self):
        "Set up the test db"
        add_objects()

    def test_trigger_filter(self):
        """Test finding trigger from project"""
        p1 = Project.objects.get(pk=1)
        t1 = Trigger.objects.get(pk=1)
        self.assertIn(t1, p1.trigger_set.all())


class WorkflowViewTest(TestCase):
    def setUp(self):
        add_objects()
        # add factory
        self.factory = RequestFactory()

    def tearDown(self):
        clear_objects()

    def test_trigger_get(self):
        r = self.factory.get('/rch/trigger/foo/')
        view_func = TriggerProcessor.as_view()
        response = view_func(r)
        self.assertEqual(response.status_code, 200)

    def test_post_data_transform(self):
        basic_det = get_det()
        xfm = convert_redcap_post_data(basic_det)
        for good_k in ['pid', 'record', 'status', 'form', 'event', 'dag']:
            self.assertIn(good_k, xfm)

    def test_trigger_post_good_trigger(self):
        pid, site, form, status = '1', 'site1', 'demographics', '2'
        det = get_det(pid, form, status)
        url = '/rch/trigger/%s' % site
        r = self.factory.post(url, data=det)
        post_data, t = filter_request_for_trigger(r, site)
        p = Project.objects.get(redcap_pid=pid, site=site)
        correct_trigger = p.trigger_set.get(form=form, status=status)
        self.assertEqual(correct_trigger, t)
        bad_trigger = p.trigger_set.get(status=1, form='imaging')
        self.assertNotEqual(bad_trigger, t)
