#!/usr/bin/env python
# -*- coding: utf-8 -*-

# filename   : tables.py
# created at : 2013-02-16 16:35:16
# author     : Jianing Yang <jianingy.yang AT gmail DOT com>

__author__ = 'Jianing Yang <jianingy.yang AT gmail DOT com>'

import django_tables2 as tables
from domain.models import DynamicDomainName
from django_tables2.utils import A


class DynamicDomainNameTable(tables.Table):

    fqdn = tables.LinkColumn('domain.views.ddns.update_view',
                             verbose_name='Full-Qualified Domain Name',
                             args=[A('pk')])
    record_a = tables.Column(verbose_name='IPv4 Address')
    record_aaaa = tables.Column(verbose_name='IPv6 Address')
    operation = tables.TemplateColumn(
        template_name="dns/ddns/table_action.html")

    class Meta:
        model = DynamicDomainName
        fields = ('fqdn', 'record_a', 'record_aaaa', 'last_update',
                  'operation')
        sequence = ('fqdn', 'record_a', 'record_aaaa', 'last_update',
                    'operation')
        orderable = False
