#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" models.py

Main workflow models
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2013 Vanderbilt University. All Rights Reserved'


import datetime

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

from qsstats import QuerySetStats
import django_rq


class HistoryManager(models.Manager):
    def timeseries_by_day(self, entity_type, days_ago=7):
        now = datetime.date.today()
        beg_day = now - datetime.timedelta(days=days_ago)
        qs = super(HistoryManager, self).filter(entity_type=entity_type)
        ts = QuerySetStats(qs, 'timestamp').time_series(beg_day, now)
        ret = []
        for dt, count in ts:
            ret.append({'time':dt.isoformat(), 'count': count})
        return ret

class History(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    ENTITY_PROJECT = 1
    ENTITY_TRIGGER = 2
    ENTITY_PROCESS = 3
    ENTITY_CHOICES = (
        (ENTITY_PROJECT, 'Project'),
        (ENTITY_TRIGGER, 'Trigger'),
        (ENTITY_PROCESS, 'Process'),)
    entity_type = models.IntegerField(choices=ENTITY_CHOICES, default=ENTITY_PROJECT)
    entity_pk = models.IntegerField(default=0)
    objects = HistoryManager()


class Trigger(models.Model):

    STATUS_INCOMPLETE = 0
    STATUS_UNVERIFIED = 1
    STATUS_COMPLETE = 2
    STATUS_CHOICES = (
                     (STATUS_INCOMPLETE, 'Incomplete'),
                     (STATUS_UNVERIFIED, 'Unverified'),
                     (STATUS_COMPLETE, 'Complete'),)
    status = models.IntegerField(choices=STATUS_CHOICES,
                                 default=STATUS_INCOMPLETE)
    form = models.CharField(max_length=50)
    event = models.CharField(max_length=50, blank=True)
    dag = models.CharField(max_length=50, blank=True)
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=50, null=False)
    project = models.ForeignKey('Project')
    processes = models.ManyToManyField('Process')

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.default_name()
        super(Trigger, self).save(*args, **kwargs)

    def default_name(self):
        return '&'.join(['form:%s' % self.form,
                         'status:%d' % self.status,
                         'event:%s' % self.event,
                         'dag:%s' % self.dag])

    def __unicode__(self):
        return '<Trigger(%s, %s, %d)>' % (self.project.name,
                                          self.form,
                                          self.status)

    def get_active_processes(self):
        return self.processes.filter(active=True)

    def activate(self, det_context):
        self.log()
        for process in self.get_active_processes():
            process.activate(det_context)

    def log(self):
        History.objects.create(entity_type=History.ENTITY_TRIGGER, entity_pk=self.pk)


class Project(models.Model):

    name = models.CharField(max_length=50)
    site = models.CharField(max_length=40, default="vanderbilt")
    redcap_pid = models.IntegerField(default=0)
    hash = models.CharField(max_length=50, default=None)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["redcap_pid"]
        unique_together = (('site', 'redcap_pid'))

    def __unicode__(self):
        return "<Project(%s, %s, %d)>" % (self.site, self.name, self.redcap_pid)

    def log(self):
        History.objects.create(entity_type=History.ENTITY_PROJECT, entity_pk=self.pk)

    def trigger_url(self):
        return '%s%s?auth=%s' % (settings.BASE_DOMAIN,
            reverse('workflow:trigger', args=(self.site,)), self.hash)

class Process(models.Model):

    name = models.CharField(max_length=50)
    qname = models.CharField(max_length=50)
    fname = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "processes"

    def __unicode__(self):
        return '<Process(%s)>' % (self.name)

    def activate(self, det_context):
        self.log()
        queue = django_rq.get_queue(self.qname)
        queue.enqueue(self.fname, **det_context)

    def log(self):
        History.objects.create(entity_type=History.ENTITY_PROCESS, entity_pk=self.pk)
