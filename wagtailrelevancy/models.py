from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.models import Page as WagtailPage

PAGE_PERMISSION_TYPE_CHOICES = [
    ('add', 'Add/edit pages you own'),
    ('edit', 'Edit any page'),
    ('publish', 'Publish any page'),
    ('lock', 'Lock/unlock any page'),
]


class GroupPagePermission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    page = models.ForeignKey(WagtailPage)
    permission_type = models.CharField(
        verbose_name='permission type',
        max_length=20,
        choices=PAGE_PERMISSION_TYPE_CHOICES
    )

    class Meta:
        unique_together = ('user', 'page', 'permission_type')

class UserPreferences(models.Model):
    pass  # TODO


class RelevancyMixin(models.Model):
    reminder_interval = models.IntegerField(blank=True, null=True)

    settings_panels = WagtailPage.settings_panels + [
        FieldPanel('reminder_interval')
    ]

    class Meta:
        abstract = True

    def get_panel(self):
        pass

    def save_revision(self, user=None, submitted_for_moderation=False, approved_go_live_at=None, changed=True):
        out = super(RelevancyMixin, self).save_revision(
            user=user,
            submitted_for_moderation=submitted_for_moderation,
            approved_go_live_at=approved_go_live_at,
            changed=changed,
        )
        if self.reminder_interval:
            current_reminders = Reminder.objects.filter(user=user)
            if current_reminders.exists():
                reminder_due = timezone.now() + timedelta(days=self.reminder_interval)
                reminder = current_reminders.objects.first()

            else:
                Reminder.objects.create(
                    page=self,
                    user=user,
                    due_to_be_sent_at=reminder_due
                )

        return out


class Reminder(models.Model):
    due_to_be_sent_at = models.DateTimeField(blank=True, null=True)
    page_reviewed = models.BooleanField(default=False)
    page = models.ForeignKey(WagtailPage)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    sent = models.BooleanField(default=False)

    def __str__(self):
        return '{0} ({1})'.format(self.page.title, self.user.get_full_name())
