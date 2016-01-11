from datetime import timedelta

from django.dispatch import receiver
from django.utils import timezone
from wagtail.wagtailcore.signals import page_published

from .models import Reminder


@receiver(page_published)
def create_reminders(sender, **kwargs):
    instance = kwargs['instance']

    reminder_queryset = Reminder.objects.filter(page=instance)

    for reminder in reminder_queryset:
        due_to_be_sent_at = timezone.now() + timedelta(days=reminder.reminder_interval)
        reminder.due_to_be_sent_at = due_to_be_sent_at
        reminder.sent = False
        reminder.save()
