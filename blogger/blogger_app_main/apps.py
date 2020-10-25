from django.apps import AppConfig


class BloggerAppMainConfig(AppConfig):
    name = 'blogger_app_main'

    def ready(self):
        import blogger_app_main.signals