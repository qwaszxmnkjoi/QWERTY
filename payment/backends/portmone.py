import hmac
import logging
from hashlib import sha256

import requests
from django.utils import timezone

from ..models import Config

logger = logging.getLogger("portmone")


class GatewayError(Exception):
    """Raised when API http request failed."""
    pass


class StatusCodeError(Exception):
    """Raised when API returns non-200 status code."""


class PortmonePayment:
    alias = 'portmone'

    def __init__(self, config: Config):
        try:
            self.config = config
            self.login = self.config.p_login
            self.password = self.config.p_password
            self.payee_id = self.config.p_payee_id
            self.credentials = self.config.p_credentials
            self.amount = self.config.price
            self.server_url = f'{self.config.server_url}/paym/{self.alias}'
        except Exception:
            self.config = None

            self.login = 'WDISHOP'  # PORTMONE
            self.password = 'wdi451'  # PORTMONE
            self.payee_id = 1185  # PORTMONE
            self.credentials = ''
            self.lang = 'uk'

            self.server_url = 'https://fcad-188-163-58-197.ngrok-free.app/paym/portmone'
            self.amount = 200

    def create_signature(self, date: str, order_num: str):
        login_bin = ''.join("{:02x}".format(ord(c)) for c in self.login)
        result = f'{self.payee_id}{date}{order_num}{int(self.amount)}{login_bin}'
        result = result.upper().encode('utf-8')
        result = hmac.new(self.credentials.encode('utf-8'), result, sha256).hexdigest().upper()
        return result

    @classmethod
    def _make_request(cls, url: str, payload: dict) -> dict:
        """Make request to API gateway.
        Raises:
            GatewayError: If no the API response.
            StatusCodeError: If the API response code is't 200.
        """
        try:
            response = requests.post(url, json=payload)
        except Exception as error:
            raise GatewayError

        if response.status_code != 200:
            raise StatusCodeError(code=response.status_code, message=response.content)

        return response.json()

    def get_subscribe_link(self, lang='en', message_id=123, user_id='123213', result_url=None, date_start=None):
        date = timezone.now().strftime('%Y%m%d%H%M%S')
        dt_start = date_start.strftime('%Y%m%d%H%M%S') if date_start else date
        order_num = f'{user_id}_{dt_start}'

        url = 'https://www.portmone.com.ua/gateway/'
        payload = {
            "method": "createLinkPayment",
            "paymentTypes": {
                "clicktopay": "Y",
                "createtokenonly": "N",
                "token": "N",
                "privat": "N",
                "gpay": "Y",
                "portmone": "Y",
                "applepay": "Y",
                "card": "Y"
            },
            "priorityPaymentTypes": {
                "card": 1,
                "applepay": 2,
                "gpay": 3,
                "clicktopay": 4,
                "portmone": 5
            },
            "payee": {
                "payeeId": self.payee_id,
                "login": self.login,
                "password": self.password,
                "credentials": self.credentials,
                "dt": date,
            },
            "order": {
                "description": "Subscription payment for 30 days",
                "shopOrderNumber": order_num,
                "billAmount": f"{self.amount}",
                "successUrl": self.server_url,
                "preauthFlag": "N",
                "billCurrency": "UAH",
                "attribute1": message_id,
                "attribute2": user_id,
            },
            "autopayment": {
                "show": "Y",
                "edit": "N",
                "defaultCheckboxState": "Y",
                "changeCheckboxState": "N",
                "settings": {
                    "period": "1",
                    "payDate": "27",
                    "amount": f"{self.amount}"
                },
                "signature": self.create_signature(date, order_num)
            },
            "payer": {
                "lang": f"{lang}",
                "emailAddress": "",
                "showEmail": "N"
            }
        }

        result: dict = self._make_request(url, payload)
        if result:
            try:
                result: str = result.get('linkPayment')
                return result
            except IndexError:
                logger.error(f"Failed to get link")
                return None

    def cancel_subscribe(self, order_id: str):
        return {
            'status': False,
            'result': {'alias': self.alias}
        }
