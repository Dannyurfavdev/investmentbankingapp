from django.apps import AppConfig


class InvestmentbankappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'investmentbankapp'

    def ready(self):
    	import investmentbankapp.signals
