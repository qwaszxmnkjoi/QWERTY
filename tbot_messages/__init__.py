# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import django

__author__ = 'Daniil Marchenko'
__version__ = '0.1.2'

if django.VERSION < (3, 2):
    default_app_config = 'tbot_messages.apps.TbotMessagesConfig'

VERSION = __version__
