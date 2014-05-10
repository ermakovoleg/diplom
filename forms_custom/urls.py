from django.conf.urls import patterns

from forms_custom.views import *

urlpatterns = patterns('',
    (r'^publish/$',form_publish),
    (r'^status/(?P<pk>[0-9]+)/$',form_status),
    (r'^record/(?P<pk>[0-9]+)/$',get_record),
    (r'^(?P<template>[0-9]+)/$', get_form),
)