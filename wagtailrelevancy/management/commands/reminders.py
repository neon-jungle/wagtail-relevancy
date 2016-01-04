import datetime

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
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
            print(reminder.due_to_be_sent_at.day)
            print(datetime.datetime.now().day)
            if reminder.due_to_be_sent_at.day == datetime.datetime.now().day:
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
