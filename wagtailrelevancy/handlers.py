import datetime

from django.conf import settings
from django.dispatch import receiver
from wagtail.wagtailcore.signals import page_published

from .models import Reminder


@receiver(page_published)
def send_reminders(sender, **kwargs):
    instance = kwargs['instance']
    revision = kwargs['revision']
    user = revision.user

    try:
        remind_interval = settings.REMIND_INTERVAL
    except AttributeError:
        remind_interval = 14

    due_to_be_sent_at = datetime.datetime.now() + datetime.timedelta(days=remind_interval)

    try:
        old_reminder = Reminder.objects.get(page=instance, sent=False)
        old_reminder.due_to_be_sent_at = due_to_be_sent_at
        old_reminder.save()
        print('did this')
    except Reminder.DoesNotExist:
        Reminder.objects.create(
            page=instance,
            user=user,
            due_to_be_sent_at=due_to_be_sent_at
        )
