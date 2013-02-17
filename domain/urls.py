#!/usr/bin/env python
# -*- coding: utf-8 -*-

# filename   : urls.py<2>
# created at : 2013-02-16 16:44:48
# author     : Jianing Yang <jianingy.yang AT gmail DOT com>

__author__ = 'Jianing Yang <jianingy.yang AT gmail DOT com>'

from django.conf.urls import patterns, url
# from django.views.generic.base import TemplateView
from domain.views import ddns, api

urlpatterns = patterns('domain.views',
                       url(r'^ddns/$',
                           ddns.list_view, name='ddns/home'),
                       url(r'^ddns/doc/$',
                           ddns.doc_view),
                       url(r'^ddns/create/$',
                           ddns.create_view),
                       url(r'^ddns/update/(?P<pk>\d+)/$',
                           ddns.update_view),
                       url(r'^ddns/delete/(?P<pk>\d+)/$',
                           ddns.delete_view),
                       url(r'^ddns/api/update_ip/$', api.update_ddns_ip),
)
