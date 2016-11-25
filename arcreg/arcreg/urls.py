"""testapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from blueslip.views import *


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/$', home, name='home'),
    url(r'^2638hjsbd3245347/$', clash, name='clash'),
    url(r'^home/tt/$', timetable, name='tt'),
    url(r'^update/$', update, name='update'),
    url(r'^submit/$', submit, name='submit'),
    url(r'^home/(?P<id>\d+)/adelete/$', adelete, name='adelete'),
    url(r'^home/(?P<id>\d+)/rdelete/$', rdelete, name='rdelete'),
    url(r'^add/$', add, name='add'),
    url(r'^remove/$', remove, name='remove'),
    url(r'^status/$', status, name='status'),
    url(r'^instructions/$', instructions, name='instructions'),
 	url(r'',include('registration.backends.simple.urls')),
]

admin.site.site_header = 'Your Header'
admin.site.site_title = 'Your Title'
admin.site.index_title = 'ADMIN'

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
