from django.apps import AppConfig


class MakersHomeAppConfig(AppConfig):
    name = 'makers_home_app'

    def ready(self):
    	import makers_home_app.signals
