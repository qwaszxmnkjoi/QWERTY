import time
from datetime import datetime

from celery.result import AsyncResult
from django.utils import timezone
from loguru import logger
from requests_html import HTML, HTMLSession

from Emigrant.celery import celery_app as app
from tbot.messages import Messages
from . import captcha
from .enums import State
from .models import (
    AsvpElem,
    Bdr, BdrElement, SavedSearch,
    Court, CourtElement, CourtAssignment, AssignmentElem,
    Debtors, DebtorsElem, DocState, InactiveDocument,
    Mvs, Search, User, Departure
)
from .parsers import BdrScrapper, CourtFairScrapper, CourtAssignScrapper


@app.task(name='check_user_subs')
def check_user_subs():
    users = User.objects.filter(role='expert', subs_id=None,
                                date_end__lte=timezone.now())
    users.update(role='client')


@app.task(name='scrap_bdr')
def scrap_fines(plate: str = 'АХ8028КЕ', document: str = 'Ррв157324',
                chat_id: int = 1, send=False, bdr_id=False):
    user, _ = User.objects.get_or_create(chat_id=chat_id)
    saved = SavedSearch.objects.filter(saved_data=document.split(), user=user, state=State.BDR.as_str).first()
    if bdr_id:
        engine = Bdr.objects.get(id=bdr_id)
    else:
        engine, _ = Bdr.objects.get_or_create(user_id=user.id, plate=plate if not saved else saved.saved_data[0],
                                              document=document if not saved else saved.saved_data[1], status=False)

    if not saved:
        Messages.MonitoringSaveSearch.send_if_active(
            chat_id,
            set_state='',
            format_keyboard_map={'search_id': State.BDR.as_num, 'obj_id': engine.id}
        )

    scrapper = BdrScrapper(engine=engine)
    resp = scrapper.scrap()

    if resp.html.find('.item-list-empty', first=True):
        if send:
            Messages.FinesResultNotFound.send_if_active(chat_id)
        logger.debug('Not Found Elem')
    else:
        # result_items = []

        items = resp.html.find('.item-list > .item')
        urls = resp.html.find('.item-list > .button')

        count_add = 0
        count_upd = 0

        for idx, item in enumerate(items):
            param = item.find('.params', first=True)

            ele, add = BdrElement.objects.update_or_create(
                number=urls[idx].attrs['href'].replace('/user/resolution/', '').replace('/', ''),
                bdr_id=engine.id,
                defaults={
                    'link': next(iter(urls[idx].absolute_links), None),
                    'date': datetime.strptime(
                        param.find('.resolution-datetime', first=True).text,
                        '%d.%m.%Y'
                    ).date(),
                    'pay': True if 'paid' in item.attrs['class'] else False,
                    'amount': float(param.find('.amount', first=True).text.replace(u'\xa0', '').replace(' грн', '')),
                    'description': param.find('.descr', first=True).text
                }
            )

            if send:
                Messages.FinesResult.send_if_active(
                    chat_id,
                    format_map={'car_number': engine.plate,
                                'resolution': ele.number,
                                'date': ele.date.strftime('%d.%m.%Y'),
                                'value': ele.amount,
                                'payment': '✅' if ele.pay else '❌'
                                },
                    format_keyboard_map={'url_view': ele.link}
                    # custom_markup=None
                )

            if add:
                if bdr_id:
                    Messages.FinesResult.send_if_active(
                        chat_id,
                        format_map={'car_number': engine.plate,
                                    'resolution': ele.number,
                                    'date': ele.date.strftime('%d.%m.%Y'),
                                    'value': ele.amount,
                                    'payment': '✅' if ele.pay else '❌'
                                    },
                        format_keyboard_map={'url_view': ele.link}
                        # custom_markup=None
                    )
                count_add += 1
            else:
                count_upd += 1

        logger.debug(f'Add {count_add} and {count_upd} update Fine/s')

    if send:
        Messages.FinesSubscribe.send_if_active(
            chat_id, format_map={'car_number': engine.plate},
            format_keyboard_map={'bdr_id': engine.id}
        )

    return engine.id


