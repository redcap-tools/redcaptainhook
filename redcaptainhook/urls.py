from django.contrib import admin
from django.conf.urls import patterns, include, url


# See: https://docs.djangoproject.com/en/dev/ref/contrib/admin/#hooking-adminsite-instances-into-your-urlconf
admin.autodiscover()


# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = patterns('',
    # Admin panel and documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # django_rq
    url(r'^django-rq/', include('django_rq.urls')),
    # rch
    url(r'^rch/', include('redcaptainhook.apps.workflow.urls', namespace="workflow")),
    url(r'^$', 'redcaptainhook.apps.main.views.index', name='index'),
    url(r'^about$', 'redcaptainhook.apps.main.views.about', name='about'),
)
