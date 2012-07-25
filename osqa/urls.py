# coding: utf-8

from django.conf.urls import include, url
from django.conf import settings


urlpatterns = [
    url(r'^messages/', include('messages_extends.urls')),
    url(r'^', include('forum.urls')),
]

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns = [
        url(r'^rosetta/', include('rosetta.urls')),
    ] + urlpatterns


handler404 = 'forum.views.meta.page'
handler500 = 'forum.views.meta.error_handler'
