# Create your views here.
#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" views.py

Main views
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2013 Vanderbilt University. All Rights Reserved'

from django.shortcuts import render_to_response


def index(request, *args, **kwargs):
    return render_to_response("main/index.html")


def about(request, *args, **kwargs):
    return render_to_response("main/about.html")
