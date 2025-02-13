from django.conf import settings
from twocaptcha import TwoCaptcha


def bdr():
    return TwoCaptcha(settings.RECAPTCHA_TOKEN).recaptcha(
        sitekey='6Ld0FP4UAAAAAMvqtSVXfZ5evqA2cZukPQDoHx0d',
        url='https://bdr.mvs.gov.ua/'
    ).get('code')


def court():
    return TwoCaptcha(settings.RECAPTCHA_TOKEN).recaptcha(
        sitekey='6LdIjOQSAAAAAA5VkX2tOq9Znrem2-r_WZi6Jetn',
        url='https://court.gov.ua/fair/'
    ).get('code')


def mvs():
    return TwoCaptcha(settings.RECAPTCHA_TOKEN).recaptcha(
        sitekey='6LdfcW8dAAAAAIwmUkjbhajxEg8nLP2RWb4wD04Z',
        url='https://wanted.mvs.gov.ua/searchperson/'
    ).get('code')


def inactive_doc():
    return TwoCaptcha(settings.RECAPTCHA_TOKEN).recaptcha(
        sitekey='6Lc4HxATAAAAAO7NEm23c-LotBDmKl3ac_dPjGJi',
        url='https://dmsu.gov.ua/services/nd.html'
    ).get('code')


def state_doc():
    return TwoCaptcha(settings.RECAPTCHA_TOKEN).recaptcha(
        sitekey='6Lc4HxATAAAAAO7NEm23c-LotBDmKl3ac_dPjGJi',
        url='https://dmsu.gov.ua/services/docstate.html'
    ).get('code')


def usr_minjust():
    return TwoCaptcha(settings.RECAPTCHA_TOKEN).recaptcha(
        sitekey='6LdStXoUAAAAAE2oEyZLHgu3dBE-WV1zOvZon7_v',
        url='https://usr.minjust.gov.ua/content/free-search'
    ).get('code')