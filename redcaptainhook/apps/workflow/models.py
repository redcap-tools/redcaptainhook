#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" models.py

Main workflow models
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2013 Vanderbilt University. All Rights Reserved'


from django.db import models
from django.contrib import admin


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
    project = models.ForeignKey('Project')
    processes = models.ManyToManyField('Process')

    def __unicode__(self):
        return '<Trigger(%s, %s, %d)>' % (self.project.name,
                                          self.form,
                                          self.status)

    def get_active_processes(self):
        return self.processes.filter(active=True)

    def activate(self, det_context):
        self.log()
        for process in self.get_active_processes():
            process.activate(**det_context)

    def log(self):
        print "Logging %s" % self


class Project(models.Model):

    name = models.CharField(max_length=20)
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
        print "Logging %s" % self


class Process(models.Model):

    name = models.CharField(max_length=50)
    qname = models.CharField(max_length=50)
    fname = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "processes"

    def __unicode__(self):
        return '<Process(%s)>' % (self.name)

    def activate(self, **kwargs):
        self.log()
        print "Activating %s..." % self

    def log(self):
        print "Logging %s" % self


#  Register models to admin site
admin.site.register(Project)
admin.site.register(Process)
admin.site.register(Trigger)
