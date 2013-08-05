#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" urls.py

Main pages urls
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2013 Vanderbilt University. All Rights Reserved'

from django.conf.urls import patterns, url

from .views import about, index

urlpatterns = patterns('',
    url(r'^about$', about, name='about'),
    url(r'^$', index, name='index'),
)
