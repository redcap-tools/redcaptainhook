#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" urls.py

Workflow URLS
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2013 Vanderbilt University. All Rights Reserved'


from django.conf.urls import patterns, url

from redcaptainhook.apps.workflow import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^trigger/(?P<site>\w+)', views.TriggerProcessor.as_view(), name='trigger'),
)
