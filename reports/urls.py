from django.conf.urls import patterns

from reports.views import *

urlpatterns = patterns('',
    (r'^(\w+)/$', get_report),
)