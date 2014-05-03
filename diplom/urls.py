from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'diplom.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^form/', include('forms_custom.urls')),
    url(r'^report/', include('reports.urls')),

    url(r'^login/', 'user.views.login_view'),
    url(r'^logout/', 'user.views.logout_view'),
    url(r'^$', 'main.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
)
