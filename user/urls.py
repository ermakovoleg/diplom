from django.conf.urls import patterns

from user.views import *

urlpatterns = patterns('',
    #(r'^maps/(\w+)/$', maps),
    (r'^$', get_user),
    #(r'^(?P<pk>[0-9]+)/$', get_report),
    (r'^password/reset/$', 'django.contrib.auth.views.password_reset', {'post_reset_redirect' : '/user/password/reset/done/'}),
    (r'^password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'post_reset_redirect' : '/user/password/done/'}),
    (r'^password/done/$','django.contrib.auth.views.password_reset_complete'),
)