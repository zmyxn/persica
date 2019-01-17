from django.apps import AppConfig


class FundsConfig(AppConfig):
    name = 'apps.funds'
    verbose_name = '资金详情'

    def ready(self):
        import apps.funds.singals
