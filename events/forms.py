''' events forms '''
# -*- coding: utf-8 -*-
from django import forms
from events.models import Event, Rsvp
from registration.forms import RegistrationFormUniqueEmail
from django.utils.translation import ugettext_lazy as _
from django.forms.extras.widgets import SelectDateWidget
attrs_dict = {'class': 'required'}


class CustomRegistrationForm(RegistrationFormUniqueEmail):
    """
    A registration form that only requires the user to enter their e-mail
    address and password. The username is automatically generated

    """
    username = forms.CharField(
        widget=forms.HiddenInput, max_length=75, required=False)

    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=75)),
                             label=_("E-mail"))

    def clean_username(self):
        "This function is required to overwrite an inherited username clean"
        return self.cleaned_data['username']

    def clean(self):
        if not self.errors:
            # simply use the email for the username:
            self.cleaned_data['email'] = self.cleaned_data['email'].strip(
            ).lower()
            self.cleaned_data['username'] = self.cleaned_data['email']

        super(CustomRegistrationForm, self).clean()
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        # reorder the fields
        super(CustomRegistrationForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['email', 'password1', 'password2']


class AddEventForm(forms.ModelForm):

    """Form for adding  an event"""

    event_date = forms.DateField(widget=SelectDateWidget)
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Event
        fields = ['title', 'description',
                  'participants', 'event_date', ]

    def save(self, user):
        '''
        custom save method to add owner
        '''
        event = super(AddEventForm, self).save(commit=False)
        if event:
            event.owner = user
        event.save()
        return event


class AddRsvpForm(forms.ModelForm):

    """Form for adding  an rsvp for event"""

    class Meta:
        model = Rsvp
        fields = ['event', 'user', ]


class UpdateEventForm(forms.ModelForm):

    """Form for adding  an event"""

    event_date = forms.DateField(widget=SelectDateWidget)
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Event
        fields = ['title', 'description',
                  'participants', 'event_date', ]

    def clean_participants(self):
        "Clean the number of participants, make sure they are not less than what was already RSVP"
        particpants = self.cleaned_data['participants']
        if particpants < self.instance.rsvp_num:
            raise forms.ValidationError(
                "{} participants already RSVP'ed , you cannot have less participants than that".format(
                    self.instance.rsvp_num
                )
            )
        return self.cleaned_data['participants']
