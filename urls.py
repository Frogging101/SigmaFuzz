from django.conf.urls import patterns, url

from sigmafuzz import views

urlpatterns = patterns('',
        url(r'^$', views.splash),
        url(r'^about/$', views.about),
        url(r'^bot/$', views.bot),
        url(r'^index/$', views.index),
        url(r'^submit/$', views.submit),
        url(r'^login/$', views.loginView),
        url(r'^s/(\d*)/?$', views.submissionView),
        url(r'^s/(\d*)/?archive$', views.submissionArchive),
        url(r'^s/(\d*)/?archiveErr$', views.submissionArchiveErr),)
