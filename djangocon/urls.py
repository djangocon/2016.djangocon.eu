"""djangocon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin

from djangocon import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^coc/$', views.coc, name='coc'),
    url(r'^glossary/$', views.glossary, name='glossary'),
    url(r'^venue/$', views.venue, name='venue'),
    url(r'^live/$', views.live, name='live'),
    url(r'^cfp/', include('cfp.urls', namespace='cfp')),
    url(r'^faq/', include('faq.urls', namespace='faq')),
    url(r'^scholarships/', include('scholarships.urls', namespace='scholarships')),
    url(r'^speakers/', include('speakers.urls', namespace='speakers')),
    url(r'^blog/', include('tinyblog.urls', namespace='blog')),
    url(r'^team/', include('organizers.urls', namespace='organizers')),
    url(r'^_webhooks/', include('webhooks.urls', namespace='webhooks')),
    url(r'^schedule/', include('schedule.urls', namespace='schedule')),
    url(r'^workshops/', include('workshops.urls', namespace='workshops')),
    url(r'^tips/', include('tips.urls', namespace='tips')),
    url(r'^badge/', include('badge.urls', namespace='badge')),

    url(r'^admin/', include('smuggler.urls')),
    url(r'^admin/', admin.site.urls),
]