@app.task(name='scrap_court')
def scrap_court(search_id: int = 1, send_message: bool = False, mes_id: int = 1):
    try:
        search = Search.objects.get(id=search_id)
        if send_message:
            saved = SavedSearch.objects.filter(saved_data=search.get_full_name.split(), user=search.user, state=State.COURT.as_str).exists()
            try:
                Messages.MonitoringStart.send_if_active(
                    search.user.chat_id, reply_to_message_id=mes_id,
                    set_state=''
                )
            except Exception as e:
                if 'replied message not found' in str(e):
                    Messages.MonitoringStart.send_if_active(
                        search.user.chat_id, set_state=''
                    )
                    mes_id = None
                else:
                    logger.debug(e)
            if not saved:
                Messages.MonitoringSaveSearch.send_if_active(
                    search.user.chat_id, reply_to_message_id=mes_id,
                    set_state='',
                    format_keyboard_map={'search_id': State.DEBTORS.as_num, 'obj_id': search_id}
                )

        scrapper = CourtFairScrapper(search)
        resp = scrapper.scrap_as_json()

        if resp.get('success') is False or len(resp.get('aaData') or []) < 1:
            result = None
        else:
            i = 0
            count_court = 0
            result_new = 0
            result_upd = 0
            for case in resp['aaData']:
                html = HTML(html=case['1'])
                court, add = Court.objects.get_or_create(
                    search=search,
                    number=html.find('input[name=CaseNumber]', first=True).attrs['value'],
                    code=html.find('input[name=UserCourtCode]', first=True).attrs['value'],
                    court=case['0'],
                    claimant=case['5'],
                    date=datetime.strptime(case['7'], '%d.%m.%Y').date()
                )
                if add:
                    count_court += 1

                new, upd = check_court_result(court)

                result_new += new
                result_upd += upd

                i += 1
                if i == 20:
                    break
            logger.debug(f'ADD {count_court} court/s, ADD {result_new} update {result_upd} Result/s')
            result = count_court
        if send_message:
            if result:
                Messages.CourtDetailSearch.send_if_active(
                    search.user.chat_id,
                    format_map={
                        'full_name': search.get_full_name,
                        'count': result
                    },
                    add_user_data={'search_id': search_id},
                    set_state='court_view'
                )
            else:
                Messages.NationalNotFound.send_if_active(
                    search.user.chat_id, format_map={
                        'full_name': search.get_full_name
                    })
    except Search.DoesNotExist:
        return f'Search Request id {search_id} Not Found'


@app.task(name='scrap_court_assign')
def scrap_court_assign(search_id: int = 1, send_message: bool = False, mes_id: int = 1):
    search = Search.objects.filter(id=search_id).first()
    if search:
        if send_message:
            saved = SavedSearch.objects.filter(saved_data=search.get_full_name.split(), user=search.user, state=State.COURT_ASSIGN.as_str).exists()
            try:
                Messages.MonitoringStart.send_if_active(
                    search.user.chat_id, reply_to_message_id=mes_id,
                    set_state=''
                )
            except Exception as e:
                if 'replied message not found' in str(e):
                    Messages.MonitoringStart.send_if_active(
                        search.user.chat_id, set_state=''
                    )
                    mes_id = None
                else:
                    logger.debug(e)
            if not saved:
                Messages.MonitoringSaveSearch.send_if_active(
                    search.user.chat_id, reply_to_message_id=mes_id,
                    set_state='',
                    format_keyboard_map={'search_id': State.COURT_ASSIGN.as_num, 'obj_id': search_id}
                )
        is_next = True
        page = 1
        elements = []
        while is_next:
            scrapper = CourtAssignScrapper(engine=search, page=page)
            data, is_next = scrapper.result_data()
            elements.extend(data)
            page += 1

        if elements:
            court_assign, created = CourtAssignment.objects.get_or_create(search=search)
            elems_db = {
                x.number: x for x in court_assign.assign_elem.all()
            }
            courts = {
                x['rcase']: Court.objects.filter(search=search, number=x['rcase']).first() for x in elements
            }
            to_add, to_update = [], []
            for elem in elements:
                num = elem['rcase']
                a_elem = AssignmentElem(
                    court_assign=court_assign,
                    court=courts.get(num),
                    dt_meet=elem['date'],
                    judges=elem['judges'],
                    number=num,
                    name_court=elem['court'].get('name'),
                    room_court=elem['court'].get('room'),
                    involved=elem['involved'],
                    description=elem['description'],
                    address=elem['address']
                )
                if elem_db := elems_db.get(num):
                    a_elem.pk = elem_db.pk
                    to_update.append(a_elem)
                else:
                    to_add.append(a_elem)

            if to_add:
                AssignmentElem.objects.bulk_create(to_add)
            if to_update:
                AssignmentElem.objects.bulk_update(to_update, fields=[
                    'court_assign', 'court',
                    'dt_meet', 'judges',
                    'number', 'name_court', 'room_court',
                    'involved', 'description',
                    'address'
                ])

            logger.debug(f'Add {len(to_add)} and {len(to_update)} update Assignment/s')

            if send_message:
                Messages.CourtAssignSearch.send_if_active(
                    search.user.chat_id,
                    format_map={
                        'full_name': search.get_full_name,
                        'count': len(elements)
                    },
                    format_keyboard_map={
                        'show_call': 'show_result',
                        'id_sub': court_assign.id,
                    },
                    add_user_data={'assign_id': court_assign.id},
                    set_state='assign_view'
                )
        elif send_message:
            Messages.NationalNotFound.send_if_active(
                search.user.chat_id, format_map={
                    'full_name': search.get_full_name
                })


