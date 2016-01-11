from datetime import timedelta

from django import forms
from django.contrib.auth import get_user_model
from django.forms.models import inlineformset_factory
from django.utils import timezone
from wagtail.wagtailadmin.widgets import AdminPageChooser
from wagtail.wagtailcore.models import Page

from .models import Reminder

User = get_user_model()


class HiddenDeleteFormSet(forms.models.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(HiddenDeleteFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.fields['DELETE'].widget = forms.HiddenInput()

    @property
    def empty_form(self):
        empty_form = super(HiddenDeleteFormSet, self).empty_form
        empty_form.fields['DELETE'].widget = forms.HiddenInput()
        return empty_form


class ReminderForm(forms.ModelForm):
    page = forms.ModelChoiceField(queryset=Page.objects.all(),
                                  widget=AdminPageChooser(show_edit_link=False, can_choose_root=True))

    class Meta:
        model = Reminder
        fields = ('page', 'reminder_interval')

    def save(self, commit=True):
        instance = super(ReminderForm, self).save(commit=False)
        if commit:
            print('called')
            instance.due_to_be_sent_at = timezone.now() + timedelta(days=instance.reminder_interval)
            instance.save()
        return instance

ReminderFormSet = inlineformset_factory(
    User,
    Reminder,
    form=ReminderForm,
    formset=HiddenDeleteFormSet,
    extra=0,
)
