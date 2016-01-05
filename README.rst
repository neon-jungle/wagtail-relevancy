===============
wagtail-relevancy
===============

A plugin for assisting editors with keeping their content up to date.
This plugin will send reminders to editors at set intervals to make sure their content
is still up to date and relevant.

Installing
==========

Install using pip::

    pip install wagtail-relevancy

It works with Wagtail 1.0 and upwards.

Usage
=====

To enable the reminders you will need to set `send_reminders` to `True` on your `Page` class definition.
By default, this will send editors a reminder 14 days after they publish something to remind them to check the content
they have entered to see if it is still up to date, or 'relevant'.

The default settings are as follows, and can be overriden.

.. code-block:: python

    PURGE_REMINDERS = True  # Reminder objects will be purged 14 days after being sent
    REMINDER_TEMPLATE = 'wagtailrelevancy/reminder.html'  # The template for reminder email, the variables user, page and site_name are available in the context
    REMINDER_FROM_EMAIL = ''  #  This will default to the Django global setting, DEFAULT_FROM_EMAIL
    REMIND_INTERVAL = 14  #  The amount of days after a page has been published that the editor will receive a reminder.
