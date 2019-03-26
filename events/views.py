''' events views'''
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import FormView
from events.filters import EventFilter
from events.models import Event
from events.forms import AddEventForm, AddRsvpForm, UpdateEventForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.conf import settings
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


User = get_user_model()


class FilteredListView(ListView):
    filterset_class = None

    def get_queryset(self):
        # Get the Events and order_by pk
        queryset = super(FilteredListView, self).get_queryset().order_by(
            'event_date'
        )
        # Then use the query parameters and the queryset to
        # instantiate a filterset and save it as an attribute
        # on the view instance for later.
        self.filterset = self.filterset_class(
            self.request.GET, queryset=queryset
        )
        # Return the filtered queryset
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super(FilteredListView, self).get_context_data(**kwargs)
        # Pass the filterset to the template - it provides the form.
        context['filterset'] = self.filterset
        return context


class EventListView(FilteredListView):
    '''
    List the events
    template templates/events/event_list.html
    Pagination setting PAGINATION_NUM in settings
    '''
    paginate_by = settings.PAGINATION_NUM
    filterset_class = EventFilter
    model = Event


class EventDetailView(DetailView):
    '''
    Display the event
    template templates/events/event_detail.html
    '''
    model = Event

    def get_context_data(self, **kwargs):
        """
        Add extra context data here
        check if the user owns the event or if they can rsvp
        """
        context = super(EventDetailView, self).get_context_data(**kwargs)
        event = self.object
        # check if the user has already rspv'ed
        if self.request.user.is_authenticated:
            context['user_has_rsvp'] = event.user_has_rsvp(self.request.user)
            if event.owner == self.request.user:
                context['user_owns_event'] = True
        return context


@method_decorator(login_required, name='dispatch')
class EventUpdateView(UpdateView):
    '''
    CBV to update an event
    '''
    template_name = "edit_event.html"
    model = Event
    form_class = UpdateEventForm

    def get_success_url(self, *args, **kwargs):
        messages.success(
            self.request, 'Your Event was successfully updated.'
        )
        return self.object.url()

    def get_object(self, *args, **kwargs):
        obj = super(EventUpdateView, self).get_object(*args, **kwargs)
        if obj.owner != self.request.user:
            raise PermissionDenied()
        return obj


@method_decorator(login_required, name='dispatch')
class AddEventView(LoginRequiredMixin, FormView):
    '''
    CBV to add an event
    '''
    template_name = "add_event.html"
    form_class = AddEventForm

    def form_valid(self, form):
        form.save(self.request.user)
        return super(AddEventView, self).form_valid(form)

    def get_success_url(self, *args, **kwargs):
        messages.success(
            self.request, 'Your Event was successfully added.'
        )
        return reverse("home")


@login_required
def rsvp_event(request, pk):
    '''
    rsvp an event
    user cannot rsvp thier own event
    I used a FBV here to demonstrate that I can also use those
    '''
    event = get_object_or_404(
        Event.objects.filter(
            pk=pk)
    )
    if event.owner == request.user:
        messages.error(
            request,
            "You cannot RSVP your own event"
        )
    elif event.user_has_rsvp(request.user):
        messages.error(
            request,
            "You already RSVP'ed this event"
        )
    else:
        """
        All is well try to add the RSVP
        """
        data = {'event': event.pk, 'user': request.user.pk}
        form = AddRsvpForm(data)
        if form.is_valid():
            form.save()
            messages.success(
                request, "You Successfully RSVP'ed"
            )
        else:
            errors = form.errors
            messages.error(request, errors)
    return HttpResponseRedirect(event.url())
