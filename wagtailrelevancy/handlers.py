from datetime import timedelta

from django.conf import settings
from django.dispatch import receiver
from django.utils import timezone
from wagtail.wagtailcore.signals import page_published, page_unpublished

from .models import Reminder


@receiver(page_published)
def create_reminders(sender, **kwargs):
    instance = kwargs['instance']
    revision = kwargs['revision']
    user = revision.user

    reminder_queryset = Reminder.objects.filter(page=instance)

    if reminder_queryset.exists():
        if reminder_queryset.count() > 1:
            raise AttributeError('There should only ever be one reminder for a page!')
        remind_interval = reminder_queryset.first().reminder_interval
        due_to_be_sent_at = timezone.now() + timedelta(days=remind_interval)
        old_reminder = Reminder.objects.get(page=instance, sent=False)
        new_reminder = old_reminder
        new_reminder.user = user
        new_reminder.due_to_be_sent_at = due_to_be_sent_at
        new_reminder.save()


@receiver(page_unpublished)
def check_reminders(sender, **kwargs):
    instance = kwargs['instance']

    reminders = Reminder.objects.filter(page=instance)
    print('Removing {0} reminders, as the page {1} has been unpublished.'.format(reminders.count(), instance.title))
    reminders.delete()
