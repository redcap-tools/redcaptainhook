#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" func.py

Test functions
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2013 Vanderbilt University. All Rights Reserved'


def echo(**kwargs):
    print '\t'.join(['%s:%s' % (k, v) for k, v in kwargs.items()])
