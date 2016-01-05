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

    try:
        send_reminders = instance.send_reminders
    except AttributeError:
        send_reminders = False

    if send_reminders is True:
        try:
            remind_interval = settings.REMIND_INTERVAL
        except AttributeError:
            remind_interval = 14

        due_to_be_sent_at = timezone.now() + timedelta(days=remind_interval)

        try:
            old_reminder = Reminder.objects.get(page=instance, sent=False)
            old_reminder.due_to_be_sent_at = due_to_be_sent_at
            old_reminder.save()
        except Reminder.DoesNotExist:
            Reminder.objects.create(
                page=instance,
                user=user,
                due_to_be_sent_at=due_to_be_sent_at
            )


@receiver(page_unpublished)
def check_reminders(sender, **kwargs):
    instance = kwargs['instance']

    reminders = Reminder.objects.filter(page=instance)
    print('Removing {0} reminders, as the page {1} has been unpublished.'.format(reminders.count(), instance.title))
    reminders.delete()
