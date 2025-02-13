import pytz
import logging
from functools import cached_property

from django.conf import settings
from requests_html import HTML, HTMLSession, HTMLResponse
from twocaptcha import TwoCaptcha


class ScrapperBase(HTMLSession):
    retry_count = 2
    site_key: str = None
    site_url: str = None
    api_key: str = settings.RECAPTCHA_TOKEN

    method_path: str = None
    method: str = None
    method_use_json: bool = False

    def __init__(self, **kwargs):
        assert self.site_key, '`site_key` must be specified'
        assert self.site_url, '`captcha_url` must be specified'
        super().__init__(**kwargs)
        self.set_log_debug()
        self.captcha_engine = TwoCaptcha(self.api_key)

    def set_log_debug(self):
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger('requests.packages.urllib3')
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

    @cached_property
    def dt_tz(self):
        return pytz.timezone(settings.TIME_ZONE)

    @cached_property
    def captcha_code(self):
        return self.build_captcha()

    def build_captcha(self, raise_exception: bool = False):
        result = None
        for c in range(self.retry_count):
            try:
                resp: dict = self.captcha_engine.recaptcha(
                    sitekey=self.site_key,
                    url=self.site_url
                )
            except Exception as e:
                if raise_exception:
                    raise e
                continue
            else:
                code = resp.get('code')
                if code is None:
                    continue
                result = code
        return result

    @cached_property
    def req_url(self):
        return self.build_req_url()

    def build_req_url(self):
        return f'{self.site_url}/{self.method_path}'

    @cached_property
    def req_data(self):
        return self.build_req_data()

    def build_req_data(self):
        raise NotImplementedError

    @cached_property
    def req_headers(self):
        return self.build_req_headers()

    def build_req_headers(self):
        return {}

    def scrap(self) -> HTMLResponse:
        data = None if self.method_use_json else self.req_data
        json_data = self.req_data if self.method_use_json else None
        method = getattr(self, self.method, self.post)
        resp = method(
            url=self.req_url,
            data=data,
            json=json_data,
            headers=self.req_headers
        )
        return resp

    def scrap_as_json(self):
        resp = self.scrap()
        return resp.json()

    def scrap_as_html(self, encoding: str = 'utf-8') -> HTML:
        data = self.scrap()
        if data and getattr(data, 'text', None):
            data = data.text
        return HTML(html=data, default_encoding=encoding)
