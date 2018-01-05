from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from prefslip.views import *


urlpatterns = [
    url(r'^offers/$', offers, name='offers'),
    url(r'^pr/$', pr, name='pr'),
    url(r'^prefstatus/$', prefstatus, name='prefstatus'),
    url(r'^prefstatus/(?P<priority>\d+)/(?P<discipline>\w+)/prefdelete$', prefdelete, name='prefdelete'),
    url(r'^avail/(?P<disp>\w+)/$', available_courses, name='avail'),
]