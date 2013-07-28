#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" tasks.py

RQ testing
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2013 Vanderbilt University. All Rights Reserved'


from requests import get
import django_rq
from django_rq import job


@job
def get_url(url):
    r = get(url)
    return r.text