def check_court_result(court: Court):
    session = HTMLSession()

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89",'
                     ' ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://reyestr.court.gov.ua',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                      ' AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/89.0.4389.114 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                  'image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://reyestr.court.gov.ua/',
        'Accept-Language': 'ru,en;q=0.9',
    }
    data = {
        'SearchExpression': '',
        'UserCourtCode': court.code,
        'ChairmenName': '',
        'RegNumber': '',
        'RegDateBegin': '',
        'RegDateEnd': '',
        'ImportDateBegin': '',
        'ImportDateEnd': '',
        'CaseNumber': court.number,
        'Sort': '1',
        'PagingInfo.ItemsPerPage': '25',
        'Liga': 'true'
    }
    r = session.post(
        url='https://reyestr.court.gov.ua/',
        headers=headers,
        data=data
    )
    table_log = r.html.find('td[class=td1]', first=True).text
    if 'На Ваш запит не знайдено' in str(table_log):
        logger.info('По данному делу еще нет решения')
        return 0, 0
    elif 'виникла помилка' in str(table_log):
        logger.info('Произошла ошибка')
        return 0, 0

    table = r.html.find('div[id=divresult]', first=True)
    trs = table.find('tr')
    if trs and len(trs) > 1:
        count_new = 0
        count_upd = 0
        for tr in trs[1:]:
            # court_name = tr.find('td.CourtName', first=True).text
            elem, add = CourtElement.objects.get_or_create(
                court=court,
                number=tr.find('a.doc_text2', first=True).text,
                defaults={
                    'date_approval': datetime.strptime(
                        tr.find('td.RegDate', first=True).text,
                        '%d.%m.%Y'
                    ),
                    'chairmen': tr.find('td.ChairmenName', first=True).text,
                    'link': 'https://reyestr.court.gov.ua' +
                            tr.find('a.doc_text2', first=True).attrs['href'],
                    'form': tr.find('td.VRType', first=True).text,
                    'court_type': tr.find('td.CSType', first=True).text,
                }
            )
            if add:
                count_new += 1
            else:
                date_approval = datetime.strptime(tr.find('td.RegDate', first=True).text, '%d.%m.%Y')
                chairmen = tr.find('td.ChairmenName', first=True).text
                link = 'https://reyestr.court.gov.ua' + tr.find('a.doc_text2', first=True).attrs['href']
                form = tr.find('td.VRType', first=True).text
                court_type = tr.find('td.CSType', first=True).text
                if elem.date_approval != date_approval.date() or elem.chairmen != chairmen \
                        or elem.link != link or elem.form != form or elem.court_type != court_type:
                    CourtElement.objects.update_or_create(
                        id=elem.id,
                        defaults={
                            'date_approval': date_approval,
                            'chairmen': chairmen,
                            'link': link,
                            'form': form,
                            'court_type': court_type,
                        }
                    )
                    count_upd += 1

        return count_new, count_upd

    else:
        logger.info('Ничего не найдено')
        return 0, 0


@app.task(name='update_result_court')
def update_result_court(court_id: int = 1):
    try:
        court = Court.objects.get(id=court_id)
        new, upd = check_court_result(court)
        if new > 0 or upd > 0:
            Messages.CourtSub.send_if_active(
                court.search.user.chat_id,
                format_map={'number': court.number},
                format_keyboard_map={'subs_id': court.id}
            )
    except Court.DoesNotExist:
        logger.debug(f'Court with id {court_id} DoesNotExist')


