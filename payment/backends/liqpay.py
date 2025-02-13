from django.utils import timezone
from liqpay import LiqPay
from loguru import logger
from ..models import Config


class LiqPayPayment(LiqPay):
    alias = 'liqpay'

    def __init__(self, config: Config):
        try:
            self.config = config
            self.public_key = self.config.public_key
            self.private_key = self.config.private_key
            self.amount = self.config.price
            self.server_url = self.config.server_url + f'/paym/{self.alias}'
        except Exception:
            self.config = None
            self.public_key = ''
            self.private_key = ''
            self.amount = 200

        super().__init__(self.public_key, self.private_key)

    def get_subscribe_link(self, lang='en', message_id=123, user_id='123213', result_url=None, date_start=None):
        url = self.checkout_url({
            'action': 'subscribe',
            'subscribe': 1,
            'version': '3',
            'amount': self.amount,
            'currency': 'uah',
            'language': lang,
            'info': f"{message_id}_{user_id}",
            'description': 'Subscription payment for 30 days',
            'order_id': f'{user_id}_' + str(timezone.now().timestamp()) if
            date_start is None else str(date_start.timestamp()),
            'subscribe_date_start': str(
                timezone.now().replace(microsecond=0, tzinfo=None)
            ) if date_start is None else str(
                date_start.replace(microsecond=0, tzinfo=None)
            ),
            'subscribe_periodicity': 'month',
            'server_url': self.server_url,
            'result_url': result_url
        })
        logger.info(url)
        return url

    def cancel_subscribe(self, order_id: str):
        result = self.api('request', {
            'action': 'unsubscribe',
            'version': '3',
            'order_id': f'{order_id}'
        })
        return {
            'status': True if result['status'] == 'unsubscribed' and result['result'] == 'ok' else False,
            'result': result
        }
