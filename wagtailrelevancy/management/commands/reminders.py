from datetime import timedelta

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils import timezone
from wagtailrelevancy.models import Reminder


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        reminders = Reminder.objects.filter(sent=False)
        try:
            sent_from = settings.REMINDER_FROM_EMAIL
        except AttributeError:
            sent_from = settings.DEFAULT_FROM_EMAIL

        try:
            reminder_template = settings.REMINDER_TEMPLATE
        except AttributeError:
            reminder_template = 'wagtailrelevancy/reminder.html'

        for reminder in reminders:
            if reminder.due_to_be_sent_at.day == timezone.now().day:
                subject = 'Reminder: Check to see if you content on your page, {0}, is up to date!'.format(reminder.page.title)
                message = render_to_string(
                    reminder_template, {
                        'user': reminder.user,
                        'page': reminder.page,
                        'site_name': settings.WAGTAIL_SITE_NAME,
                    }
                )
                email = EmailMessage(
                    subject,
                    message,
                    sent_from,
                    [reminder.user.email])
                email.content_subtype = 'html'
                email.send()

                reminder.sent = True
                reminder.save()

        # Purge old sent reminders after 14 days, unless set to false in settings
        try:
            purge = settings.PURGE_REMINDERS
        except AttributeError:
            purge = True

        if purge:
            fourteen_days_after_now = timezone.now() + timedelta(days=14)
            stale_reminders = Reminder.objects.filter(sent=True, due_to_be_sent_at__gt=fourteen_days_after_now)
            if stale_reminders.exists():
                print('Purging {0} stale reminders'.format(stale_reminders.count()))
                stale_reminders.delete()
            else:
                print('There were no stale reminders to purge.')