@app.task(name='wanted_mws')
def wanted_mws(search_id: int = 1, send_message: bool = False, mes_id: int = 1):
    try:
        search = Search.objects.get(id=search_id)
        session = HTMLSession()
        if send_message:
            saved = SavedSearch.objects.filter(saved_data=search.get_full_name.split(), user=search.user, state=State.WANTED.as_str).exists()
            try:
                Messages.MonitoringStart.send_if_active(
                    search.user.chat_id, reply_to_message_id=mes_id,
                    set_state=''
                )
            except Exception as e:
                if 'replied message not found' in str(e):
                    Messages.MonitoringStart.send_if_active(
                        search.user.chat_id, set_state=''
                    )
                    mes_id = None
                else:
                    logger.debug(e)
            if not saved:
                Messages.MonitoringSaveSearch.send_if_active(
                    search.user.chat_id, reply_to_message_id=mes_id,
                    set_state='',
                    format_keyboard_map={'search_id': State.WANTED.as_num, 'obj_id': search_id}
                )

        ABSOLUTE_LINK = 'https://wanted.mvs.gov.ua'

        data = {
            'PRUFM': search.surname,
            'PRUIM': search.name,
            'PRUOT': search.patronymic,
            'page': 1,
            'g-recaptcha-response': captcha.mvs(),
        }
        count = 0

        while True:
            r = session.get(
                url=ABSOLUTE_LINK + '/searchperson',
                params=data
            )
            if r.status_code == 503:
                break
            content = r.html.find('div.section-content', first=True)
            for person in content.find('a.card'):
                person = session.get(
                    url=next(iter(person.absolute_links), None)
                )
                if person.status_code == 503:
                    break

                info_list = person.html.find('div[class=info-list]',
                                             first=True)

                _, add = Mvs.objects.get_or_create(
                    search=search,
                    photo=ABSOLUTE_LINK + person.html.find('img[class=card-img]', first=True).attrs['src'],
                    region=info_list.find('div[class=info-list-item]:nth-child(2)>div[data=second]', first=True).text,
                    category=info_list.find('div[class=info-list-item]:nth-child(3)>div[data=second]', first=True).text,
                    disappearance=datetime.strptime(
                        info_list.find('div[class=info-list-item]:nth-child(4)>div[data=second]', first=True).text,
                        '%d.%m.%Y'),
                    birth=datetime.strptime(
                        info_list.find('div[class=info-list-item]:nth-child(12)>div[data=second]', first=True).text,
                        '%d.%m.%Y'),
                    accusations=info_list.find('div[class=info-list-item]:nth-child(14)>div[data=second]', first=True).text,
                    precaution=info_list.find('div[class=info-list-item]:nth-child(15)>div[data=second]', first=True).text,
                    link=person.url

                )
                if add:
                    count += 1

            data['page'] += 1
            if 'За вашим запитом не знайдено жодного результату' in content.text:
                break
        if send_message and count:
            Messages.WantedDetailSearch.send_if_active(
                search.user.chat_id,
                format_map={
                    'full_name': search.get_full_name,
                    'count': count
                },
                format_keyboard_map={'show_data': 'show_result'},
                add_user_data={'search_id': search_id},
                set_state='wanted_view'
            )
        elif send_message:
            Messages.NationalNotFound.send_if_active(
                search.user.chat_id, format_map={
                    'full_name': search.get_full_name
                })

        return f'Wanted Mws: New {count}'
    except Search.DoesNotExist:
        return f'Search Request id {search_id} Not Found'


@app.task(name='ScrapWantedById')
def scrap_wanted_by_id(mvs_id: int):
    session = HTMLSession()

    mvs = Mvs.objects.get(id=mvs_id)

    person = session.get(
        url=mvs.link,
    )
    if person.status_code == 200:
        info_list = person.html.find('div[class=info-list]', first=True)

        data = {
            'region': info_list.find('div[class=info-list-item]:nth-child(2)>div[data=second]', first=True).text,
            'category': info_list.find('div[class=info-list-item]:nth-child(3)>div[data=second]', first=True).text,
            'disappearance': datetime.strptime(
                info_list.find('div[class=info-list-item]:nth-child(4)>div[data=second]', first=True).text,
                '%d.%m.%Y'),
            'birth': datetime.strptime(
                info_list.find('div[class=info-list-item]:nth-child(12)>div[data=second]', first=True).text,
                '%d.%m.%Y'),
            'accusations': info_list.find('div[class=info-list-item]:nth-child(14)>div[data=second]', first=True).text,
            'precaution': info_list.find('div[class=info-list-item]:nth-child(15)>div[data=second]', first=True).text
        }

        if mvs.region != data.get('region') or \
                mvs.category != data.get('category') or mvs.disappearance != \
                data.get('disappearance') or mvs.birth != data.get('birth') or \
                mvs.accusations != data.get('accusations') or mvs.precaution != \
                data.get('precaution'):
            mvs, _ = Mvs.objects.update_or_create(
                id=mvs_id,
                region=data.get('region'),
                category=data.get('category'),
                disappearance=data.get('disappearance'),
                birth=data.get('birth'),
                accusations=data.get('accusations'),
                precaution=data.get('precaution')
            )
            Messages.MvsSub.send_if_active(
                mvs.search.user.chat_id,
                format_map={'full_name': mvs.search.get_full_name},
                format_keyboard_map={'subs_id': mvs.id}
            )


@app.task(name='inactive_document')
def inactive_doc(inactive_id: int = 1, mes_id: str = None, send: bool = False, daily: bool = False):
    try:
        obj = InactiveDocument.objects.get(id=inactive_id)
        session = HTMLSession()

        data = {
            'typedoc': obj.type_doc,
            'passportseries': obj.series if obj.series else '',
            'passportnumber': obj.number,
            'goValid': ''
        }

        try:
            data['g-recaptcha-response'] = captcha.inactive_doc()
        except Exception as e:
            logger.warning(f'кажется ошибка с каптчей, пробую снова ({e})')
            data['g-recaptcha-response'] = captcha.inactive_doc()

        r = session.post(
            url='https://dmsu.gov.ua/services/nd.html',
            data=data,
            verify=False
        )
        status = r.html.find('article.service-content-indent')
        if len(status) >= 2:
            status = status[1]
        else:
            logger.debug('Error Parse Status InActive Doc')
            return

        print(status)

        obj.status = True if 'service-result-success' in status.attrs['class'] else False
        desc = '\n'.join([x.text for x in status.find('p')[2:4] if 'Перевірити інший' not in x.text])

        if desc != obj.description and daily:
            Messages.InactiveResult.send_if_active(
                obj.user.chat_id,
                format_map={'status': obj.description},
                format_keyboard_map={'doc_id': obj.id},
            )

        obj.description = desc
        obj.save()

        if send:
            try:
                Messages.InactiveResult.send_if_active(
                    obj.user.chat_id,
                    format_map={'status': obj.description},
                    format_keyboard_map={'doc_id': obj.id},
                    reply_to_message_id=mes_id
                )
            except Exception as e:
                if 'replied message not found' in str(e):
                    Messages.InactiveResult.send_if_active(
                        obj.user.chat_id,
                        format_map={'status': obj.description},
                        format_keyboard_map={'doc_id': obj.id},
                    )
                else:
                    logger.debug(e)

    except InactiveDocument.DoesNotExist:
        return f'InactiveDocument with id {inactive_id} DoesNotExist'


