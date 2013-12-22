'''from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()
# Uncomment the next two lines to enable the admin:
'''
'''from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
'''
from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
    (r'^$', 'BuiltyMaker.builty.views.index'),
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('registration.urls')),
    (r'^main/', include('BuiltyMaker.builty.urls')),
)

