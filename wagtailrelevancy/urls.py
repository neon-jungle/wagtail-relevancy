from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from .views import actions, chooser

urlpatterns = [
    url(r'^$', chooser.edit,
        name='wagtailrelevancy'),
    url(r'^(?P<pk>.*)/$', actions.review,
        name='wagtailrelevancy_review'),
]