@app.task(name='state_document')
def doc_state(doc_id: int = 1, mes_id: str = None, send: bool = False, daily: bool = False):
    try:
        doc = DocState.objects.get(id=doc_id)

        slug = False
        session = HTMLSession()

        data = {}

        if doc.type_doc == 'id':
            data = {
                'doc-state-type': doc.type_doc,
                'kind': doc.type_doc,
                'sdInputDoc_Type_Id': doc.doc_type_id
            }
            slug = 'Id'
        elif doc.type_doc == 'zp':
            data = {
                'doc-state-type': doc.type_doc,
                'kind': doc.type_doc,
                'sdFor_X': 0,
                'sdFor_Zp': doc.for_doc,
                'sdInputDoc_Type_Zp': doc.doc_type_id,
            }
            slug = 'Zp'
        elif doc.type_doc == 'tt':
            data = {
                'doc-state-type': doc.type_doc,
                'kind': doc.type_doc,
                'sdFor_X': 0,
                'sdFor_Zp': doc.for_doc,
                'sdInputDoc_Type_Zp': 1,
                'sdInputDoc_Number_X': doc.number
            }
        elif doc.type_doc == 'tp':
            data = {
                'doc-state-type': doc.type_doc,
                'kind': doc.type_doc,
                'sdFor_X': 0,
                'sdFor_Zp': doc.for_doc,
                'sdInputDoc_Number_X': doc.number
            }
        elif doc.type_doc == 'dd' or doc.type_doc == 'pp':
            data = {
                'doc-state-type': doc.type_doc,
                'kind': doc.type_doc,
                'sdFor_X': 0,
                'sdInputDoc_Number_X': doc.number
            }
        if slug:
            if doc.register_doc == 'book':
                data[f'sdInputDoc_SeriesBook_{slug}'] = doc.series
                data[f'sdInputDoc_NumberBook_{slug}'] = doc.number
            elif doc.register_doc == 'id':
                data[f'sdInputDoc_NumberId_{slug}'] = doc.number
            elif doc.register_doc == 'cert':
                data[f'sdInputDoc_SeriesSv_{slug}'] = doc.series
                data[f'sdInputDoc_NumberSv_{slug}'] = doc.number

        try:
            data['g-recaptcha-response'] = captcha.state_doc()
        except Exception as e:
            logger.warning(f'кажется ошибка с каптчей, пробую снова ({e})')
            data['g-recaptcha-response'] = captcha.state_doc()

        r = session.post(
            url='https://dmsu.gov.ua/services/docstate/rezultat.html',
            data=data
        )

        status = r.html.find('.service-section  .service-content-indent')[-1]

        if doc.description != status.text and daily:
            Messages.DocumentsResult.send_if_active(
                doc.user.chat_id,
                format_map={'status': doc.description},
                format_keyboard_map={'doc_id': doc.id},
            )
        doc.description = status.text
        doc.save()

        if send:
            try:
                Messages.DocumentsResult.send_if_active(
                    doc.user.chat_id, format_map={'status': doc.description},
                    format_keyboard_map={'doc_id': doc.id},
                    reply_to_message_id=mes_id
                )
            except Exception as e:
                if 'replied message not found' in str(e):
                    Messages.DocumentsResult.send_if_active(
                        doc.user.chat_id,
                        format_map={'status': doc.description},
                        format_keyboard_map={'doc_id': doc.id},
                    )
                else:
                    logger.debug(e)
    except DocState.DoesNotExist:
        return f'DocState with id {doc_id} DoesNotExist'


