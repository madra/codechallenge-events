''' events filters'''
# -*- coding: utf-8 -*-

import django_filters
from events.models import Event


class EventFilter(django_filters.FilterSet):
    '''
    Filter an event by title , date or owner
    '''

    def __init__(self, data, *args, **kwargs):
        '''
        override th filter to filter by new first
        '''
        data = data.copy()
        data.setdefault('order', '-event_date')
        super(EventFilter, self).__init__(data, *args, **kwargs)

    class Meta:
        model = Event
        fields = ['title', 'event_date', 'owner', ]
