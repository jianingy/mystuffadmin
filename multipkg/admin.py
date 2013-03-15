#!/usr/bin/env python
# -*- coding: utf-8 -*-

# filename   : admin.py<2>
# created at : 2013-02-25 15:38:42
# author     : Jianing Yang <jianingy.yang AT gmail DOT com>

__author__ = 'Jianing Yang <jianingy.yang AT gmail DOT com>'

from django.contrib import admin
from multipkg.models import Package, Comment


class PackageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'version', 'release', 'build', 'owner',
                    'last_modified', 'created')
    search_fields = ('name', )
    actions = ['delete_selected']
    list_per_page = 50

admin.site.register(Package, PackageAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'package', 'created',)
    search_fields = ('name', )
    actions = ['delete_selected']
    list_per_page = 50

admin.site.register(Comment, CommentAdmin)