@app.task(name='DebtorsParsing')
def scrap_debtors(debtors_id: int = 1, send_message: bool = False, mes_id: int = 1, is_update: bool = False):
    try:
        debtors = Debtors.objects.get(id=debtors_id)
        session = HTMLSession()
        if send_message and not is_update:
            saved = SavedSearch.objects.filter(saved_data=debtors.search.get_full_name.split(), user=debtors.search.user, state=State.DEBTORS.as_str).exists()
            try:
                Messages.MonitoringStart.send_if_active(
                    debtors.search.user.chat_id, reply_to_message_id=mes_id,
                    set_state=''
                )
            except Exception as e:
                if 'replied message not found' in str(e):
                    Messages.MonitoringStart.send_if_active(
                        debtors.search.user.chat_id, set_state=''
                    )
                    mes_id = None
                else:
                    logger.debug(e)
            if not saved:
                Messages.MonitoringSaveSearch.send_if_active(
                    debtors.search.user.chat_id, reply_to_message_id=mes_id,
                    set_state='',
                    format_keyboard_map={'search_id': State.DEBTORS.as_num, 'obj_id': debtors.search.id}
                )

        rm = session.post(
            url='https://erb.minjust.gov.ua/listDebtorsEndpoint',
            json={
                "searchType": "1",
                "paging": "1",
                "filter": {
                    "LastName": debtors.search.surname,
                    "FirstName": debtors.search.name,
                    "MiddleName": debtors.search.patronymic,
                    "BirthDate": None,
                    "IdentCode": "",
                    "categoryCode": ""
                }
            }).json()

        if len(rm.get('results')) < 1:
            if send_message:
                Messages.NationalNotFound.send_if_active(
                    debtors.search.user.chat_id, format_map={
                        'full_name': debtors.search.get_full_name
                    })
            logger.info(
                f'Должники по запросу {debtors.search.get_full_name}: в базе отсутствует'
            )
            return True
        else:
            count_new = 0
            for debt in rm['results']:
                connection = '{}\n{}\n{}\nphone: {}\nemail: {}'.format(
                    debt.get('departmentName', ''),
                    debt.get('departmentPhone', ''),
                    debt.get('executor', ''), debt.get('executorPhone', ''),
                    debt.get('executorEmail', '-')
                )
                debt_elem, created = DebtorsElem.objects.update_or_create(
                    debtors=debtors, number=debt.get('vpNum'),
                    defaults={
                        'publisher': debt.get('publisher'),
                        'connection': connection,
                        'deduction': debt.get('deductionType'),
                        'birth': datetime.strptime(debt['birthDate'], '%Y-%m-%dT%H:%M:%SZ').date()
                    }
                )
                if created:
                    count_new += 1
            if send_message and count_new:
                Messages.DebtorsDetailSearch.send_if_active(
                    debtors.search.user.chat_id,
                    format_map={
                        'full_name': debtors.search.get_full_name,
                        'count': count_new
                    },
                    format_keyboard_map={'show_data': 'show_result',
                                         'deb_id': debtors_id if not debtors.subscribe else None, 'subs_id': debtors_id if debtors.subscribe else None},
                    add_user_data={'debtors_id': debtors_id},
                    set_state='debtors_view'
                )
            return
    except Debtors.DoesNotExist:
        return f'Debtors with id {debtors_id} DoesNotExist'


@app.task(name='AsvpParsing')
def scrap_asvp(search_id: int = 1, send_message: bool = False, mes_id: int = 1):
    try:
        search = Search.objects.get(id=search_id)
        if send_message:
            saved = SavedSearch.objects.filter(saved_data=search.get_full_name.split(), user=search.user, state=State.ASVP.as_str).exists()
            try:
                Messages.MonitoringStart.send_if_active(
                    search.user.chat_id, reply_to_message_id=mes_id,
                    set_state=''
                )
            except Exception as e:
                if 'replied message not found' in str(e):
                    Messages.MonitoringStart.send_if_active(
                        search.user.chat_id, set_state=''
                    )
                    mes_id = None
                else:
                    logger.debug(e)
            if not saved:
                Messages.MonitoringSaveSearch.send_if_active(
                    search.user.chat_id, reply_to_message_id=mes_id,
                    set_state='',
                    format_keyboard_map={'search_id': State.ASVP.as_num, 'obj_id': search_id}
                )
        count_new = search_asvp(surname=search.surname or '', name=search.name or '', patronymic=search.patronymic or '', search_id=search_id)
        if send_message:
            if count_new:
                Messages.AsvpDetailSearch.send_if_active(
                    search.user.chat_id,
                    format_map={
                        'full_name': search.get_full_name,
                        'count': count_new
                    },
                    format_keyboard_map={'show_data': 'show_result'},
                    add_user_data={'search_id': search_id},
                    set_state='asvp_view'
                )
            else:
                Messages.NationalNotFound.send_if_active(
                    search.user.chat_id, format_map={
                        'full_name': search.get_full_name
                    })
    except Search.DoesNotExist:
        return f'Search Request id {search_id} Not Found'


