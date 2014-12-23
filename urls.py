from django.conf.urls import patterns, url

from sigmafuzz import views

urlpatterns = patterns('',
        url(r'^$', views.splash),
        url(r'^about/$', views.about),
        url(r'^bot/$', views.bot),
        url(r'^index/(\d*)$', views.index),
        url(r'^submit/$', views.submit),
        url(r'^login/$', views.loginView),
        url(r'^tasks/$', views.tasks),
        url(r'^s/(\d*)/?$', views.submissionView),
        url(r'^s/(\d*)/?archival$', views.submissionArchival),
        url(r'^s/(\d*)/?approval$', views.submissionApproval),
        url(r'^s/(\d*)/?archiveErr$', views.submissionArchiveErr),)
