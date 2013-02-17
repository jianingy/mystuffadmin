from django.conf.urls import patterns, url
from account.views import login, logout, profile
urlpatterns = patterns('account',
                       url(r'^profile/$', profile, name='account/profile'),
                       url(r'^login/$', login),
                       url(r'^logout/$', logout))
