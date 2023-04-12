# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
#from django.conf.urls import url
#from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('routers.http_routers'))
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)