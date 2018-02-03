#coding=utf-8

from . import views
from django.conf.urls import url 
from django.urls import include, path

urlpatterns = [
            path('', views.index, name='index'),
            url(r'^login', views.login, name='login'),
            url(r'^logout', views.logout, name='logout'),
            url(r'^(?P<person>persons)?/?(?P<name>[^/]+)/(?P<grade_info>[^/]+)_comments.html$', views.detail, name='detail'),
            url(r'^persons.html', views.persons, name='persons'),
            url(r'^update.html', views.update, name='update'),
        ]
