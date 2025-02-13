import typing
from datetime import datetime

from customer.models import Search
from ..base import ScrapperBase


class CourtAssignScrapper(ScrapperBase):
    site_url = 'https://court.gov.ua'
    site_key = '6LdIjOQSAAAAAA5VkX2tOq9Znrem2-r_WZi6Jetn'

    method = 'post'

    def __init__(self, engine: Search, page: int, **kwargs):
        self.engine = engine
        self.page = page
        super().__init__(**kwargs)

    def build_req_url(self):
        return f'{self.site_url}/main_assignments.php'

    def build_captcha(self, raise_exception: bool = False):
        return ''

    def build_req_data(self):
        return {
            'page': self.page,
            'search': self.engine.get_full_name,
            'g-recaptcha-response': self.captcha_code
        }

    def build_req_headers(self):
        return {
            'Connection': 'keep-alive',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': self.site_url,
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': f'{self.site_url}/assignments/',
            'Accept-Language': 'en,ru;q=0.9,ru-UA;q=0.8,ru-RU;q=0.7,en-US;q=0.6,uk;q=0.5',
        }

    def result_data(self) -> typing.Tuple[typing.List[typing.Dict[str, typing.Any]], bool]:
        result = []
        is_next = False
        html = self.scrap_as_html()
        meetings = html.find('tr.assignment-table__tr')
        if meetings:
            dsb = not html.find('button.assignment-tb-top__btn:last-child', first=True).attrs.get('disabled', True)
            is_next = not dsb
            for meet in meetings:
                date = meet.find('.meeting_date', first=True).text
                meeting_court = meet.find('.meeting_court')
                result.append({
                    'id': int(meet.attrs.get('id', '').replace('meeting_', '') or 0),
                    'date': datetime.strptime(date, '%d.%m.%Y %H:%M').replace(tzinfo=self.dt_tz) if date else None,
                    'judges': meet.find('.meeting_judges', first=True).text,
                    'rcase': meet.find('.meeting_rcase', first=True).text,
                    'court': {
                        'name': meeting_court[0].text if meeting_court else None,
                        'room': meeting_court[1].text if len(meeting_court) >= 2 else None
                    },
                    'involved': meet.find('.meeting_involved', first=True).text,
                    'description': meet.find('.meeting_description', first=True).text,
                    'address': meet.find('.meeting_description:last-child', first=True).text,
                })

        return result, is_next
