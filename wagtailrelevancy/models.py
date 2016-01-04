from django.conf import settings
from django.db import models
from wagtail.wagtailcore.models import Page


class Reminder(models.Model):
    due_to_be_sent_at = models.DateTimeField(blank=True, null=True)
    page = models.ForeignKey(Page, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    sent = models.BooleanField(default=False)
