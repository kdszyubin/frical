from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^', include('home.urls', namespace = "home")),
    url(r'^jobs/', include('jobs.urls', namespace = "jobs")),
    url(r'^polls/', include('polls.urls', namespace = "polls")),
    url(r'^contact/', include('contacts.urls', namespace = "contacts")),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT}),
    )
