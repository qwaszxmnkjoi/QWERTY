from django.db import models


class Config(models.Model):
    title = models.CharField('Название конфига', max_length=80, default='Базовый конфиг')
    public_key = models.CharField('Public key LiqPay', max_length=100, blank=True, null=True)
    private_key = models.CharField('Private key LiqPay', max_length=100, blank=True, null=True)
    price = models.PositiveIntegerField('Стоимость подписки', default=200)

    p_login = models.CharField('Login Portmone', max_length=120, blank=True, null=True)
    p_password = models.CharField('Password Portmone', max_length=120, blank=True, null=True)
    p_payee_id = models.CharField('PayeeID Portmone', max_length=120, blank=True, null=True)
    p_credentials = models.TextField('Credentials Portmone', blank=True, null=True)

    is_active = models.BooleanField(default=True, verbose_name='Активный?')
    server_url = models.CharField('URL to get status from Payment', max_length=200, default='', help_text="https://your_server_url.com")

    class Meta:
        verbose_name = 'настройка'
        verbose_name_plural = 'настройки'

    def __str__(self):
        return self.title

    @property
    def liqpay_enable(self):
        return self.public_key and self.private_key

    @property
    def portmone_enable(self):
        return self.p_login and self.p_password and self.p_payee_id and self.p_credentials

    @property
    def any_enable(self):
        return self.portmone_enable or self.liqpay_enable

    def set_active_config(self):
        if self.is_active:
            other_active_configs = Config.objects.filter(is_active=True)
            for config in other_active_configs:
                if config.pk != self.pk:
                    config.is_active = False
                    config.save()

    def update_config(self):
        from .payment import service
        service.config = self

        return service

    def clean(self):
        self.set_active_config()
        self.update_config()
