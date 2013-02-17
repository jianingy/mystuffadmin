#!/usr/bin/env python
# -*- coding: utf-8 -*-

# filename   : admin.py
# created at : 2013-02-16 14:39:17
# author     : Jianing Yang <jianingy.yang AT gmail DOT com>

from django.contrib import admin
from domain.models import Zone, DynamicDomainName


class ZoneAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )
    search_fields = ('name', )
    actions = ['delete_selected']
    list_per_page = 50

admin.site.register(Zone, ZoneAdmin)


class DynamicDomainNameAdmin(admin.ModelAdmin):
    list_display = ('id', 'domainname', 'zone')
    search_fields = ('domainname', 'zone')
    actions = ['delete_selected']
    list_per_page = 50

admin.site.register(DynamicDomainName, DynamicDomainNameAdmin)
