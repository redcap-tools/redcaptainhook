"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import RequestFactory, Client
from django.core.urlresolvers import reverse

from redcaptainhook.apps.workflow.models import Project, Process, Trigger,\
    History
from redcaptainhook.apps.workflow.views import TriggerProcessor, \
    filter_request_for_trigger, convert_redcap_post_data


def add_objects():
    # Projects
    proj1 = Project.objects.create(name="Test1", site="site1", redcap_pid=1, hash="foo")
    proj2 = Project.objects.create(name="Test2", site="site1", redcap_pid=2, hash="foo")
    proj3 = Project.objects.create(name="Test3", site="site2", redcap_pid=1, hash="foo")
    proj4 = Project.objects.create(name="Inactive", site="site1", redcap_pid=3, hash="foo", active=False)
    # Triggers
    t1 = Trigger.objects.create(status=2, form='demographics', project=proj1)
    t2 = Trigger.objects.create(status=1, form='imaging', project=proj1)
    t3 = Trigger.objects.create(status=2, form='imaging', active=False, project=proj1)
    t4 = Trigger.objects.create(status=2, form='demographics', project=proj2)
    t5 = Trigger.objects.create(status=2, form='demographics', project=proj3)
    t6 = Trigger.objects.create(status=2, form='demographics', project=proj4)
    # Processes
    proc1 = Process.objects.create(name='Process1', qname='default', fname='foo.bar.bat')
    proc2 = Process.objects.create(name='Process2', qname='default', fname='foo.bar.bar', active=False)
    proc3 = Process.objects.create(name='Process3', qname='default', fname='foo.bar.foo')
    proc4 = Process.objects.create(name='Process4', qname='default', fname='foo.bat.bar')
    proc5 = Process.objects.create(name='Process5', qname='default', fname='bar.bat.foo')

    # Set some relationships
    t1.processes.add(proc1, proc2)
    t2.processes.add(proc3)
    t3.processes.add(proc2)
    t4.processes.add(proc4)
    t5.processes.add(proc5)
    t6.processes.add(proc1)


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

    def tearDown(self):
        clear_objects()

    def test_trigger_filter(self):
        """Test finding trigger from project"""
        p1 = Project.objects.get(name='Test1')
        t1 = Trigger.objects.get(pk=1)
        self.assertIn(t1, p1.trigger_set.all())

    def test_trigger_get_active_processes(self):
        t = Trigger.objects.get(status=2,
            form='demographics', project__redcap_pid=1, project__site='site1')
        good_proc = Process.objects.get(name='Process1')
        inactive_proc = Process.objects.get(name='Process2')
        active_procs_from_t = t.get_active_processes()
        self.assertIn(good_proc, active_procs_from_t)
        self.assertNotIn(inactive_proc, active_procs_from_t)


class WorkflowViewTest(TestCase):
    def setUp(self):
        add_objects()
        # add factory
        self.factory = RequestFactory()

    def tearDown(self):
        clear_objects()

    def _build_trigger_url(self, site, auth=''):
        return '%s?auth=%s' % (reverse('workflow:trigger', args=(site,)), auth)

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

    def test_trigger_good_trigger(self):
        pid, site, form, status = '1', 'site1', 'demographics', '2'
        det = get_det(pid, form, status)
        url = self._build_trigger_url(site, 'foo')
        r = self.factory.post(url, data=det)
        project, post_data, t = filter_request_for_trigger(r, site)
        p = Project.objects.get(redcap_pid=pid, site=site)
        self.assertEqual(project, p)
        correct_trigger = p.trigger_set.get(form=form, status=status)
        self.assertEqual(correct_trigger, t)
        bad_trigger = p.trigger_set.get(status=1, form='imaging')
        self.assertNotEqual(bad_trigger, t)

    def test_trigger_inactive_project(self):
        "The trigger filter shouldn't return a trigger to an inactive project"
        pid, site, form, status = '3', 'site1', 'demographics', '2'
        det = get_det(pid, form, status)
        url = self._build_trigger_url(site, 'foo')
        r = self.factory.post(url, data=det)
        project, post_data, t = filter_request_for_trigger(r, site)
        self.assertIsNone(t)

    def test_trigger_bad_auth(self):
        "Bad auth parameter should not return a project/trigger combo"
        pid, site, form, status = '1', 'site1', 'demographics', '2'
        det = get_det(pid, form, status)
        url = self._build_trigger_url(site, 'notfoo')
        r = self.factory.post(url, data=det)
        project, post_data, t = filter_request_for_trigger(r, site)
        self.assertIsNone(project)
        self.assertIsNone(t)

    def test_trigger_inactive_trigger(self):
        "The trigger filter shouldn't return an inactive trigger"
        pid, site, form, status = '1', 'site1', 'imaging', '2'
        det = get_det(pid, form, status)
        url = '/rch/trigger/%s' % site
        r = self.factory.post(url, data=det)
        project, post_data, t = filter_request_for_trigger(r, site)
        self.assertIsNone(t)

    def test_history_additions(self):
        c = Client()
        pid, site, form, status = '1', 'site1', 'demographics', '2'
        det = get_det(pid, form, status)
        url = self._build_trigger_url(site, 'foo')
        response = c.post(url, data=det)
        self.assertEqual(response.status_code, 200)
        # Should have a 1 Project, 1 Trigger, and 1 Process records
        self.assertEqual(len(History.objects.all()), 3)
        self.assertEqual(len(History.objects.filter(entity_type=History.ENTITY_PROJECT)), 1)
        self.assertEqual(len(History.objects.filter(entity_type=History.ENTITY_TRIGGER)), 1)
        self.assertEqual(len(History.objects.filter(entity_type=History.ENTITY_PROCESS)), 1)



