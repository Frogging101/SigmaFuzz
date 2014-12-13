from django.conf.urls import patterns, url

from sigmafuzz import views

urlpatterns = patterns('',
        url(r'^$', views.splash),
        url(r'^index/', views.index),
        url(r'^submit/$', views.submit),
        url(r'^submit/doSubmit$', views.doSubmit),)
