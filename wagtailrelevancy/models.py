from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _
from wagtail.wagtailcore.models import Page as WagtailPage


class Reminder(models.Model):
    due_to_be_sent_at = models.DateTimeField(blank=True, null=True)
    reminder_interval = models.PositiveIntegerField()
    page_reviewed = models.BooleanField(default=True)
    page = models.ForeignKey(WagtailPage)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    sent = models.BooleanField(default=False)

    class Meta:
        unique_together = [['user', 'page']]

    def __str__(self):
        return _('{0} ({1})'.format(self.page.title, self.user.get_full_name()))
