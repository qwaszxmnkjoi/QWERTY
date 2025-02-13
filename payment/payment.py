import typing

from .backends import LiqPayPayment, PortmonePayment
from .models import Config


class Payment:
    def __init__(self):
        self.config = Config.objects.filter(is_active=True).first()
        if not self.config:
            self.config = Config(
                title='DUMMY',
                price=200,
                is_active=True,
            )
            self.config.save()

    @property
    def amount(self):
        return self.config.price

    @property
    def lqp(self) -> typing.Optional[LiqPayPayment]:
        result = None
        if self.config.liqpay_enable:
            result = LiqPayPayment(self.config)

        return result

    def get_pay_links(self, lang='en', message_id=123, user_id='123213', result_url=None, date_start=None):
        message_id += 1
        result = {}
        if self.config.any_enable:
            if self.config.portmone_enable:
                backend = PortmonePayment(self.config)
                result[backend.alias] = backend.get_subscribe_link(lang, message_id, user_id, result_url, date_start)
            if self.lqp:
                result[self.lqp.alias] = self.lqp.get_subscribe_link(lang, message_id, user_id, result_url, date_start)

        return result

    def cancel_subscribe(self, order_id: str):
        result = {}
        if self.config.any_enable:
            if self.config.portmone_enable:
                backend = PortmonePayment(self.config)
                result[backend.alias] = backend.cancel_subscribe(order_id)
            if self.lqp:
                result[self.lqp.alias] = self.lqp.cancel_subscribe(order_id)

        return result


try:
    service = Payment()
except Exception as e:
    service = object()
    print(f'NOt Init Payment with Exc={e}')