@app.task(name='search_asvp')
def search_asvp_by_id(asvp_id: int):
    asvp = AsvpElem.objects.get(id=asvp_id)
    session = HTMLSession()

    req = session.post(
        url='https://asvpweb.minjust.gov.ua/listDebtCredVPEndpoint',
        json={
            "searchType": "11",
            "paging": "1",
            "filter": {
                "VPNum": asvp.number,
                "vpOpenFrom": None,
                "vpOpenTo": None,
                "debtFilter": {
                    "LastName": "",
                    "FirstName": "",
                    "MiddleName": "",
                    "BirthDate": None
                },
                "creditFilter": {
                    "LastName": "",
                    "FirstName": "",
                    "MiddleName": "",
                }
            }
        }
    ).json()
    if len(req.get('results')) < 1:
        return
    else:
        result = req['results'][0]
        if asvp.status != result.get('mi_wfStateWithError') or \
                asvp.creditors_name != result.get('creditors')[0].get('name'):
            asvp.status = result.get('mi_wfStateWithError')
            asvp.creditors_name = result.get('creditors')[0].get('name')
            asvp.save()
            Messages.AsvpSub.send_if_active(
                asvp.debtors.debtors.search.user.chat_id,
                format_map={'number': asvp.debtors.number},
                format_keyboard_map={'subs_id': asvp.id}
            )


def search_asvp(vp_num: str = '', surname: str = '', name: str = '',
                patronymic: str = '', birth: datetime = None,
                search_id: int = 1):
    session = HTMLSession()

    req = session.post(
        url='https://asvpweb.minjust.gov.ua/listDebtCredVPEndpoint',
        json={
            "searchType": "11",
            "paging": "1",
            "filter": {
                "VPNum": vp_num,
                "vpOpenFrom": None,
                "vpOpenTo": None,
                "debtFilter": {
                    "LastName": surname,
                    "FirstName": name,
                    "MiddleName": patronymic,
                    "BirthDate": str(birth.strftime('%Y-%m-%dT%H:%M:%SZ')) if birth else None
                },
                "creditFilter": {
                    "LastName": "",
                    "FirstName": "",
                    "MiddleName": "",
                }
            }
        }
    ).json()

    count_asvp = 0

    if len(req.get('results')) < 1:
        return count_asvp
    else:
        for asvp in req['results']:
            debtor = asvp.get('debtors', [{}])[0]
            elem, created = AsvpElem.objects.update_or_create(
                search_id=search_id, number=asvp.get('orderNum'),
                defaults={
                    'agency_edrpou': asvp.get('depEdrpou'),
                    'agency': asvp.get('depStr'),
                    'debtors': f'{debtor.get("lastName", "")} {debtor.get("firstName", "")} {debtor.get("middleName", "")}',
                    'birth': datetime.strptime(debtor['birthDate'], '%Y-%m-%dT%H:%M:%SZ').date() if debtor.get('birthDate') else None,
                    'date_open': datetime.strptime(asvp['beginDate'], '%Y-%m-%dT%H:%M:%SZ').date() if asvp.get('beginDate') else datetime.strptime('1990-10-10', '%Y-%m-%d').date(),
                    'creditors_name': asvp.get('creditors')[0].get('name'),
                    'status': asvp.get('mi_wfStateWithError')
                }
            )
            if created:
                count_asvp += 1
        return count_asvp


@app.task(name='process_depart')
def process_depart(depart_id: int = 1):
    try:
        depart = Departure.objects.get(id=depart_id)
        all_days = 0

        for elem in depart.dep_elem.all():
            if elem.date_of_departure:
                date_of_departure = elem.date_of_departure
            else:
                date_of_departure = timezone.now()

            all_days += (date_of_departure - elem.date_of_entry).days

        left_days = 90 - all_days

        depart.days = left_days
        depart.save()

        if depart.dep_elem.last().date_of_departure is None:
            if left_days == 20:
                Messages.DepartTwenty.send_if_active(depart.user.chat_id)
            elif left_days == 0:
                Messages.DepartDeparture.send_if_active(depart.user.chat_id)

    except Departure.DoesNotExist:
        logger.debug(f'Departure with id {depart_id} DoesNotExist')


