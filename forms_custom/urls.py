from django.conf.urls import patterns

from forms_custom.views import *

urlpatterns = patterns('',
    (r'^(?P<template>[A-Za-z0-9_-]+)/$', get_form),
)