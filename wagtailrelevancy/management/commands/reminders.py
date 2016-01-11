from datetime import timedelta

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import ugettext as _
from wagtailrelevancy.models import Reminder


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        reminders = Reminder.objects.filter(sent=False, due_to_be_sent_at__lt=timezone.now(), page__live=True)
        try:
            sent_from = settings.REMINDER_FROM_EMAIL
        except AttributeError:
            sent_from = settings.DEFAULT_FROM_EMAIL

        try:
            reminder_template = settings.REMINDER_TEMPLATE
        except AttributeError:
            reminder_template = 'wagtailrelevancy/reminder.html'

        for reminder in reminders:
            subject = _('Reminder: Check to see if the content on the page, {0}, is up to date!'.format(reminder.page.title))
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
            reminder.page_reviewed = False
            reminder.save()

        # Purge old sent reminders after 14 days, unless set to false in settings
        try:
            purge = settings.PURGE_REMINDERS
        except AttributeError:
            purge = True
            default_purge_days = 14

        if purge:
            fourteen_days_after_now = timezone.now() + timedelta(days=default_purge_days)
            stale_reminders = Reminder.objects.filter(sent=True, due_to_be_sent_at__gt=fourteen_days_after_now)
            if stale_reminders.exists():
                print(_('Purging {0} stale reminders'.format(stale_reminders.count())))
                stale_reminders.delete()
            else:
                print(_('There were no stale reminders to purge.'))
