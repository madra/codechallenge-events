
"""events URL Configuration"""
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.contrib import admin
from events import views

urlpatterns = [
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^add-event.html', views.AddEventView.as_view(), name="add_event"),
    url(r'^event/(?P<pk>\d+)/rsvp/', views.rsvp_event, name="rsvp_event"),
    url(r'^event/(?P<pk>\d+)/edit/',
        views.EventUpdateView.as_view(), name="event_edit"),
    url(r'^event/(?P<pk>\d+)/', views.EventDetailView.as_view(), name="event_detail"),
    url(r'^$', views.EventListView.as_view(), name="home"),
]
