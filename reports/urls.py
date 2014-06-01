from django.conf.urls import patterns

from reports.views import *

urlpatterns = patterns('',
    (r'^maps/(\w+)/$', maps),
    (r'^$', get_reports),
    (r'^(\w+)/$', get_report),

)