@app.task(name='NationalParsing')
def national_parsing(search_id: int = 1, new_send: bool = False, mes_id: int = 1):
    try:
        search = Search.objects.get(id=search_id)
        saved = SavedSearch.objects.filter(saved_data=search.get_full_name.split(), user=search.user, state=State.NATIONAL.as_str).exists()
        try:
            Messages.MonitoringStart.send_if_active(
                search.user.chat_id, reply_to_message_id=mes_id,
                set_state=''
            )
        except Exception as e:
            if 'replied message not found' in str(e):
                Messages.MonitoringStart.send_if_active(
                    search.user.chat_id, set_state=''
                )
                mes_id = None
            else:
                logger.debug(e)
        if not saved:
            Messages.MonitoringSaveSearch.send_if_active(
                search.user.chat_id, reply_to_message_id=mes_id,
                set_state='',
                format_keyboard_map={'search_id': State.NATIONAL.as_num, 'obj_id': search_id}
            )
        debt, _ = Debtors.objects.get_or_create(search=search)
        court_assign, created = CourtAssignment.objects.get_or_create(search=search)

        assign = scrap_court_assign.apply_async(args=[search.id])
        court = scrap_court.apply_async(args=[search.id])
        mvs = wanted_mws.apply_async(args=[search.id])
        debtors = scrap_debtors.apply_async(args=[debt.id])
        asvp = scrap_asvp.apply_async(args=[search.id])

        i = 0

        while True:
            if AsyncResult(court.id).status == 'SUCCESS' \
                    and AsyncResult(mvs.id).status == 'SUCCESS' \
                    and AsyncResult(assign.id).status == 'SUCCESS' \
                    and AsyncResult(asvp.id).status == 'SUCCESS' \
                    and AsyncResult(debtors.id).status == 'SUCCESS':
                break
            else:
                if i == 20:
                    try:
                        Messages.MonitoringInProgress.send_if_active(
                            search.user.chat_id, reply_to_message_id=mes_id
                        )
                    except Exception as e:
                        logger.info(e)
                        if 'replied message not found' in str(e):
                            Messages.MonitoringInProgress.send_if_active(
                                search.user.chat_id
                            )
                        else:
                            logger.debug(e)
                elif i == 60:
                    try:
                        Messages.MonitoringIsDelayed.send_if_active(
                            search.user.chat_id, reply_to_message_id=mes_id
                        )
                    except Exception as e:
                        logger.info(e)
                        if 'replied message not found' in str(e):
                            Messages.MonitoringIsDelayed.send_if_active(
                                search.user.chat_id
                            )
                        else:
                            logger.debug(e)
                time.sleep(1)
                i += 1
                continue

        court_count = search.court.count()
        assign_count = court_assign.assign_elem.count()
        mvs_count = search.mvs.count()
        debt_count = debt.debtors_elem.count()
        asvp_count = search.asvp_elem.count()
        if court_count or mvs_count or debt_count or asvp_count or assign_count:
            Messages.NationalResult.send_if_active(
                search.user.chat_id,
                format_map={
                    'full_name': search.get_full_name,

                    'court_count': court_count,
                    'court_assign_count': assign_count,
                    'court_assign': f'(/court_assign_{court_assign.id})' if assign_count >= 1 else '',
                    'court': f'(/court_{search.id})' if court_count >= 1 else '',
                    'mvs_count': mvs_count,
                    'mvs': f'(/wanted_{search.id})' if mvs_count >= 1 else '',
                    'debtors_count': debt_count,
                    'debtors': f'(/debtors_{debt.id})' if debt_count >= 1 else '',
                    'asvp_count': asvp_count,
                    'asvp': f'(/asvp_{search.id})' if asvp_count >= 1 else ''
                }
            )
            Messages.NationalResultSubs.send_if_active(
                search.user.chat_id,
                format_map={
                    'full_name': search.get_full_name
                },
                format_keyboard_map={'search_id': search.id}
            )
        else:
            Messages.NationalNotFound.send_if_active(
                search.user.chat_id, format_map={
                    'full_name': search.get_full_name
                })

    except Search.DoesNotExist:
        return f'Search with id {search_id} DoesNotExist'


@app.task(name='scrap_subs')
def scrap_subscription():
    fines = Bdr.objects.filter(status=True).exclude(user__role='client')
    for fine in fines:
        scrap_fines.apply_async(args=['', '', fine.user.chat_id, False, fine.id])

    docs = DocState.objects.filter(subscribe=True).exclude(user__role='client')
    for doc in docs:
        doc_state.apply_async(args=[doc.id, None, False, True])

    inactive = InactiveDocument.objects.filter(subscribe=True).exclude(user__role='client')
    for obj in inactive:
        inactive_doc.apply_async(args=[obj.id, None, False, True])

    depart = Departure.objects.filter(subscribe=True).exclude(user__role='client')
    for dep in depart:
        process_depart.apply_async(args=[dep.id])

    courts = Court.objects.filter(subscribe=True).exclude(search__user__role='client')
    for court in courts:
        update_result_court.apply_async(args=[court.id])

    wanted = Mvs.objects.filter(subscribe=True).exclude(search__user__role='client')
    for mvs in wanted:
        scrap_wanted_by_id.apply_async(args=[mvs.id])

    asvp_elems = AsvpElem.objects.filter(subscribe=True).exclude(search__user__role='client')
    for asvp in asvp_elems:
        search_asvp_by_id.apply_async(args=[asvp.id])

    debt_ids = set(Debtors.objects.filter(subscribe=True).exclude(search__user__role='client').values_list('id', flat=True))
    for debt_id in debt_ids:
        # debtors_id: int = 1, asvp_search: bool = True, send_message: bool = False, mes_id: int = 1, is_update: bool = False
        scrap_debtors.apply_async(
            kwargs={'debtors_id': debt_id, 'send_message': True, 'is_update': True},
        )
