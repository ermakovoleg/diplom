from django.conf.urls import patterns

urlpatterns = patterns('flatpages.views',
    (r'^(?P<url>.*)$', 'flatpage'),
)
