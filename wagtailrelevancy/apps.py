from django.apps import AppConfig


class WagtailRelevancyConfig(AppConfig):
    name = 'wagtailrelevancy'
    verbose_name = "Wagtail Relevancy"

    def ready(self):
        import wagtailrelevancy.handlers
