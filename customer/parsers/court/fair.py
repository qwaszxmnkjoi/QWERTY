from customer.models import Search
from ..base import ScrapperBase


class CourtFairScrapper(ScrapperBase):
    site_url = 'https://court.gov.ua'
    site_key = '6LdIjOQSAAAAAA5VkX2tOq9Znrem2-r_WZi6Jetn'

    method = 'post'

    def __init__(self, engine: Search, **kwargs):
        super().__init__(**kwargs)
        self.engine = engine

    def build_req_url(self):
        return f'{self.site_url}/fair.php'

    def build_req_data(self):
        return {
            'sEcho': '2',
            'iColumns': '10', 'sColumns': '',
            'iDisplayStart': '0', 'iDisplayLength': '200',
            'mDataProp_0': '0', 'mDataProp_1': '1', 'mDataProp_2': '2',
            'mDataProp_3': '3', 'mDataProp_4': '4', 'mDataProp_5': '5',
            'mDataProp_6': '6', 'mDataProp_7': '7', 'mDataProp_8': '8', 'mDataProp_9': '9',
            'sSearch': self.engine.get_full_name,
            'bRegex': 'False',
            'sSearch_0': '', 'bRegex_0': 'False', 'bSearchable_0': 'False',
            'sSearch_1': '', 'bRegex_1': 'False', 'bSearchable_1': 'False',
            'sSearch_2': '', 'bRegex_2': 'False', 'bSearchable_2': 'False',
            'sSearch_3': '', 'bRegex_3': 'False', 'bSearchable_3': 'False',
            'sSearch_4': '', 'bRegex_4': 'False', 'bSearchable_4': 'False',
            'sSearch_5': '', 'bRegex_5': 'False', 'bSearchable_5': 'False',
            'sSearch_6': '', 'bRegex_6': 'False', 'bSearchable_6': 'False',
            'sSearch_7': '', 'bRegex_7': 'False', 'bSearchable_7': 'False',
            'sSearch_8': '', 'bRegex_8': 'False', 'bSearchable_8': 'False',
            'sSearch_9': '', 'bRegex_9': 'False', 'bSearchable_9': 'False',
            'q_ver': 'arbitr', 'date': '~',
            'grecap': self.captcha_code,
            'region': '0', 'court': '0',
            'n_case': '', 'n_proc': '',
            'a': '', 'b': '', 'c': ''
        }

    def build_req_headers(self):
        return {
            'Connection': 'keep-alive',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': self.site_url,
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': f'{self.site_url}/fair/',
            'Accept-Language': 'ru,en;q=0.9',
        }
