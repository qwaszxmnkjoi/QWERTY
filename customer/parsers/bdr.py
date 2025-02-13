from .base import ScrapperBase
from ..models import Bdr


class BdrScrapper(ScrapperBase):
    site_url = 'https://bdr.mvs.gov.ua'
    site_key = '6Ld0FP4UAAAAAMvqtSVXfZ5evqA2cZukPQDoHx0d'

    method_path = 'en/main/search/'
    method = 'post'

    def __init__(self, engine: Bdr, **kwargs):
        super().__init__(**kwargs)
        self.engine = engine

    def build_req_data(self):
        return {
            'plate': self.engine.plate,
            'document': self.engine.document,
            'g-recaptcha-response': self.captcha_code
        }

    def build_req_headers(self):
        return {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        }

