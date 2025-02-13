translate = {
    'Start': {
        'text': 'Привет',
        'text_en': 'Hello',
        'text_ua': 'Вітаю! Це бот-помічник для іноземців в Україні.'
                   ' З ним легко:'
                   '\n\n👉 отримувати інформацію з державних реєстрів'
                   '\n\n👉 спілкуватись з іншими іноземцями, щоб ділитись '
                   'досвідом перебування в Україні.'
                   '\n\n👉 бути в курсі новин які стосуються митного та'
                   ' міграційного законодавства.'
                   '\n\n👉 всі підписники бота мають можливість користуватись'
                   ' послугами',
    },
    'Language': {
        'text': 'Выбери язык бота\nChoose language bot\nОберіть мову',
        'text_en': 'Choose language bot\nВыбери язык бота\nОберіть мову',
        'text_ua': 'Оберіть мову\nВыбери язык бота\nChoose language bot',
        'buttons': [
            {'text': '🇷🇺РУС', 'text_en': '🇷🇺RUS', 'text_ua': '🇷🇺РОС',
             'row': 0, 'callback_data': 'language#ru'},
            {'text': '🇺🇦УКР', 'text_en': '🇺🇦UA', 'text_ua': '🇺🇦УКР',
             'row': 0, 'callback_data': 'language#ua'},
            {'text': '🇬🇧АНГЛ', 'text_en': '🇬🇧ENG', 'text_ua': '🇬🇧АНГЛ',
             'row': 0, 'callback_data': 'language#en'},
        ]
    },
    'Menu': {
        'text': 'Меню',
        'text_en': 'MENU',
        'text_ua': '🔍 Для перевірки інформації з держаних реєстрів натисніть'
                   ' на "Моніторинг".'
                   '\n\n🙎‍♂ Для налаштування персональних даних, підписки,'
                   ' а також для зв\'язку з персональним асистентом '
                   'перейдіть в "Кабінет".'
                   '\n\n📰 В меню "Новини" зібрана інформація по останнім'
                   ' подіям чи змінам в сфері міграційної політики'
                   ' та законодавства.'
                   '\n\n💬 Ви можете спілкуватись в груповому чаті з земляками'
                   ' та іншими іноземцями які перебувають в Україні.'
                   ' Для цього перейдіть в "Чат"'
                   '\n\n🇺🇦 Інформація про правила та процедури пов\'язані з '
                   'міграційним законодавством України Ви зможете переглянути'
                   ' в меню "Міграція"'
                   '\n\n⚠️ Для отримання допомоги спеціаліста у розв\'язанні'
                   ' організаційних питань скористайтесь меню "Консультант".'
                   ' А для вирішення технічних проблем натисніть'
                   ' на "Тех. підтримка".'
                   '\n\nℹ️ Інформація про Global guide service перегляньте'
                   ' в меню "Про нас"'
                   '\n\n🛂 Основні правила та положення міграційного'
                   ' та прикордонного контролю, а також інформацію'
                   ' про порядок заборони на в\'їзд та депортації Ви можете '
                   'знайти у відповідних кнопках головного меню меню'
                   '\n\nВи можете змінити мову чат-бота ввівши'
                   ' команду /language.',
        'buttons': [
            {'text': 'Мониторинг', 'text_en': 'Monitoring', 'text_ua':
                'Моніторинг', 'row': 0, 'reply': True},
            {'text': 'Новости', 'text_en': 'News', 'text_ua': 'Новини',
             'row': 0, 'reply': True},
            {'text': 'Чат', 'text_en': 'Chat', 'text_ua': 'Чат',
             'row': 1, 'reply': True},
            {'text': 'Миграция', 'text_en': 'Migration', 'text_ua': 'Міграція',
             'row': 1, 'reply': True},
            {'text': 'Тех. Поддержка', 'text_en': 'Support', 'text_ua':
                'Тех. підтримка', 'row': 2, 'reply': True},
            {'text': 'Кабинет', 'text_en': 'Cabinet', 'text_ua': 'Кабінет',
             'row': 2, 'reply': True},
            {'text': 'Пересечение границы Украины',
             'text_en': 'Crossing the border of Ukraine',
             'text_ua': 'Перетин кордону України', 'row': 3, 'reply': True},
        ],
    },
    'NotFoundNews': {
        'text': 'Новостей нет.',
        'text_en': 'News not found.',
        'text_ua': 'Новин немає. ',
        'buttons': [
            {
                'text': '🚫 Отписаться от оповещений',
                'text_en': '🚫 Unsubscribe from notifications',
                'text_ua': '🚫 Відписатись від сповіщень',
                'row': 0,
                'reply': True
            },
            {
                'text': 'Меню',
                'text_en': 'Menu',
                'text_ua': 'Меню',
                'row': 0,
                'reply': True
            }
        ]
    },
    'NotFoundNewsUnsubscribe': {
        'text': 'Новостей нет.',
        'text_en': 'News not found.',
        'text_ua': 'Новин немає. ',
        'buttons': [
            {
                'text': '✅ Подписаться на оповещения',
                'text_en': '✅ Subscribe to notification',
                'text_ua': '✅ Підписатись на сповіщення',
                'row': 0,
                'reply': True
            },
            {
                'text': 'Меню',
                'text_en': 'Menu',
                'text_ua': 'Меню',
                'row': 0,
                'reply': True
            }
        ]
    },
    'DetailNews': {
        'text': '{description}',
        'text_en': '{description}',
        'text_ua': '{description}',
        'buttons': [
            {
                'text': '↩️ Назад',
                'text_en': '↩️ Back',
                'text_ua': '↩️ Назад',
                'row': 0,
                'reply': True
            },
            {
                'text': 'Меню',
                'text_en': 'Menu',
                'text_ua': 'Меню',
                'row': 0,
                'reply': True
            }
        ]
    },
    'Subscribe': {
        'text': 'Вы подписались на получение уведомлений с новостями.',
        'text_en': 'You have subscribed to receive news notifications.',
        'text_ua': 'Ви підписались на отримання сповіщень з новинами.',
        'buttons': [
            {
                'text': '🚫 Отписаться от оповещений',
                'text_en': '🚫 Unsubscribe from notifications',
                'text_ua': '🚫 Відписатись від сповіщень',
                'row': 0,
                'reply': True
            },
            {
                'text': 'Меню',
                'text_en': 'Menu',
                'text_ua': 'Меню',
                'row': 0,
                'reply': True
            }
        ]
    },
    'Unsubscribe': {
        'text': 'Вы отписались от получения уведомлений с новостями.',
        'text_en': 'You have unsubscribed from receiving news'
                   ' notifications',
        'text_ua': 'Ви відписались від отримання сповіщень з новинами.',
        'buttons': [
            {
                'text': '✅ Подписаться на оповещения',
                'text_en': '✅ Subscribe to notification',
                'text_ua': '✅ Підписатись на сповіщення',
                'row': 0,
                'reply': True
            },
            {
                'text': 'Меню',
                'text_en': 'Menu',
                'text_ua': 'Меню',
                'row': 0,
                'reply': True
            }
        ]
    },
    'News': {
        'text': '{description}',
        'text_en': '{description}',
        'text_ua': '{description}',
        'buttons': [
            {
                'text': 'Просмотреть',
                'text_en': 'show',
                'text_ua': 'Переглянути',
                'row': 0,
                'callback_data': 'get_news#{news_id}'
            }
        ]
    },
    'NewsTitle': {
        'text': '<b>{title}</b>',
        'text_en': '<b>{title}</b>',
        'text_ua': '<b>{title}</b>',
        'buttons': [
            {
                'text': '🚫 Отписаться от оповещений',
                'text_en': '🚫 Unsubscribe from notifications',
                'text_ua': '🚫 Відписатись від сповіщень',
                'row': 0,
                'reply': True
            },
            {
                'text': 'Меню',
                'text_en': 'Menu',
                'text_ua': 'Меню',
                'row': 0,
                'reply': True
            }
        ]
    },
    'NewsTitleUnsub': {
        'text': '{title}',
        'text_en': '{title}',
        'text_ua': '{title}',
        'buttons': [
            {
                'text': '✅ Подписаться на оповещения',
                'text_en': '✅ Subscribe to notification',
                'text_ua': '✅ Підписатись на сповіщення',
                'row': 0,
                'reply': True
            },
            {
                'text': 'Меню',
                'text_en': 'Menu',
                'text_ua': 'Меню',
                'row': 0,
                'reply': True
            }
        ]
    },
    'NewsShowMore': {
        'text': 'Показано {current} из {total}',
        'text_en': 'Show {current} from {total}',
        'text_ua': 'Показано {current} з {total}',
        'buttons': [
            {
                'text': 'Показать еще {next_count}',
                'text_en': 'Show more {next_count}',
                'text_ua': 'Показати ще {next_count}',
                'row': 0,
                'callback_data': 'news#{page}'
            }
        ]
    },
    'NewsSendTitle': {
        'text': '<b>{title}</b>',
        'text_en': '<b>{title}</b>',
        'text_ua': '<b>{title}</b>',
        'buttons': [
            {
                'text': '🚫 Отписаться от оповещений',
                'text_en': '🚫 Unsubscribe from notifications',
                'text_ua': '🚫 Відписатись від сповіщень',
                'row': 0,
                'reply': True
            },
            {
                'text': 'Меню',
                'text_en': 'Menu',
                'text_ua': 'Меню',
                'row': 0,
                'reply': True
            },
            {
                'text': 'Все новости',
                'text_en': 'All News',
                'text_ua': 'Усі Новини',
                'row': 0,
                'reply': True
            },
        ]
    },
    'NewsSendDetail': {
        'text': '{description}',
        'text_en': '{description}',
        'text_ua': '{description}',
        'buttons': [
            {
                'text': '↩️ Назад',
                'text_en': '↩️ Back',
                'text_ua': '↩️ Назад',
                'row': 0,
                'reply': True
            },
            {
                'text': 'Меню',
                'text_en': 'Menu',
                'text_ua': 'Меню',
                'row': 0,
                'reply': True
            }
        ]
    },
    'Migration': {
        'text': 'Миграция',
        'text_en': 'Migration',
        'text_ua': 'В этом меню Вы можете получить информацию о том как:'
                   '\n-получить Украинское гражданства.'
                   '\n-получить статус беженаца'
                   '\n-оформить постоянный или временный вид на жительство.'
                   '\n\nПерейдите по кнопкам ниже и воспользуйтесь ссылками '
                   'на нормативные документы которые найдете в них.👇',
        'buttons': [
            {
                'text': 'Гражданство Украины',
                'text_en': 'Citizenship of Ukraine',
                'text_ua': 'Громадянство України',
                'row': 0,
                'inline_mode': True
            },
            {
                'text': 'Статус Беженца',
                'text_en': 'Статус Беженца',
                'text_ua': 'Статус Беженца',
                'row': 1,
                'url': 'https://telegra.ph/Status-bezhenca-rus-09-23',
                'url_ua': 'https://telegra.ph/Status-bezhenca-ukr-09-23',
                'url_en': 'https://telegra.ph/Status-bezhenca-angl-09-23'
            },
            {
                'text': 'Постоянный вид на жительство в Украине',
                'text_en': 'Permanent residence permit in Ukraine',
                'text_ua': 'Постійний дозвіл на проживання в Україні',
                'row': 2,
                'url': 'https://telegra.ph/Postoyannyj-vid-na-zhitelstvo-v'
                       '-Ukraine-rus-09-23',
                'url_ua': 'https://telegra.ph/Postoyannyj-vid-na-zhitelstvo-v'
                          '-Ukraine-ukr-09-23',
                'url_en': 'https://telegra.ph/Postoyannyj-vid-na-zhitelstvo-v'
                          '-Ukraine-angl-09-23'
            },
            {
                'text': 'Временный вид на жительство в Украине',
                'text_en': 'Temporary residence permit in Ukraine',
                'text_ua': 'Тимчасовий дозвіл на проживання в Україні',
                'row': 3,
                'url': 'https://telegra.ph/Vremennyj-vid-na-zhitelstvo-v'
                       '-Ukraine-rus-09-23',
                'url_ua': 'https://telegra.ph/Vremennyj-vid-na-zhitelstvo-v'
                          '-Ukraine-ukr-09-23',
                'url_en': 'https://telegra.ph/Vremennyj-vid-na-zhitelstvo-v'
                          '-Ukraine-angl-09-23'
            },
            {
                'text': '↩️ Назад',
                'text_en': '↩️ Back',
                'text_ua': '↩️ Назад',
                'row': 4,
                'callback_data': 'menu'
            }
        ]
    },
    'Migration_Citizenship': {
        'text': 'Гражданство Украины',
        'text_en': 'Citizenship of Ukraine',
        'text_ua': 'Громадянство України',
        'buttons': [
            {
                'text': 'Упрощенный порядок оформления гражданства Украины',
                'text_en': 'Simplified procedure for obtaining citizenship'
                           ' of Ukraine',
                'text_ua': 'Спрощений порядок оформлення громадянства'
                           ' України.',
                'url': 'https://telegra.ph/Uproshchennyj-poryadok-oformleniya'
                       '-grazhdanstva-Ukrainy-rus-09-16',
                'url_en': 'https://telegra.ph/Uproshchennyj-poryadok'
                          '-oformleniya-grazhdanstva-Ukrainy-angl-09-16',
                'url_ua': 'https://telegra.ph/Uproshchennyj-poryadok'
                          '-oformleniya-grazhdanstva-Ukrainy-ukr-09-16'
            },
            {
                'text': 'По установлению факта отцовства или материнства',
                'text_en': 'Establishing the fact of paternity or motherhood',
                'text_ua': 'За встановленням факту батьківства чи'
                           ' материнства',
                'url': 'https://telegra.ph/Po-ustanovleniyu-fakta-otcovstva'
                       '-ili-materinstva-rus-09-23 ',
                'url_en': 'https://telegra.ph/Po-ustanovleniyu-fakta'
                          '-otcovstva-ili-materinstva-angl-09-23',
                'url_ua': 'https://telegra.ph/Po-ustanovleniyu-fakta'
                          '-otcovstva-ili-materinstva-ukr-09-23'
            },
            {
                'text': 'Установление опекунства над недееспособным',
                'text_en': 'Establishment of guardianship over the'
                           ' incapacitated',
                'text_ua': 'Встановлення опікунства над недієздатним',
                'url': 'https://telegra.ph/Ustanovlenie-opeki-nad'
                       '-nedeesposobnym-rus-09-23',
                'url_en': 'https://telegra.ph/Ustanovlenie-opeki-nad'
                          '-nedeesposobnym-angl-09-23',
                'url_ua': 'https://telegra.ph/Ustanovlenie-opeki-nad'
                          '-nedeesposobnym-ukr-09-23'
            },
            {
                'text': 'Общая информация про гражданство Украины',
                'text_en': 'General information about citizenship of Ukraine',
                'text_ua': 'Загальна інформація про громадянство України',
                'url': 'https://telegra.ph/Obshchaya-informaciya-o'
                       '-grazhdanstve-Ukrainy-rus-09-16',
                'url_en': 'https://telegra.ph/Obshchaya-informaciya-o'
                          '-grazhdanstve-Ukrainy-angl-09-16',
                'url_ua': 'https://telegra.ph/Obshchaya-informaciya-o'
                          '-grazhdanstve-Ukrainy-ukr-09-16'
            },
            {
                'text': 'Восстановление гражданства Украины',
                'text_en': 'Restoration of Ukrainian citizenship',
                'text_ua': 'Відновлення громадянства України',
                'url': 'https://telegra.ph/Vosstanovlenie-grazhdanstva'
                       '-Ukrainy-rus-09-23',
                'url_en': 'https://telegra.ph/Vosstanovlenie-grazhdanstva'
                          '-Ukrainy-09-23',
                'url_ua': 'https://telegra.ph/Vosstanovlenie-grazhdanstva'
                          '-Ukrainy-ukr-09-23'
            },
            {
                'text': 'По территориальному происхождению',
                'text_en': 'By territorial origin',
                'text_ua': 'За територіальним походженням',
                'url': 'https://telegra.ph/Po-territorialnomu-proishozhdeniyu'
                       '-rus-09-23 ',
                'url_en': 'https://telegra.ph/Po-territorialnomu'
                          '-proishozhdeniyu-angl-09-23',
                'url_ua': 'https://telegra.ph/Po-territorialnomu'
                          '-proishozhdeniyu-ukr-09-23'
            },
            {
                'text': 'По установлению опекунства',
                'text_en': 'To establish guardianship',
                'text_ua': 'За встановленням опікунства',
                'url': 'https://telegra.ph/Po-ustanovleniyu-opekunstva'
                       '-rus-09-23',
                'url_en': 'https://telegra.ph/Po-ustanovleniyu-opekunstva'
                          '-angl-09-23',
                'url_ua': 'https://telegra.ph/Po-ustanovleniyu-opekunstva'
                          '-ukr-09-23'
            },
            {
                'text': 'По усыновлению', 'text_en': 'By adoption',
                'text_ua': 'За усиновленням',
                'url': 'https://telegra.ph/Po-usynovleniyu-rus-09-23',
                'url_en': 'https://telegra.ph/Po-usynovleniyu-angl-09-23',
                'url_ua': 'https://telegra.ph/Po-usynovleniyu-ukr-09-23'
            },
            {
                'text': 'По родителям', 'text_en': 'By parents',
                'text_ua': 'За батьками',
                'url': 'https://telegra.ph/Po-roditelyam-09-23',
                'url_en': 'https://telegra.ph/Po-roditelyam-angl-09-23',
                'url_ua': 'https://telegra.ph/Po-roditelyam-ukr-09-23'
            },
            {
                'text': 'По рождению', 'text_en': 'By birth',
                'text_ua': 'За народженням',
                'url': 'https://telegra.ph/Po-rozhdeniyu-Russkij-09-16',
                'url_en': 'https://telegra.ph/Po-rozhdeniyu-Angl-09-16',
                'url_ua': 'https://telegra.ph/Po-narodzhennyu-'
                          'Ukrainskoyu-09-16'
            },
        ]
    },
    'Monitoring': {
        'text': 'Мониторинг',
        'text_en': 'Monitoring',
        'text_ua': '<b>В цьому меню Ви можете:</b>'
                   '\n✳️ Створити моніторинг даних  із державних реєстрів '
                   'України 👨‍🎓.'
                   '\n✳️ Перевірити статус своїх документів 📄 ✅ 🚫'
                   '\n✳️ Контролювати кількість днів Вашого  перебування на '
                   'території України 🕠.'
                   '\n✳️ Вчасно дізнатись про наявність штрафів за порушення '
                   'правил дорожнього руху 🚗.',
        'buttons': [
            {
                'text': '👨‍🎓 Государственные реестры',
                'text_en': '👨‍🎓 State registers',
                'text_ua': '👨‍🎓 Державні реєстри',
                'row': 0,
                'callback_data': 'monitoring#state'
            },
            {
                'text': '‍📄 ✅ Проверка готовности документов',
                'text_en': '‍📄 ✅ Checking the readiness of documents',
                'text_ua': '📄 ✅ Перевірка готовність документів',
                'row': 1,
                'callback_data': 'monitoring#docstate'
            },
            {
                'text': '📄🚫 Проверка в базе недействительных документов',
                'text_en': '📄🚫 Checking invalid documents in the database',
                'text_ua': '📄🚫 Перевірка за базою недійсних документів',
                'row': 2,
                'callback_data': 'monitoring#inactive'
            },
            {
                'text': '🕠 Проверка сроков пребывания на территории Украины',
                'text_en': '🕠 Checking the duration of stay on the territory'
                           ' of Ukraine',
                'text_ua': '🕠 Перевірка термінів перебування на території'
                           ' України',
                'row': 3,
                'callback_data': 'monitoring#depart'
            },
            {
                'text': '🚗 Штрафы ПДД',
                'text_en': '🚗 Traffic fines',
                'text_ua': '🚗 Штрафи ПДР',
                'row': 4,
                'callback_data': 'monitoring#fines'
            },
            {
                'text': '⬅️ Меню',
                'text_en': '⬅️ Menu',
                'text_ua': '⬅️ Меню',
                'row': 5,
                'callback_data': 'menu'
            }
        ]
    },
    'Pay': {
        'text': '<b>У вас нет доступа к платным функциям.</b>'
                '\nВы можете использовать дополнительные функции бота за'
                ' {cost} грн в месяц.'
                '\n\nЧто входит в платные функции:'
                '\n✅ доступ к личному ассистенту'
                '\n✅ мониторинг готовности документов в миграционной службе.'
                '\n✅ подсчет дней пребывания на территории Украины.'
                '\n✅ мониторинг недействительных документов.'
                '\n✅ мониторинг данных из государственных реестров'
                '\n\n💳 Для проведения оплаты через платежный сервис LiqPay '
                'нажимай "Оплатить с помощью LiqPay".',
        'text_en': '<b> You do not have access to paid features. </b> '
                   '\nYou can use additional features of the bot for '
                   ' {cost} UAH per month. '
                   '\n\n What is included in the paid functions: '
                   '\n✅ access to the personal assistant '
                   '\n✅ monitoring the readiness of documents in the '
                   'migration service.'
                   '\n✅ counting the days spent in Ukraine.'
                   '\n✅ monitoring of invalid documents.'
                   '\n✅ monitoring of data from state registers'
                   '\n\n💳 To make a payment through the payment service'
                   'LiqPay click "Pay with LiqPay"',
        'text_ua': '<b>У Вас немає доступу до платних функцій.</b>'
                   '\nВи можете користуватися  додатковими функціями бота за '
                   '{cost} грн на місяць. '
                   '\n\nЩо входить у платні функції:'
                   '\n✅ доступ до особистого асистента'
                   '\n✅ моніторинг готовності документів в міграційній '
                   'службі.'
                   '\n✅ підрахунок днів перебування на території України.'
                   '\n✅ моніторинг недійсних документів.'
                   '\n✅ моніторинг даних з державних реєстрів'
                   '\n\n💳 Для проведення оплати через платіжний сервіс '
                   'LiqPay натискай "Сплатити за допомогою LiqPay"',
        'buttons': [
            {
                'text': 'Оплатить с помощью “LiqPay“',
                'text_en': 'Pay with “LiqPay“',
                'text_ua': 'Сплатити за допомогою “LiqPay“',
                'row': 0,
                'url': '{liq_url}',
                'url_en': '{liq_url}',
                'url_ua': '{liq_url}'
            },
            {
                'text': 'Оплатить с помощью “PortMone“',
                'text_en': 'Pay with “PortMone“',
                'text_ua': 'Сплатити за допомогою “PortMone“',
                'row': 1,
                'url': '{port_url}',
                'url_en': '{port_url}',
                'url_ua': '{port_url}'
            },
            {
                'text': '⬅️ Назад',
                'text_en': '⬅️ Back',
                'text_ua': '⬅️ Повернутися',
                'row': 2,
                'callback_data': '{back_callback}'
            },
            {
                'text': 'Меню',
                'text_en': 'Menu',
                'text_ua': 'Меню',
                'row': 2,
                'callback_data': 'menu'
            }
        ]
    },
    'pay_sub': {
        'text': 'Вы успешно оформили подписку, теперь каждые 30 дней с вашей'
                ' карты {card} будет списано {cost} грн',
        'text_en': 'You have successfully subscribed, now every 30 days from'
                   ' your card {card} will be written off {cost} uah',
        'text_ua': 'Ви успішно оформили підписку, тепер кожні 30 днів із вашої'
                   ' карти {card} буде списано {cost} грн'
    },
    'pay_continue_sub': {
        'text': 'Ваша подписка успешно продлена до {date}',
        'text_en': 'Your subscription has been successfully renewed until'
                   ' {date}',
        'text_ua': 'Ваша підписка успішно продовжена до {date}'
    },
    'Chat': {
        'text': 'В этом меню Вы можете выбрать групповой чат для общения'
                ' с гражданами Вашей страны, которые так же как и'
                ' Вы являетесь пользователями бота и могут поделиться'
                ' своим опытом пребывания в Украине.'
                '\n\nЧтобы перейти в чат, нужно выбрать страну. Сначала '
                'нажмите кнопку "Выбрать государство" и выберите страну'
                ' из списка. После этого нажмите "Перейти в чат"',
        'text_en': 'In this menu you can choose a group chat to communicate'
                   ' with the citizens of your country, who, like you,'
                   ' are users of the bot and can share their experience'
                   ' of staying in Ukraine.'
                   '\n\nTo go to chat you need to select a country. First, '
                   'click the "Select Country" button and select your country'
                   ' from the list. Then click "Go to chat"',
        'text_ua': 'В цьому меню Ви можете обрати груповий чат для'
                   ' спілкування з громадянами Вашої країни,'
                   ' які так само як і Ви є кристувачами бота і можуть'
                   ' поділитись своїм досвідом перебування в Україні.'
                   '\n\nЩоб перейти в чат потрібно обрати країну.'
                   ' Спочатку натисніть на кнопку "Обрати державу"'
                   ' та оберіть свою країну із списку.'
                   ' Після цього натисніть "Перейти в чат"',
        'buttons': [
            {
                'text': '🌐 Выбрать государство',
                'text_en': '🌐 Select state',
                'text_ua': '🌐 Обрати державу',
                'row': 0,
                'inline_mode': True
            },
            {
                'text': '⬅️ Меню',
                'text_en': '⬅️ Menu',
                'text_ua': '⬅️ Меню',
                'row': 1,
                'callback_data': 'menu'
            }
        ]
    },
    'GetCountry': {
        'text': 'Вы выбрали {country}. Выбрать категорию или выбрать другое государство?',
        'text_en': 'You have selected {country}. Choose a category or choose another state?',
        'text_ua': 'Ви обрали {country}. Вибрати категорію чи вибрати іншу державу?',
        'buttons': [
            {
                'text': '🌐 Выбрать государство',
                'text_en': '🌐 Select state',
                'text_ua': '🌐 Обрати державу',
                'inline_mode': True
            },
        ]
    },
    'GetCategory': {
        'text': 'Вы выбрали {country} и категорию {category}. Выбрать чат или выбрать другое государство?',
        'text_en': 'You have selected {country} and {category}. Choose a chat or choose another state?',
        'text_ua': 'Ви обрали {country} та категорію {category}. Вибрати чат чи вибрати іншу державу?',
        'buttons': [
            {
                'text': 'Назад',
                'text_en': 'Back',
                'text_ua': 'Повернутися',
                'row': 0,
                'callback_data': 'category#{cat_id}'
            },
            {
                'text': '🌐 Выбрать государство',
                'text_en': '🌐 Select state',
                'text_ua': '🌐 Обрати державу',
                'row': 0,
                'inline_mode': True
            },
        ]
    },
    'Support': {
        'text': 'Если у вас возникли технические проблемы при работе бота '
                'напишите сообщение нашему техническому специалисту. Для '
                'этого нажмите ❓ "Задать вопрос"'
                '\n\nЧтобы ознакомиться с договором оферты, нажмите на 📝 '
                '"Договор оферты"'
                '\n\nТакже Вы можете связаться с нами по контактам:',
        'text_en': 'If you have technical problems while running the bot, '
                   'write a message to our technician. To do this, click ❓ '
                   '"Ask a question"\n\nTo read the offer agreement, '
                   'click on 📝 "Offer agreement"'
                   '\n\nYou can also contact us by contacts:',
        'text_ua': 'Якщо у вас виникли технічні проблеми під час роботи бота'
                   ' напишіть повідомлення нашому технічному спеціалісту.'
                   ' Для цього натисніть ❓ "Задати питання"'
                   '\n\nЩоб ознайомитись договору оферти натисніть на 📝 '
                   '"Договір оферти'
                   '"\n\nТакож Ви можете зв\'язатись з нами за контактами:',
        'buttons': [
            {
                'text': '❓ Задать вопрос',
                'text_en': '❓ Ask a question',
                'text_ua': '❓ Задати питання',
                'row': 0,
                'callback_data': 'ask'
            },
            {
                'text': '📝 Договор оферты',
                'text_en': '📝 Offer agreement',
                'text_ua': '📝 Договір оферти',
                'row': 1,
                'callback_data': 'agreement'
            },
            {
                'text': '⬅️ Меню',
                'text_en': '⬅️ Menu',
                'text_ua': '⬅️ Меню',
                'row': 2,
                'callback_data': 'menu'
            }
        ]
    },
    'SupportAsk': {
        'text': 'Задайте вопросы нашему сотруднику. Опишите вашу проблему.'
                '\n\nВведите текст вопроса 👇',
        'text_en': 'Ask a question to our employee. Describe your problem.'
                   '\n\nEnter the text of the question 👇',
        'text_ua': 'Задайте запитання нашому співробітнику. Опишіть вашу '
                   'проблему.'
                   '\n\nВведіть текст запитання 👇',
        'buttons': [
            {
                'text': 'Назад',
                'text_en': 'Back',
                'text_ua': 'Повернутися',
                'row': 0,
                'reply': True
            },
            {
                'text': '⬅️ Меню',
                'text_en': '⬅️ Menu',
                'text_ua': '⬅️ Меню',
                'row': 0,
                'reply': True
            }
        ]
    },
    'ThxForQuestion': {
        'text': 'Мы постараемся проработать Ваш запрос максимально быстро!',
        'text_en': 'We will try to process your request as quickly as'
                   ' possible!',
        'text_ua': 'Ми постараємось опрацювати Ваш запит максимально швидко!',
        'buttons': [
            {
                'text': 'Назад',
                'text_en': 'Back',
                'text_ua': 'Повернутися',
                'row': 0,
                'reply': True
            },
            {
                'text': '⬅️ Меню',
                'text_en': '⬅️ Menu',
                'text_ua': '⬅️ Меню',
                'row': 0,
                'reply': True
            }
        ]
    },
    'Agreement': {
        'text': 'Договор Оферты',
        'text_en': 'Agreement',
        'text_ua': 'Договір оферти',
        'buttons': [
            {
                'text': 'Назад',
                'text_en': 'Back',
                'text_ua': 'Повернутися',
                'row': 0,
                'reply': True
            },
            {
                'text': '⬅️ Меню',
                'text_en': '⬅️ Menu',
                'text_ua': '⬅️ Меню',
                'row': 0,
                'reply': True
            }
        ]
    },
    'Profile': {
        'text': '🔹Перейдите в ☂️"Ассистент", чтобы получить контактные '
                'данные личного ассистента, который будет Вашим помощником '
                'во время пребывания в Украине.'
                '\n🔹Воспользуйтесь функцией транслитерации, чтобы узнать, '
                'как правильно пишется ваше имя на украинском языке. Для '
                'этого перейдите в "Мое имя"'
                '\n🔹Чтобы проверить и изменить свои подписки на мониторинг'
                ' данных перейдите в ✍️"Мои подписки".'
                '\n🔹Чтобы просмотреть статус своего тарифа и просмотреть '
                'условия использования дополнительных функций, перейдите в'
                ' "Оплата дополнительных функций"',
        'text_en': '🔹Go to ☂️"Assistant" to get the contact '
                   'data of a personal assistant who will be your assistant '
                   'during your stay in Ukraine.'
                   '\n🔹Use the transliteration function to find out '
                   'how to spell your name correctly in Ukrainian. To '
                   'go to "My Name"'
                   '\n🔹To check and change your data monitoring subscriptions'
                   ' go to ✍️"My Subscriptions".'
                   '\n🔹To view the status of your plan and view the '
                   'terms and conditions for using additional features, go to'
                   '"Paying for additional features"',
        'text_ua': '🔹Перейдіть в ☂️"Асистент", щоб отримати контактні дані'
                   ' особистого асистента, який буде Вашим помічником'
                   ' під час перебування в Україні.'
                   '\n🔹Скористайтесь функцією транслітерації, щоб дізнатись '
                   'як правильно пишеться ваше ім\'я українською мовою. Для '
                   'цього перейдіть в "Моє ім\'я"'
                   '\n🔹Щоб перевіри та змінити свої підписки на моніторинг '
                   'даних перейдіть в ✍️"Мої підписки".'
                   '\n🔹Щоб переглянути статус свого тарифу, та переглянути '
                   'умови використання додаткових функцій перейдіть в'
                   ' "Оплата додаткових функцій"',
        'buttons': [
            {
                'text': '🇺🇦Сменить язык',
                'text_en': '🇺🇦Change language',
                'text_ua': '🇺🇦Змінити Мову',
                'row': 0,
                'reply': True
            },
            {
                'text': '☂️ Ассистент',
                'text_en': '☂️ Assistant',
                'text_ua': '☂️ Асистент',
                'row': 1,
                'reply': True
            },
            {
                'text': '✍️ Мои подписки',
                'text_en': '✍️ My subscriptions',
                'text_ua': '✍️ Мої підписки',
                'row': 1,
                'reply': True
            },
            {
                'text': 'Моё имя',
                'text_en': 'My name',
                'text_ua': 'Моє ім\'я',
                'row': 2,
                'reply': True
            },
            {
                'text': 'Сохраненные поиски',
                'text_en': 'Saved searches',
                'text_ua': 'Збережені пошуки',
                'row': 2,
                'reply': True
            },
            {
                'text': 'Оплата дополнительных функций',
                'text_en': 'Payment for additional features',
                'text_ua': 'Оплата додаткових функцій',
                'row': 3,
                'reply': True
            },
            {
                'text': '⬅️ Меню',
                'text_en': '⬅️ Menu',
                'text_ua': '⬅️ Меню',
                'row': 4,
                'reply': True
            }
        ]
    },
    'Name': {
        'text': 'Ваше имя - {name_en}'
                '\n\nДля мониторинга информации о себе в украинских '
                'государственных реестрах используйте написания вашего '
                'Имени, фамилии, отчество (опционально) украинском языке.'
                '\n\nВаше имя, фамилию украинском языке:',
        'text_en': 'Your name is {name_en}'
                   '\n\nTo monitor information about yourself in Ukrainian '
                   'public registers, use the spelling of your '
                   'Name, surname, patronymic (optional) in Ukrainian.'
                   '\n\nYour first name, last name in Ukrainian:',
        'text_ua': 'Ваше ім\'я - {name_en}'
                   '\n\nДля моніторингу інформації про себе в українських '
                   'державних реєстрах '
                   'Використовуйте написання вашого Імені, прізвища,'
                   ' по батькові (опціонально) українською мовою.'
                   '\n\nВаше ім\'я, прізвище українською мовою:',
        'buttons': [
            {
                'text': 'Назад',
                'text_en': 'Back',
                'text_ua': 'Повернутися',
                'row': 0,
                'reply': True
            },
            {
                'text': '⬅️ Меню',
                'text_en': '⬅️ Menu',
                'text_ua': '⬅️ Меню',
                'row': 0,
                'reply': True
            }
        ]
    },
    'NameNotSet': {
        'text': 'Введите свое имя фамилия и отчество (если у вас есть) латиницой.',
        'text_en': 'Enter your first name, last name and patronymic (if you have one) in Latin.',
        'text_ua': 'Введіть своє ім\'я прізвище та по батькові (якщо у вас є) латиницею.',
        'buttons': [
            {
                'text': 'Назад',
                'text_en': 'Back',
                'text_ua': 'Повернутися',
                'row': 0,
                'reply': True
            },
            {
                'text': '⬅️ Меню',
                'text_en': '⬅️ Menu',
                'text_ua': '⬅️ Меню',
                'row': 0,
                'reply': True
            }
        ]
    },
    'SavedSearch': {
        'text': 'Сохраненные поиски:\n'
                'Каждый раз когда вы делаете поиск в государственных реестрах, '
                'у вас есть возможность сохранить данные поиска, чтобы небыло нужды повторно вводить их.',
        'text_en': 'Saved searches:\n'
                   'Every time you do a search on public registries, '
                   'you have the option to save your search data so you don`t have to re-enter it.',
        'text_ua': 'Збережені пошуки:\n'
                   'Щоразу, коли ви робите пошук у державних реєстрах, '
                   'у вас є можливість зберегти дані пошуку, щоб не було потреби повторно вводити їх',

        'buttons': [
            {
                'text': 'Показати ({count})',
                'text_en': 'Show ({count})',
                'text_ua': 'Подивитися ({count})',
                'row': 0,
                'callback_data': '{call_data}'
            }
        ]

    },
    'SavedAsvp': {
        'text': 'Для поиска в Системе автоматизированного производства сохранены "{saved_data}" данные',
        'text_en': '"{saved_data}" data has been saved for searching in the Computer-Aided Manufacturing System',
        'text_ua': 'Для пошуку в Системі автоматизованого виробництва збережено "{saved_data}" дані',
        'buttons': [
            {
                'text': 'Удалить',
                'text_en': 'Remove',
                'text_ua': 'Видалити',
                'row': 0,
                'callback_data': 'save_d#{obj_id}'
            },
            {
                'text': 'Показать еще',
                'text_en': 'Show more',
                'text_ua': 'Показати ще',
                'row': 1,
                'callback_data': 'save_s#{page}'
            }
        ]
    },
    'SavedBdr': {
        'text': 'Для поиска штрафов ПДД сохранены "{saved_data}" данные',
        'text_en': '"{saved_data}" data was saved to search for traffic fines',
        'text_ua': 'Для пошуку штрафів правил дорожнього руху збережено "{saved_data}" дані',
        'buttons': [
            {
                'text': 'Удалить',
                'text_en': 'Remove',
                'text_ua': 'Видалити',
                'row': 0,
                'callback_data': 'save_d#{obj_id}'
            },
            {
                'text': 'Показать еще',
                'text_en': 'Show more',
                'text_ua': 'Показати ще',
                'row': 1,
                'callback_data': 'save_s#{page}'
            }
        ]
    },
    'SavedCourt': {
        'text': 'Для поиска в судебном реестре сохранены "{saved_data}" данные',
        'text_en': 'Saved "{saved_data}" data for searching in court register',
        'text_ua': 'Для пошуку в судовому реєстрі збережено "{saved_data}" дані',
        'buttons': [
            {
                'text': 'Удалить',
                'text_en': 'Remove',
                'text_ua': 'Видалити',
                'row': 0,
                'callback_data': 'save_d#{obj_id}'
            },
            {
                'text': 'Показать еще',
                'text_en': 'Show more',
                'text_ua': 'Показати ще',
                'row': 1,
                'callback_data': 'save_s#{page}'
            }
        ]
    },
    'SavedCourtAssign': {
        'text': 'Для поиска судебных дел, предназначенных для рассмотрения сохранены "{saved_data}" данные',
        'text_en': 'Saved "{saved_data}" data to search for court cases to be considered',
        'text_ua': 'Для пошуку судових справ, призначених для розгляду, збережені "{saved_data}" дані',
        'buttons': [
            {
                'text': 'Удалить',
                'text_en': 'Remove',
                'text_ua': 'Видалити',
                'row': 0,
                'callback_data': 'save_d#{obj_id}'
            },
            {
                'text': 'Показать еще',
                'text_en': 'Show more',
                'text_ua': 'Показати ще',
                'row': 1,
                'callback_data': 'save_s#{page}'
            }
        ]
    },
    'SavedDebtors': {
        'text': 'Для поиска в реестре должников сохранены "{saved_data}" данные',
        'text_en': '"{saved_data}" data saved for search in the register of debtors',
        'text_ua': 'Для пошуку в реєстрі боржників збережено "{saved_data}" дані',
        'buttons': [
            {
                'text': 'Удалить',
                'text_en': 'Remove',
                'text_ua': 'Видалити',
                'row': 0,
                'callback_data': 'save_d#{obj_id}'
            },
            {
                'text': 'Показать еще',
                'text_en': 'Show more',
                'text_ua': 'Показати ще',
                'row': 1,
                'callback_data': 'save_s#{page}'
            }
        ]
    },
    'SavedNational': {
        'text': 'Для поиска во всех государственных реестрах сохранены "{saved_data}" данные',
        'text_en': 'Saved "{saved_data}" data for searching in all state registries',
        'text_ua': 'Для пошуку у всіх державних реєстрах збережено "{saved_data}" дані',
        'buttons': [
            {
                'text': 'Удалить',
                'text_en': 'Remove',
                'text_ua': 'Видалити',
                'row': 0,
                'callback_data': 'save_d#{obj_id}'
            },
            {
                'text': 'Показать еще',
                'text_en': 'Show more',
                'text_ua': 'Показати ще',
                'row': 1,
                'callback_data': 'save_s#{page}'
            }
        ]
    },
    'SavedWanted': {
        'text': 'Для поиска лиц которые в розыске сохранены "{saved_data}" данные',
        'text_en': 'To search for persons who are wanted, "{saved_data}" data is saved',
        'text_ua': 'Для пошуку осіб, які в розшуку збережені "{saved_data}" дані',
        'buttons': [
            {
                'text': 'Удалить',
                'text_en': 'Remove',
                'text_ua': 'Видалити',
                'row': 0,
                'callback_data': 'save_d#{obj_id}'
            },
            {
                'text': 'Показать еще',
                'text_en': 'Show more',
                'text_ua': 'Показати ще',
                'row': 1,
                'callback_data': 'save_s#{page}'
            }
        ]
    },
    'SavedDelete': {
        'text': 'Сохраненный поиск Успешно удален, чтобы снова его добавить нужно выполнить поиск с нужными параметрами и следовать инструкции бота',
        'text_en': 'Saved search Successfully deleted, to add it again you need to search with the required parameters and follow the instructions of the bot',
        'text_ua': 'Збережений пошук Успішно видалено, щоб знову його додати потрібно виконати пошук з потрібними параметрами та дотримуватися інструкції бота',
    },
    'Assistant': {
        'text': 'У вас есть доступ к личному помощнику.'
                ' Он будет ассистировать вас по любым вопросам и'
                ' в любое время.',
        'text_en': 'You have access to a personal assistant. He will assist '
                   'you through any questions and at any time.',
        'text_ua': 'У вас є доступ до особистого помічника. Він буде '
                   'асистувати вас по будь-яких питань та в будь-який час.',
        'buttons': [
            {
                'text': 'Назад',
                'text_en': 'Back',
                'text_ua': 'Повернутися',
                'row': 0,
                'reply': True
            },
            {
                'text': '⬅️ Меню',
                'text_en': '⬅️ Menu',
                'text_ua': '⬅️ Меню',
                'row': 0,
                'reply': True
            }
        ]
    },
    'Payment_Advanced': {
        'text': 'Статус вашего аккаунта "Продвинутый"'
                '\n\nВы можете использовать дополнительные функции бота.'
                '\n\nСредства будут списываться с вашего счета автоматически.'
                ' Дата следующего списания {date_pay}',
        'text_en': 'Your Advanced Account Status'
                   '\n\nYou can use additional features of the bot.'
                   '\n\nFunds will be deducted from your account '
                   'automatically. Date of next write-off {date_pay}',
        'text_ua': 'Статус вашого облікового запису "Просунутий"'
                   '\n\nВи можете користуватися додатковими функціями бота.'
                   '\n\nКошти будуть списуватися з вашого рахунку автоматично.'
                   ' Дата наступного списання {date_pay}',
        'buttons': [
            {
                'text': 'Прекратить платную подписку',
                'text_en': 'Stop Paid Subscription',
                'text_ua': 'Припинити платну підписку',
                'row': 0,
                'callback_data': 'cancel_subscribe'
            },
            {
                'text': '⬅️ Назад',
                'text_en': '⬅️ Back',
                'text_ua': '⬅️ Повернутися',
                'row': 1,
                'callback_data': '{back_callback}'
            },
            {
                'text': 'Меню',
                'text_en': 'Menu',
                'text_ua': 'Меню',
                'row': 1,
                'callback_data': 'menu'
            }
        ]
    },
    'Payment_Free': {
        'text': 'Статус вашего аккаунта "Свободный"'
                '\n\nВы можете использовать дополнительные функции бота.',
        'text_en': 'The status of your account "Free"'
                   '\n\nYou can use additional features of the bot.',
        'text_ua': 'Статус вашого облікового запису "Вільний"'
                   '\n\nВи можете користуватися додатковими функціями бота.',
        'buttons': [
            {
                'text': '⬅️ Назад',
                'text_en': '⬅️ Back',
                'text_ua': '⬅️ Повернутися',
                'row': 0,
                'callback_data': '{back_callback}'
            },
            {
                'text': 'Меню',
                'text_en': 'Menu',
                'text_ua': 'Меню',
                'row': 0,
                'callback_data': 'menu'
            }
        ]
    },
    'Term_of_stay': {
        'text': 'Данная функция при вводе необходимых данных поможет вам '
                'сориентироваться о оставшемся законном сроке пребывания в '
                'Украине не нарушая местное. законодательство.'
                ' Также система оповестит вас заранее о исходе данного срока,'
                ' что позволит вовремя вам подать документы в'
                ' миграционную службу не нарушая закон'
                '\n\nУкажите даты ваших поездок в Украину за последние 180 '
                'дней (въезд и выезд).'
                '\nЕсли эта поездка для вас первая укажите только дату въезда',
        'text_en': 'This function, when entering the necessary data,'
                   ' will help you navigate the remaining legal period of'
                   ' stay in Ukraine without violating the local'
                   ' legislation. Also, the system will notify you'
                   ' in advance of the expiration of this period,'
                   ' which will allow you to submit documents to the'
                   ' migration service on time without violating the law'
                   '\n\nIndicate the dates of your trips to Ukraine for'
                   ' the last 180 days (in and out).'
                   '\nIf this is your first trip, enter only the date of '
                   'entry',
        'text_ua': 'Данная функция при вводе необходимых данных поможет'
                   ' вам сориентироваться о оставшемся законном сроке'
                   ' пребывания в Украине не нарушая местное'
                   ' законодательство. Также система оповестит вас заранее'
                   ' о исходе данного срока, что позволит вовремя'
                   ' вам подать документы в миграционную службу'
                   ' не нарушая закон.'
                   '\n\nУкажите даты ваших поездок в Украину за последние 180 '
                   'дней (въезд и выезд).'
                   '\nЕсли эта поездка для вас первая укажите только дату '
                   'въезда'
    },
    'Enter_Date': {
        'text': 'Введите дату въезда, в формате 01/01/2021(дд/мм/гггг)👇',
        'text_en': 'Enter the date of entry,'
                   ' in the format 01/01/2021(dd/mm/yyyy)👇',
        'text_ua': 'Введіть дату в\'їзду у форматі 01/01/2021(дд/мм/гггг)👇',
        'buttons': [
            {
                'text': 'Назад',
                'text_en': 'Back',
                'text_ua': 'Повернутися',
                'row': 0,
                'reply': True
            },
            {
                'text': '⬅️ Меню',
                'text_en': '⬅️ Menu',
                'text_ua': '⬅️ Меню',
                'row': 0,
                'reply': True
            }
        ]
    },
    'DateEntry': {
        'text': 'Поездка №{depart_num}'
                '\nДата въезда - {date_of_entry}'
                '\n\nВведите дату выезда, в формате 01/01/2021(дд/мм/гггг)'
                '\n\nЕсли вы еще находится на теретории Украины и НЕ '
                'спланировали дату выезда, то выберите кнопку "Считать дни"',
        'text_en': 'Trip №{depart_num}'
                   '\nArrival date - {date_of_entry}'
                   '\n\nEnter departure date, in the format 01/01/2021('
                   'dd/mm/yyyy)'
                   '\n\nIf you are still on the territory of Ukraine and '
                   'have NOT planned the '
                   'date of departure,then select the button "Count days"',
        'text_ua': "Поїздка №{depart_num}"
                   '\nДата в\'їзду - {date_of_entry}'
                   '\n\nВведіть дату виїзду, в форматі 01/01/2021(дд/мм/рррр)'
                   '\n\nЯкщо ви ще знаходиться на території України і НЕ '
                   'спланували дату виїзду, '
                   'то виберіть кнопку "Рахувати дні"',
        'buttons': [
            {
                'text': 'Считать дни',
                'text_en': 'Count days',
                'text_ua': 'Рахувати дні',
                'row': 0,
                'callback_data': 'no_departure'
            },
            {
                'text': '⬅️ Назад',
                'text_en': '⬅️ Back',
                'text_ua': '⬅️ Повернутися',
                'row': 1,
                'callback_data': 'back'
            }

        ]
    },
    'DateError': {
        'text': 'Вы неправильно ввели даты, попробуйте еще раз',
        'text_en': 'You entered the dates incorrectly, please try again',
        'text_ua': 'Ви неправильно ввели дати, спробуйте ще раз',
    },
    'DepartureEntryTrip': {
        'text': '\n\nПоездка №{trip}\nДата въезда - {date_of_entry}',
        'text_en': '\n\nTrip №{trip}\nDeparture date - {date_of_entry}',
        'text_ua': '\n\nПоїздка №{trip}\nДата в\'їзду - {date_of_entry}',
        'buttons': [
            {
                'text': 'Подписаться на расчет дней',
                'text_en': 'Subscribe to the calculation of days',
                'text_ua': 'Підписатися на розрахунок днів',
                'row': 1,
                'callback_data': 'subscribe'
            }
        ]
    },
    'DepartureTrip': {
        'text': '\n\nПоездка №{trip}\nДата въезда - {date_of_entry}'
                '\nДата выезда - {date_of_departure}',
        'text_en': '\n\nTrip №{trip}\nDeparture date - {date_of_entry}'
                   '\nDate of departure - {date_of_departure}',
        'text_ua': '\n\nПоїздка №{trip}\nДата в\'їзду - {date_of_entry}'
                   '\nДата виїзду - {date_of_departure}',
        'buttons': [
            {
                'text': 'Добавить поездку',
                'text_en': 'Add a trip',
                'text_ua': 'Додати поїздку',
                'row': 0,
                'callback_data': 'add_trip'
            },
            {
                'text': 'Подписаться на расчет дней',
                'text_en': 'Subscribe to the calculation of days',
                'text_ua': 'Підписатися на розрахунок днів',
                'row': 1,
                'callback_data': 'subscribe'
            },
            {
                'text': '⬅️ Назад',
                'text_en': '⬅️ Back',
                'text_ua': '⬅️ Повернутися',
                'row': 2,
                'callback_data': 'back'
            }
        ]
    },
    'DepartViolated': {
        'text': '\n\n<b>Вы нарушили сроки пребывания на {days} дней</b>',
        'text_en': '\n\n<b>You violated the terms of stay for {days} days</b>',
        'text_ua': '\n\n<b>Ви порушили термін перебування на {days} днів</b>',
    },
    'DepartLeft': {
        'text': '\n\n<b>Вам осталось: {days} дней</b>',
        'text_en': '\n\n<b>You have: {days} days left</b>',
        'text_ua': '\n\n<b>Вам залишилось: {days} днів</b>',
    },
    'DepartSubs': {
        'text': 'Подписка на расчет дней оформлена!'
                '\n\nКогда будут новые события - мы сообщим вас',
        'text_en': 'Subscription to the calculation of days has been issued!'
                   '\n\nWhen there are new events - we will notify you',
        'text_ua': 'Підписку на розрахунок днів оформлено!'
                   '\n\nКоли будуть нові події – ми повідомимо вас'
    },
    'Car_fines': {
        'text': 'При вводе интересующих вас данных, вы будете в курсе о '
                'нарушении вами правил дорожного движения и наличии штафа,'
                ' что позволит вам своевременно оплачивать данные штрафы'
                ' без исполнительного производства и передачи данных'
                ' в миграционные органы с последующим запретом'
                ' на въезд в Украину',
        'text_en': 'When entering the data you are interested in, you'
                   ' will be aware of your violation of traffic rules and'
                   ' the presence of a fine, which will allow you to pay'
                   ' these fines in a timely manner without enforcement'
                   ' proceedings and transferring data to the migration'
                   ' authorities with a subsequent ban on entry into Ukraine',
        'text_ua': 'При введенні даних, що вас цікавлять, ви будете в'
                   ' курсі про порушення вами правил дорожнього руху та'
                   ' наявність штафу, що дозволить вам своєчасно сплачувати'
                   ' дані штрафи без виконавчого провадження та передачі'
                   ' даних в міграційні органи з подальшою забороною на '
                   'в\'їзд в Україну',
    },
    'Enter_car_number': {
        'text': 'Введите номер Транспортного средства 👇',
        'text_en': 'Enter Vehicle Number 👇',
        'text_ua': 'Введіть номер Транспортного засобу 👇',
        'buttons': [
            {
                'text': 'Назад',
                'text_en': 'Back',
                'text_ua': 'Повернутися',
                'row': 0,
                'reply': True
            },
            {
                'text': '⬅️ Меню',
                'text_en': '⬅️ Menu',
                'text_ua': '⬅️ Меню',
                'row': 0,
                'reply': True
            }
        ]
    },
    'Enter_car_series': {
        'text': 'Введите РНОКПП, или серия и номер паспорта или серия и номер'
                ' водительского удостоверения, или серия и номер'
                ' постановления, или серия и номер свидетельства'
                ' о регистрации ТС 👇',
        'text_en': 'Enter RNOKPP, or the series and number of the passport,'
                   ' or the series and number of the driver\'s license, '
                   'or the series and number of the resolution,'
                   ' or the series and number of the vehicle'
                   ' registration certificate 👇',
        'text_ua': 'Введіть РНОКПП, або серія та номер паспорта або серія '
                   'та номер посвідчення водія, або серія та номер постанови,'
                   ' або серія та номер свідоцтва про реєстрацію ТЗ 👇',
        'buttons': [
            {
                'text': 'Назад',
                'text_en': 'Back',
                'text_ua': 'Повернутися',
                'row': 0,
                'reply': True
            },
            {
                'text': '⬅️ Меню',
                'text_en': '⬅️ Menu',
                'text_ua': '⬅️ Меню',
                'row': 0,
                'reply': True
            }
        ]
    },
    'Fines_Start': {
        'text': 'Начинаю поиск штрафов по авто...',
        'text_en': 'I\'m looking for car fines...',
        'text_ua': 'Починаю пошук штрафів з авто...',
        'buttons': [
            {
                'text': '⬅️ Меню',
                'text_en': '⬅️ Menu',
                'text_ua': '⬅️ Меню',
                'row': 0,
                'reply': True
            }
        ]
    },
    'Fines_Result': {
        'text': '<b>🚘Номер ТС:</b> {car_number}'
                '\n<b>#️⃣Номер постановления:</b> {resolution}'
                '\n<b>📅Дата нарушения:</b> {date}'
                '\n<b>💳Сумма штрафа:</b> {value}грн'
                '\n{payment}',
        'text_en': '<b>🚘Car number:</b> {car_number}'
                   '\n<b>#️⃣Decree number:</b> {resolution}'
                   '\n<b>📅Date of violation:</b> {date}'
                   '\n<b>💳The amount of the fine:</b> {value}UAH'
                   '{payment}',
        'text_ua': '<b>🚘Номер ТЗ:</b> {car_number}'
                   '\n<b>#️⃣Номер постанови:</b> {resolution}'
                   '\n<b>📅Дата порушення:</b> {date}'
                   '\n<b>💳Сума штрафу:</b> {value}грн'
                   '{payment}',
        'buttons': [
            {
                'text': 'Смотреть',
                'text_en': 'View',
                'text_ua': 'Дивитися',
                'row': 0,
                'url': '{url_view}',
                'url_en': '{url_view}',
                'url_ua': '{url_view}'
            }
        ]
    },
    'Fines_Result_Not_Found': {
        'text': 'Штрафов не найдено или при поиске произошла ошибка',
        'text_en': 'No penalties found or an error occurred while searching',
        'text_ua': 'Штрафів не знайдено або при пошуку сталася помилка',
        'buttons': [
            {
                'text': '⬅️ Меню',
                'text_en': '⬅️ Menu',
                'text_ua': '⬅️ Меню',
                'row': 0,
                'reply': True
            }
        ]
    },
    'Fines_Subscribe': {
        'text': 'Если вы хотите следить за штрафами по авто '
                'с Номер ТС: {car_number}, то вы можете',
        'text_en': 'If you want to keep track of car fines '
                   'with number: {car_number}, then you can',
        'text_ua': 'Якщо ви хочете слідкувати за штрафами по авто '
                   'з Номер ТЗ: {car_number}, то ви можете',
        'buttons': [
            {
                'text': 'Подписаться',
                'text_en': 'Subscribe',
                'text_ua': 'Підписатися',
                'row': 0,
                'callback_data': 'bdr#{bdr_id}'
            },
            {
                'text': '↩️ Меню',
                'text_en': '↩️ Menu',
                'text_ua': '↩️ Меню',
                'row': 1,
                'callback_data': 'menu'
            },
        ]
    },
    'FinesSubscribeSuccess': {
        'text': 'Подписка на поиск штрафов по номеру "{car_number}" оформлена!'
                '\n\nКогда будут новые события - мы сообщим вас',
        'text_en': 'Search for fines by number "{car_number}" Subscribed!'
                   '\n\nWhen there are new events - we will notify you',
        'text_ua': 'Підписка на пошук штрафів за номером "{car_number}" '
                   'оформлена!'
                   '\n\nКоли будуть нові події – ми повідомимо вас'
    },
    'DocumentsReadiness': {
        'text': 'Данная функция поможет вам ежедневно в автоматическом режиме'
                'отслеживать готовность введенного вами документа.'
                '\n\nПри изменении статуса вы сразу же будете оповещены и '
                'сможете получить интересующий вас документ без промедления.'
                '\n\nВыберите тип документа, состояние изготовление которого '
                'нужно проверить 👇',
        'text_en': 'This function will help you automatically monitor the'
                   ' readiness of the document you entered on a daily basis.'
                   ' When you change the status'
                   '\n\nYou will be immediately notified and will be able to '
                   'receive the document you are interested in without delay.'
                   '\n\nSelect the type of document whose production status '
                   'you want to check 👇',
        'text_ua': 'Ця функція допоможе вам щодня в автоматичному режимі'
                   ' відстежувати готовність введеного вами документа.'
                   '\n\nВи відразу ж будете оповіщені і зможете отримати '
                   'цікавий для вас документ без зволікання.'
                   '\n\nВиберіть тип документа, стан якого потрібно '
                   'перевірити 👇',
        'buttons': [
            {
                'text': 'Выбрать',
                'text_en': 'Select',
                'text_ua': 'Вибрати',
                'row': 0,
                'inline_mode': True
            },
            {
                'text': '↩️ Назад',
                'text_en': '↩️ Back',
                'text_ua': '↩️ Назад',
                'row': 1,
                'callback_data': 'monitoring_back'
            }
        ]
    },
    'DocumentsType': {
        'text': 'Тип документа, изготовление которого нужно проверить',
        'text_en': 'Тип документа, изготовление которого нужно проверить',
        'text_ua': 'Тип документа, изготовление которого нужно проверить',
        'buttons': [
            {
                'text': 'ID Паспорт',
                'text_en': 'ID passport',
                'text_ua': 'ID Паспорт',
                'callback_data': 'id',
            },
            {
                'text': 'Загран Паспорт',
                'text_en': 'International passport',
                'text_ua': 'Закордонний Паспорт',
                'callback_data': 'zp',
            },
            {
                'text': 'Вид на временное жительство',
                'text_en': 'Temporary residence permit',
                'text_ua': 'Вид на тимчасове проживання',
                'callback_data': 'tt',
            },
            {
                'text': 'Вид на постоянное жительство',
                'text_en': 'Permanent residence permit',
                'text_ua': 'Вид на постійне проживання',
                'callback_data': 'tp',
            },
            {
                'text': 'Разрешение на иммиграцию в Украину',
                'text_en': 'Permission to immigrate to Ukraine',
                'text_ua': 'Дозвіл на імміграцію в Україну',
                'callback_data': 'dd',
            },
            {
                'text': 'Продление срока пребывания в Украине',
                'text_en': 'Extension of stay in Ukraine',
                'text_ua': 'Продовження терміну перебування в Україні',
                'callback_data': 'pp',
            }
        ]
    },
    'DocumentsKind': {
        'text': 'Для кого оформлялся документ?',
        'text_en': 'Who was the document for?',
        'text_ua': 'Для кого оформлювався документ?',
        'buttons': [
            {
                'text': 'Для взрослого',
                'text_en': 'For an adult',
                'text_ua': 'Для дорослого',
                'callback_data': '0',
                'row': 0,
            },
            {
                'text': 'Для ребенка',
                'text_en': 'For a child',
                'text_ua': 'Для дитини',
                'callback_data': '1',
                'row': 0,
            },
            {
                'text': '⬅️ Назад',
                'text_en': '⬅️ Back',
                'text_ua': '⬅️ Повернутися',
                'row': 1,
                'callback_data': 'back'
            }
        ]
    },
    'DocumentsZp': {
        'text': 'Выбери паспорта гражданина Украины,'
                ' на основании которого осуществлялось оформление',
        'text_en': 'Choose the passport of a citizen of Ukraine,'
                   ' on the basis of which the registration was carried out',
        'text_ua': 'Обери паспорти громадянина України,'
                   ' на підставі якого здійснювалось оформлення',
        'buttons': [
            {
                'text': 'Паспорт в форме книги',
                'text_en': 'Passport in the form of a book',
                'text_ua': 'Паспорт у формі книги',
                'callback_data': 'book',
                'row': 0
            },
            {
                'text': 'ID Паспорт',
                'text_en': 'ID passport',
                'text_ua': 'ID Паспорт',
                'callback_data': 'id',
                'row': 1
            },
            {
                'text': '↩️ Назад',
                'text_en': '↩️ Back',
                'text_ua': '↩️ Назад',
                'row': 2,
                'callback_data': 'back'
            }
        ]
    },
    'DocumentsId': {
        'text': 'Для проверки состояния оформления паспорта в форме карточки,'
                ' пожалуйста, введите серию и номер документа,'
                ' на основании которого осуществлено оформление.',
        'text_en': 'To check the status of issuing a passport in the form of'
                   ' a card, please enter the series and number of the'
                   ' document on the basis of which the issuance was'
                   ' carried out.',
        'text_ua': 'Для перевірки стану оформлення паспорта у формі картки,'
                   ' будь ласка, введіть серію та номер документа,'
                   ' на підставі якого здійснено оформлення.',
        'buttons': [
            {
                'text': 'Паспорт в форме книги',
                'text_en': 'Passport in the form of a book',
                'text_ua': 'Паспорт у формі книги',
                'callback_data': 'book',
                'row': 0
            },
            {
                'text': 'ID Паспорт',
                'text_en': 'ID passport',
                'text_ua': 'ID Паспорт',
                'callback_data': 'id',
                'row': 1
            },
            {
                'text': 'Свидетельства о рождении',
                'text_en': 'Birth certificates',
                'text_ua': 'Свідоцтва про народження',
                'callback_data': 'certificate',
                'row': 2
            },
            {
                'text': '↩️ Назад',
                'text_en': '↩️ Back',
                'text_ua': '↩️ Назад',
                'row': 3,
                'callback_data': 'back'
            }
        ]
    },
    'DocumentsOld': {
        'text': 'Введите данные документа, на основании которого'
                ' осуществлялось оформление'
                '\n\nВведите серию и номер используя латинские буквы и '
                'арабские цифры без пробелов (пример: GO1407665)',
        'text_en': 'Enter the data of the document on the basis of which the'
                   ' registration was carried out'
                   '\n\nEnter the series and number using latin letters and '
                   'arabic numerals without spaces (example: GO1407665)',
        'text_ua': 'Введіть дані документа, на підставі якого здійснювалось'
                   ' оформлення'
                   '\n\nВведіть серію та номер за допомогою латинських літер '
                   'та арабських цифр без пробілів (приклад: GO1407665)',
        'buttons': [
            {
                'text': '↩️ Назад',
                'text_en': '↩️ Back',
                'text_ua': '↩️ Назад',
                'row': 0,
                'callback_data': 'back'
            }
        ]
    },
    'DocumentsBookSeries': {
        'text': 'Введите серию паспорта в форме книги',
        'text_en': 'Enter a series of passport in the form of a book',
        'text_ua': 'Введіть серію паспорта у формі книги',
        'buttons': [
            {
                'text': 'Назад',
                'text_en': 'Back',
                'text_ua': 'Повернутися',
                'row': 0,
                'reply': True
            },
            {
                'text': '⬅️ Меню',
                'text_en': '⬅️ Menu',
                'text_ua': '⬅️ Меню',
                'row': 0,
                'reply': True
            }
        ]
    },
    'DocumentsBookNumber': {
        'text': 'Введите номер паспорта в форме книги',
        'text_en': 'Enter a number of passport in the form of a book',
        'text_ua': 'Введіть номер паспорта у формі книги',
        'buttons': [
            {
                'text': 'Назад',
                'text_en': 'Back',
                'text_ua': 'Повернутися',
                'row': 0,
                'reply': True
            },
            {
                'text': '⬅️ Меню',
                'text_en': '⬅️ Menu',
                'text_ua': '⬅️ Меню',
                'row': 0,
                'reply': True
            }
        ]
    },
    'DocumentsIdNumber': {
        'text': 'Введите номер паспорта в форме id карты',
        'text_en': 'Enter a number of passport in the form of a id card',
        'text_ua': 'Введіть номер паспорта у формі id картки',
        'buttons': [
            {
                'text': 'Назад',
                'text_en': 'Back',
                'text_ua': 'Повернутися',
                'row': 0,
                'reply': True
            },
            {
                'text': '⬅️ Меню',
                'text_en': '⬅️ Menu',
                'text_ua': '⬅️ Меню',
                'row': 0,
                'reply': True
            }
        ]
    },
    'DocumentsCertificateSeries': {
        'text': 'Введите серию Свидетельства о рождении',
        'text_en': 'Enter series of Birth Certificates',
        'text_ua': 'Введіть серію Свідоцтва про народження',
        'buttons': [
            {
                'text': 'Назад',
                'text_en': 'Back',
                'text_ua': 'Повернутися',
                'row': 0,
                'reply': True
            },
            {
                'text': '⬅️ Меню',
                'text_en': '⬅️ Menu',
                'text_ua': '⬅️ Меню',
                'row': 0,
                'reply': True
            }
        ]
    },
    'DocumentsCertificateNumber': {
        'text': 'Введите номер Свидетельства о рождении',
        'text_en': 'Enter number of Birth Certificates',
        'text_ua': 'Введіть номер Свідоцтва про народження',
        'buttons': [
            {
                'text': 'Назад',
                'text_en': 'Back',
                'text_ua': 'Повернутися',
                'row': 0,
                'reply': True
            },
            {
                'text': '⬅️ Меню',
                'text_en': '⬅️ Menu',
                'text_ua': '⬅️ Меню',
                'row': 0,
                'reply': True
            }
        ]
    },
    'DocumentStart': {
        'text': 'Начинаю проверку готовности документа...',
        'text_en': 'I start checking the readiness of the document...',
        'text_ua': 'Починаю перевірку готовності документа...',
        'buttons': [
            {
                'text': '⬅️ Меню',
                'text_en': '⬅️ Menu',
                'text_ua': '⬅️ Меню',
                'row': 0,
                'reply': True
            }
        ]
    },
    'DocumentsResult': {
        'text': '{status}',
        'text_en': '{status}',
        'text_ua': '{status}',
        'buttons': [
            {
                'text': 'Подписаться на изменения статуса',
                'text_en': 'Subscribe to status updates',
                'text_ua': 'Підписатися на зміни статусу',
                'row': 0,
                'callback_data': 'doc_{doc_id}'
            },
            {
                'text': '↩️ Меню',
                'text_en': '↩️ Menu',
                'text_ua': '↩️ Меню',
                'row': 1,
                'callback_data': 'menu'
            }
        ]
    },
    'DocumentsSubscribe': {
        'text': 'Подписка проверку готовности документов оформлена!'
                '\n\nКогда будут новые события - мы сообщим вас',
        'text_en': 'Subscription to check the readiness of documents is issued!'
                   '\n\nWhen there are new events - we will notify you',
        'text_ua': 'Підписка на перевірку готовності документів оформлена!'
                   '\n\nКоли будуть нові події – ми повідомимо вас',
    },
    'Documents_verification': {
        'text': 'Данная функция поможет вам проверять подлинность и '
                'действительность интересующего вас документа, '
                'что предупредит вас от возможных неприятных ситуаций при '
                'пересечении украинской границы и в иных случаях.'
                '\n\nВыберите тип документа, который нужно проверить 👇',
        'text_en': 'This function will help you check the authenticity and '
                   'validity of the document you are interested in, '
                   'which will warn you from possible unpleasant situations '
                   'when crossing the Ukrainian border and in other cases.'
                   '\n\nSelect the type of document you want to check 👇',
        'text_ua': 'Дана функція допоможе вам перевіряти справжність і '
                   'дійсність документа, що вас цікавить, що попередить вас '
                   'від можливих неприємних ситуацій при перетині '
                   'українського кордону та в інших випадках.'
                   '\n\nВиберіть тип документа, який потрібно перевірити 👇',
        'buttons': [
            {
                'text': 'Выбрать',
                'text_en': 'Select',
                'text_ua': 'Вибрати',
                'row': 0,
                'inline_mode': True
            },
            {
                'text': '↩️ Назад',
                'text_en': '↩️ Back',
                'text_ua': '↩️ Назад',
                'row': 1,
                'callback_data': 'monitoring_back'
            }
        ]
    },
    'InactiveTypes': {
        'text': 'Тип документа, изготовление которого нужно проверить',
        'text_en': 'Тип документа, изготовление которого нужно проверить',
        'text_ua': 'Тип документа, изготовление которого нужно проверить',
        'buttons': [
            {
                'text': 'ID Паспорт',
                'text_en': 'ID passport',
                'text_ua': 'ID Паспорт',
                'callback_data': '2',
            },
            {
                'text': 'Паспорт Украины в виде книги',
                'text_en': 'Passport of Ukraine in the form of a book',
                'text_ua': 'Паспорт України у вигляді книги',
                'callback_data': '1',
            },
            {
                'text': 'Загран Паспорт',
                'text_en': 'International passport',
                'text_ua': 'Закордонний Паспорт',
                'callback_data': '3',
            },
            {
                'text': 'Временное удостоверение гражданина Украины',
                'text_en': 'Temporary certificate of a citizen of Ukraine',
                'text_ua': 'Тимчасове посвідчення громадянина України',
                'callback_data': '5',
            },
            {
                'text': 'Удостоверение лица без гражданства для выезда за'
                        ' границу',
                'text_en': 'Certificate of a stateless person for traveling abroad',
                'text_ua': 'Посвідчення особи без громадянства для виїзду за кордон',
                'callback_data': '6',
            },
            {
                'text': 'Удостоверение на временное жительство',
                'text_en': 'Temporary Residence Certificate',
                'text_ua': 'Посвідчення на тимчасове проживання',
                'callback_data': '8',
            },
            {
                'text': 'Удостоверение на временное жительство'
                        ' (биометрическое)',
                'text_en': 'Temporary residence permit (biometric)',
                'text_ua': 'Посвідчення на тимчасове проживання (біометричне)',
                'callback_data': '16',
            },
            {
                'text': 'Удостоверение на постоянное жительство',
                'text_en': 'Permanent Residence Certificate',
                'text_ua': 'Посвідчення на постійне проживання',
                'callback_data': '7',
            },
            {
                'text': 'Удостоверение на постоянное жительство'
                        ' (биометрическое)',
                'text_en': 'Permanent residence card (biometric)',
                'text_ua': 'Посвідчення на постійне проживання (біометричне)',
                'callback_data': '15',
            },
            {
                'text': 'Удостоверение беженца',
                'text_en': 'Refugee ID',
                'text_ua': 'Посвідчення біженця',
                'callback_data': '10',
            },
            {
                'text': 'Проездной документ беженца',
                'text_en': 'Refugee travel document',
                'text_ua': 'Проїзний документ біженця',
                'callback_data': '11',
            },
            {
                'text': 'Удостоверение личности, которая нуждается в'
                        ' дополнительной защите',
                'text_en': 'Identity card that needs additional protection',
                'text_ua': 'Посвідчення особи, яка потребує додаткового'
                           ' захисту',
                'callback_data': '12',
            },
            {
                'text': 'Проездной документ лица, которому предоставлена'
                        ' дополнительная защита',
                'text_en': 'Travel document of a person who has been granted'
                           ' subsidiary protection',
                'text_ua': 'Проїзний документ особи, якій надано'
                           ' додатковий захист',
                'callback_data': '13',
            },
            {
                'text': 'Проездной документ ребенка',
                'text_en': 'Child\'s travel document',
                'text_ua': 'Проїзний документ дитини',
                'callback_data': '14',
            },
        ]
    },
    'InactiveSeries': {
        'text': 'Введите серию документа, на основании которого '
                'осуществляется проверка',
        'text_en': 'Enter the series of the document on the basis of which '
                   'the verification is carried out',
        'text_ua': 'Введіть серію документа, на підставі якого здійснюється '
                   'перевірка',
        'buttons': [
            {
                'text': 'Назад',
                'text_en': 'Back',
                'text_ua': 'Повернутися',
                'row': 0,
                'reply': True
            }
        ]
    },
    'InactiveNumber': {
        'text': 'Введите номер документа, на основании которого '
                'осуществляется проверка',
        'text_en': 'Enter the number of the document on the basis of which '
                   'the verification is carried out',
        'text_ua': 'Введіть номер документа, на підставі якого здійснюється '
                   'перевірка',
        'buttons': [
            {
                'text': 'Назад',
                'text_en': 'Back',
                'text_ua': 'Повернутися',
                'row': 0,
                'reply': True
            }
        ]
    },
    'InactiveStart': {
        'text': 'Начинаю проверку недействительного документа...',
        'text_en': 'Starting a check for an invalid document...',
        'text_ua': 'Починаю перевірку недійсного документа...',
        'buttons': [
            {
                'text': '⬅️ Меню',
                'text_en': '⬅️ Menu',
                'text_ua': '⬅️ Меню',
                'row': 0,
                'reply': True
            }
        ]
    },
    'InactiveResult': {
        'text': '{status}',
        'text_en': '{status}',
        'text_ua': '{status}',
        'buttons': [
            {
                'text': 'Подписаться на изменения статуса',
                'text_en': 'Subscribe to status updates',
                'text_ua': 'Підписатися на зміни статусу',
                'row': 0,
                'callback_data': 'inactive_{doc_id}'
            },
            {
                'text': '↩️ Меню',
                'text_en': '↩️ Menu',
                'text_ua': '↩️ Меню',
                'row': 1,
                'callback_data': 'menu'
            }
        ]
    },
    'InactiveSubscribe': {
        'text': 'Подписка на проверку по базе недействительных документов '
                'оформлена!'
                '\n\nКогда будут новые события - мы сообщим вас',
        'text_en': 'Subscription to check against the database of invalid '
                   'documents has been issued!'
                   '\n\nWhen there are new events - we will notify you',
        'text_ua': 'Підписка на перевірку на базі недійсних документів '
                   'оформлена!'
                   '\n\nКоли будуть нові події – ми повідомимо вас',
    },
    'StateRegisters': {
        'text': '<b>Список реестров:</b>'
                '\n-Документы в судебном реестре и Поиск по судебным делам (/detail_court);'
                '\n-Список судебных дел, предназначенных для рассмотрения (/detail_court_assign);'
                '\n-расчеты налогоплательщиков с бюджетом (/detail_debtors);'
                '\n-система выполнения производств и Единый реестр должников (/detail_asvp);'
                '\n-лица, находящиеся в розыске (/detail_wanted).'
                '\n\nДля получения информации обо всех видах реестров и для '
                'чего их нужно мониторить, перейдите в меню "О Государственных реестрах"'
                '\n\nЧтобы начать мониторинг, нажми "Искать по всем" или выбери реестр 👇',
        'text_en': 'List of registers:'
                   '\n-Documents in the court register and Search in court cases (/detail_court);'
                   '\n-List of court cases scheduled for consideration (/detail_court_assign);'
                   '\n-Calculations of taxpayers with the budget (/detail_debtors);'
                   '\n-System of proceedings and the Unified Register of Debtors (/detail_asvp);'
                   '\n-Persons wanted (/detail_wanted).'
                   '\n\nFor information on all types of registers, and why '
                   'they need to be monitored, go to the menu "About State Registers"'
                   '\n\nTo start monitoring, click "Search all" or select a register 👇',
        'text_ua': '<b>Список реєстрів:</b>'
                   '\n-Документи у судовому реєстрі та Пошук у судових справах (/detail_court);'
                   '\n-Список судових справ, призначених до розгляду (/detail_court_assign);'
                   '\n-Розрахунки платників податків з бюджетом (/detail_debtors);'
                   '\n-Система виконання проваджень та Єдиний реєстр боржників (/detail_asvp);'
                   '\n-Особи, які у розшуку (/detail_wanted).'
                   '\n\n Для отримання інформації про всі види реєстрів, та'
                   ' для чого їх потрібно моніторити, прейдіть в меню "Про Державні реєстри"'
                   '\n\nЩоб розпочати моніторинг натисни "Шукати по всім" або обери реєстр 👇',
        'buttons': [
            {
                'text': '🔎 Искать по всем',
                'text_en': '🔎 Search all',
                'text_ua': '🔎 Шукати по всім',
                'row': 0,
                'reply': True
            },
            {
                'text': 'О Государственных реестрах',
                'text_en': 'About State Registers',
                'text_ua': 'Про Державні реєстри',
                'row': 0,
                'reply': True
            },
            {
                'text': 'Судебные дела',
                'text_en': 'Court cases',
                'text_ua': 'Судові Справи',
                'row': 1,
                'reply': True
            },
            {
                'text': 'Судебные рассмотрения',
                'text_en': 'Court assignments',
                'text_ua': 'Судові розгляди',
                'row': 1,
                'reply': True
            },
            {
                'text': 'Должники',
                'text_en': 'Debtors',
                'text_ua': 'Боржники',
                'row': 2,
                'reply': True
            },
            {
                'text': 'Исполнительные производства',
                'text_en': 'Executive proceedings',
                'text_ua': 'Виконавчі провадження',
                'row': 2,
                'reply': True
            },
            {
                'text': 'Розыск',
                'text_en': 'Wanted',
                'text_ua': 'Розшук',
                'row': 3,
                'reply': True
            },
            {
                'text': '⬅️ Назад',
                'text_en': '⬅️ Back',
                'text_ua': '⬅️ Повернутися',
                'row': 4,
                'reply': True
            },
            {
                'text': 'Меню',
                'text_en': 'Menu',
                'text_ua': 'Меню',
                'row': 4,
                'reply': True
            }
        ]
    },
    'AboutStateRegisters': {
        'text': '\n<b>📌Документы в судебном реестре и Поиск по судебным '
                'делам.</b>'
                '\nДанные реестры будут всегда держать вас в курсе '
                'относительно вызовов в судебные органы Украины,'
                ' открытых гражданских, уголовных или других судебных'
                ' процессов и обезопасит вас от получения нежелательного'
                ' судебного решения, что при отсутствии своевременного'
                ' обращения, может повлечь негативные последствия для'
                ' законного пребывания в Украине.'
                '\n<b>📌Расчет налогоплательщиков с бюджетом.</b>'
                '\nДанный реестр, оповестит вас о возникшей налоговой '
                'задолженности по интересующему вас юридическому лицу и'
                ' при своевременном реагировании поможет вам избежать'
                ' возникновения штрафных санкций и последующего'
                ' административного взыскания, что может привести к'
                ' негативным последствиям законного пребывания на'
                ' территории Украины.'
                '\n<b>📌Система выполнения производств и Единый реестр '
                'должников.</b>'
                '\nДанный реестр, оповестит вас об исполнительных '
                'производствах и позволит вам своевременно устранить'
                ' возникшие обязательства без негативных последствий для'
                ' законного пребывания на территории Украины'
                ' (штрафы, судебные решения и др.)'
                '\n<b>📌Лица, которые находятся в розыске.</b>'
                '\nС помощью данного реестра, вы сможете проверить'
                ' интересующего вас человека, не находится ли он в розыске'
                ' за совершение уголовных преступлений.',
        'text_en': '\n<b>📌Documents in the court registry and search for'
                   ' court cases.</b>'
                   '\nThese registries will always keep you informed about '
                   'summons to the judicial authorities of Ukraine,'
                   ' open civil, criminal or other legal proceedings and'
                   ' will protect you from receiving an unwanted court'
                   ' decision, which, if not applied in a timely manner,'
                   ' may lead to negative consequences for your legal stay'
                   ' in Ukraine.'
                   '\n<b>📌 Calculation of taxpayers with the budget.</b>'
                   'This registry will notify you of the tax debt that'
                   ' has arisen for the legal entity you are interested in'
                   ' and, with a timely response, will help you avoid'
                   ' penalties and subsequent administrative penalties,'
                   ' which can lead to negative consequences of legal stay'
                   ' on the territory of Ukraine.'
                   '\n<b>📌Proceedings execution system and the Unified'
                   ' Register of Debtors.</b>'
                   '\nThis register will notify you of enforcement'
                   ' proceedings and allow you to timely eliminate the'
                   ' obligations that have arisen without negative'
                   ' consequences for the legal stay on the territory'
                   ' of Ukraine (fines, court decisions, etc.)'
                   '\n<b>📌Persons who are wanted.</b>'
                   '\nWith the help of this registry, you can check the'
                   ' person you are interested in, whether he is wanted'
                   ' for criminal offenses.',
        'text_ua': '\n<b>📌Документи в судовому реєстрі та Пошук у судових справах.</b>'
                   '\nДані реєстри завжди будуть тримати вас в курсі щодо '
                   'викликів до судових органів України, відкритих цивільних,'
                   ' кримінальних чи інших судових процесів та убезпечить'
                   ' вас від отримання небажаного судового рішення,'
                   ' що за відсутності своєчасного звернення може призвести'
                   ' до негативних наслідків для законного перебування'
                   ' в Україні.'
                   '\n<b>📌Розрахунок платників податків із бюджетом.</b>'
                   '\nДаний реєстр, повідомить вас про податкову '
                   'заборгованість, що вас зацікавила, юридична особа,'
                   ' що вас цікавить, і при своєчасному реагуванні допоможе'
                   ' вам уникнути виникнення штрафних санкцій і подальшого'
                   ' адміністративного стягнення, що може призвести до'
                   ' негативних наслідків законного перебування на'
                   ' території України.'
                   '\n<b>📌Система виконання виробництв та Єдиний реєстр '
                   'боржників.</b>'
                   '\nДаний реєстр, повідомить вас про виконавчі провадження '
                   'і дозволить вам своєчасно усунути зобов\'язання,'
                   ' що виникли, без негативних наслідків для законного'
                   ' перебування на території України'
                   ' (штрафи, судові рішення та ін.)'
                   '\n<b>📌Обличчя, які знаходяться в розшуку.</b>'
                   '\nЗа допомогою даного реєстру, ви зможете перевірити '
                   'людину, яка вас цікавить, чи не знаходиться вона в'
                   ' розшуку за скоєння кримінальних злочинів.',
        'buttons': [
            {
                'text': '🔎 Искать по всем',
                'text_en': '🔎 Search all',
                'text_ua': '🔎 Шукати по всім',
                'row': 0,
                'callback_data': 'national_search'
            },
            {
                'text': '⬅️ Назад',
                'text_en': '⬅️ Back',
                'text_ua': '⬅️ Повернутися',
                'row': 1,
                'callback_data': 'monitoring_back'
            },
            {
                'text': 'Меню',
                'text_en': 'Menu',
                'text_ua': 'Меню',
                'row': 1,
                'callback_data': 'menu'
            }
        ]
    },
    'MonitoringNational': {
        'text': 'Введите Фамилию Имя Отчество человека на украинском языке.',
        'text_en': 'Enter the Last Name First Name of the person in Ukrainian',
        'text_ua': 'Введіть Прізвище Ім\'я По-батькові людини українською мовою.',
        'buttons': [
            {
                'text': 'Применить: {name}',
                'text_en': 'Apply: {name}',
                'text_ua': 'Застосувати: {name}',
                'row': 0,
                'reply': True
            },
            {
                'text': '⬅️ Меню',
                'text_en': '⬅️ Menu',
                'text_ua': '⬅️ Меню',
                'row': 1,
                'reply': True
            }
        ]

    },
    'CourtDetail': {
        'text': '<b>📌Документы в судебном реестре и Поиск по судебным '
                'делам.</b>'
                '\nДанные реестры будут всегда держать вас в курсе '
                'относительно вызовов в судебные органы Украины,'
                ' открытых гражданских, уголовных или других судебных'
                ' процессов и обезопасит вас от получения нежелательного'
                ' судебного решения, что при отсутствии своевременного'
                ' обращения, может повлечь негативные последствия'
                ' для законного пребывания в Украине.',
        'text_en': '<b>📌Documents in the court registry and search for'
                   ' court cases.</b>'
                   '\nThese registries will always keep you informed about '
                   'summons to the judicial authorities of Ukraine,'
                   ' open civil, criminal or other legal proceedings'
                   ' and will protect you from receiving an unwanted'
                   ' court decision, which, if not applied in a timely'
                   ' manner, may lead to negative consequences for your'
                   ' legal stay in Ukraine.',
        'text_ua': '<b>📌Документи в судовому реєстрі та Пошук у судових '
                   'справах.</b>'
                   '\nДані реєстри будуть завжди тримати вас в курсі щодо '
                   'викликів до судових органів України, відкритих цивільних,'
                   ' кримінальних або інших судових процесів та убезпечить'
                   ' вас від отримання небажаного судового рішення,'
                   ' що за відсутності своєчасного звернення може '
                   'призвести до негативних наслідків для законного'
                   ' перебування в Україні.',
    },
    'AssignDetail': {
        'text': '<b>📌Список судебных дел, предназначенных для рассмотрения</b>'
                '\nДанный реестры будут всегда держать вас в курсе '
                'относительно вызовов в судебные органы Украины',
        'text_en': '<b>📌List of court cases scheduled for consideration</b>'
                   '\nThese registries will always keep you informed about '
                   'summons to the judicial authorities of Ukraine',
        'text_ua': '<b>📌Список судових справ, призначених до розгляду</b>'
                   '\nДані реєстри будуть завжди тримати вас в курсі щодо '
                   'викликів до судових органів України',
    },
    'DebtorsDetail': {
        'text': '<b>📌Расчет налогоплательщиков с бюджетом.</b>'
                '\nДанный реестр, оповестит вас о возникшей налоговой '
                'задолженности по интересующему вас юридическому лицу'
                ' и при своевременном реагировании поможет вам избежать'
                ' возникновения штрафных санкций и последующего'
                ' административного взыскания, что может привести'
                ' к негативным последствиям законного пребывания'
                ' на территории Украины.',
        'text_en': '<b>📌 Calculation of taxpayers with the budget.</b>'
                   '\bThis registry will notify you of the tax debt that has'
                   ' arisen for the legal entity you are interested in and,'
                   ' with a timely response, will help you avoid penalties'
                   ' and subsequent administrative penalties, which can'
                   ' lead to negative consequences of legal stay on the'
                   ' territory of Ukraine.',
        'text_ua': '<b>📌Розрахунок платників податків із бюджетом.</b>'
                   '\nДаний реєстр, повідомить вас про податкову '
                   'заборгованість за юридичною особою, що вас цікавить,'
                   ' і при своєчасному реагуванні допоможе вам уникнути'
                   ' виникнення штрафних санкцій і подальшого'
                   ' адміністративного стягнення, що може призвести до'
                   ' негативних наслідків законного перебування'
                   ' на території України.',
    },
    'AsvpDetail': {
        'text': '<b>📌Система выполнения производств и Единый реестр '
                'должников.</b>'
                '\nДанный реестр, оповестит вас об исполнительных '
                'производствах и позволит вам своевременно устранить'
                ' возникшие обязательства без негативных последствий'
                ' для законного пребывания на территории Украины'
                ' (штрафы, судебные решения и др.)',
        'text_en': '<b>📌Proceedings execution system and the Unified'
                   ' Register of Debtors.</b>'
                   '\nThis register will notify you of enforcement '
                   'proceedings and allow you to timely eliminate the '
                   'obligations that have arisen without negative '
                   'consequences for the legal stay on the territory of '
                   'Ukraine (fines, court decisions, etc.)',
        'text_ua': '<b>📌Система виконання виробництв та Єдиний реєстр '
                   'боржників.</b>'
                   '\nДаний реєстр, повідомить вас про виконавчі провадження '
                   'і дозволить вам своєчасно усунути зобов\'язання,'
                   ' що виникли, без негативних наслідків для законного'
                   ' перебування на території України (штрафи, судові '
                   'рішення та ін.)'
    },
    'WantedDetail': {
        'text': '<b>📌Лица, которые находятся в розыске.</b>'
                '\nС помощью данного реестра, вы сможете проверить'
                ' интересующего вас человека, не находится ли он в розыске'
                ' за совершение уголовных преступлений.',
        'text_en': '<b>📌Persons who are wanted.</b>'
                   '\nWith the help of this registry, you can check the'
                   ' person you are interested in, whether he is wanted'
                   ' for criminal offenses.',
        'text_ua': '<b>📌Обличчя, які знаходяться в розшуку.</b>'
                   '\nЗа допомогою даного реєстру, ви зможете перевірити '
                   'людину, яка вас цікавить, чи не знаходиться вона в'
                   ' розшуку за скоєння кримінальних злочинів.',
    },
    'MonitoringStart': {
        'text': 'Мониторинг начался',
        'text_en': 'Monitoring has begun',
        'text_ua': 'Моніторинг розпочався',
        'buttons': [
            {
                'text': '⬅️ Меню',
                'text_en': '⬅️ Menu',
                'text_ua': '⬅️ Меню',
                'row': 1,
                'reply': True
            }
        ]
    },
    'MonitoringSaveSearch': {
        'text': 'Чтобы сохранить поисковые парметры нажми ниже "Сохранить поиск"',
        'text_en': 'To save your search parameters, click "Save Search" below.',
        'text_ua': 'Щоб зберегти пошукові парметри, натисніть нижче "Зберегти пошук"',
        'buttons': [
            {
                'text': 'Сохранить поиск',
                'text_en': 'Save Search',
                'text_ua': 'Зберегти пошук',
                'row': 1,
                'callback_data': 'save#{search_id}#{obj_id}'
            }
        ]
    },
    'MonitoringInProgress': {
        'text': 'Процесс поиска в процессе',
        'text_en': 'The search process continues',
        'text_ua': 'Процес пошуку триває',
    },
    'MonitoringIsDelayed': {
        'text': 'Поиск потребует больше времени чем всегда',
        'text_en': 'The search takes longer than usual.',
        'text_ua': 'Пошук потребує більше часу ніж зазвичай.',
    },
    'NationalResult': {
        'text': 'Вот что мне удалось найти по запросу: <b>{full_name}</b>'
                '\nДокументов в судебном реестре - {court_count} {court}'
                '\nДокументов в судебном рассмотрения - {court_assign_count} {court_assign}'
                '\nЛица, которые в розыске - {mvs_count} {mvs}'
                '\nЕдиный реестр должников - {debtors_count} {debtors}'
                '\nСистема автоматизированного производства - {asvp_count} '
                '{asvp}',
        'text_en': 'Here is what I was able to find on request: <b>{'
                   'full_name}</b>'
                   '\nDocuments in the court register - {court_count} {court}'
                   '\nDocuments in court assignments - {court_assign_count} {court_assign}'
                   '\nPersons who are wanted - {mvs_count} {mvs}'
                   '\nUnified register of debtors - {debtors_count} {debtors}'
                   '\nAutomated production system - {asvp_count} {asvp}',
        'text_ua': 'Ось що мені вдалося знайти на запит: <b>{full_name}</b>'
                   '\nДокументів у судовому реєстрі - {court_count} {court}'
                   '\nДокументів у судовому розгляду - {court_assign_count} {court_assign}'
                   '\nОсоби, які у розшуку - {mvs_count} {mvs}'
                   '\nЄдиний реєстр боржників - {debtors_count} {debtors}'
                   '\nСистема автоматизованого виробництва - {asvp_count} '
                   '{asvp}',
    },
    'NationalResultSubs': {
        'text': 'Если вы хотите следить в судебном и других реестрах по'
                ' информации по запросу {full_name}, то вы можете',
        'text_en': 'If you want to follow the information in the judicial'
                   ' and other registries at the request of {full_name},'
                   ' then you can',
        'text_ua': 'Якщо ви хочете стежити в судовому та інших реєстрах'
                   ' за інформацією на запит {full_name}, то ви можете',
        'buttons': [
            {
                'text': 'Подписаться',
                'text_en': 'Subscribe',
                'text_ua': 'Підписатися',
                'row': 0,
                'callback_data': 'national_{search_id}'
            }
        ]
    },
    'NationalNotFound': {
        'text': 'Поиск не принес результатов по запросу "<b>{full_name}</b>"',
        'text_en': 'Your search did not return any results'
                   ' "<b>{full_name}</b>"',
        'text_ua': 'Пошук не приніс результатів за запитом'
                   ' "<b>{full_name}</b>"'
    },

    'CourtDetailSearch': {
        'text': 'В едином реестре судебных решений по запросу {full_name}'
                ' найдено {count} судебных документов',
        'text_en': '{count} court documents were found in the Unified Register'
                   ' of Court Decisions at the request of {full_name}',
        'text_ua': 'В єдиному реєстрі судових рішень на запит {full_name}'
                   ' знайдено {count} судових документів',
        'buttons': [
            {
                'text': 'Смотреть',
                'text_en': 'View',
                'text_ua': 'Дивитися',
                'row': 0,
                'callback_data': 'show_result'
            },
        ]
    },

    'CourtDetailElem': {
        'text': 'Суд: {court}'
                '\nНомер Дела: {number}'
                '\nФорма судопроизводства: {form}'
                '\nСтороны спора: {claimant}',
        'text_en': 'Court: {court}'
                   '\nCase Number: {number}'
                   '\nJudicial Form: {form}'
                   '\nDisputing Parties: {claimant}',
        'text_ua': 'Суд: {court}'
                   '\nНомер Справи: {number}'
                   '\nФорма судочинства: {form}'
                   '\nСторони суперечки: {claimant}',
        'buttons': [
            {
                'text': 'Посмотреть решения по делу',
                'text_en': 'View case decisions',
                'text_ua': 'Подивитися рішення у справі',
                'row': 0,
                'callback_data': 'v#{court_id}'
            },
            {
                'text': 'Подписаться',
                'text_en': 'Subscribe',
                'text_ua': 'Підписатися',
                'row': 1,
                'callback_data': 'subs#{court_sub}'
            },
            {
                'text': 'Показать еще',
                'text_en': 'Show more',
                'text_ua': 'Показати ще',
                'row': 2,
                'callback_data': 'next#{page}'
            }
        ]
    },
    'CourtResultDetail': {
        'text': '<b>Дата принятие решение:</b> {date_approval}'
                '\n<b>Номер решения:</b> {number}'
                '\n<b>Cудья:</b> {chairmen}'
                '\n<b>Форма судебного решения:</b> {form}'
                '\n<b>Форма судопроизводства:</b> {court_type}',
        'text_en': '<b>Approval date:</b> {date_approval}'
                   '\n<b>Solution number:</b> {number}'
                   '\n<b>Judge:</b> {chairmen}'
                   '\n<b>Judgment Form:</b> {form}'
                   '\n<b>Court Form:</b> {court_type}',
        'text_ua': '<b>Дата прийняття рішення:</b> {date_approval}'
                   '\n<b>Номер рішення:</b> {number}'
                   '\n<b>Суддя:</b> {chairmen}'
                   '\n<b>Форма судового рішення:</b> {form}'
                   '\n<b>Форма судочинства:</b> {court_type}',
        'buttons': [
            {
                'text': 'Посмотреть решение',
                'text_en': 'View Solution',
                'text_ua': 'Переглянути рішення',
                'row': 0,
                'url': '{link}',
                'url_en': '{link}',
                'url_ua': '{link}'
            }
        ]
    },
    'SubscribeCourt': {
        'text': 'Подписка на поиск в реестре судебных решений оформлена!'
                '\n\nКогда будут новые события - мы сообщим вас',
        'text_en': 'Subscription to the search in the register of judgments has been issued!'
                   '\n\nWhen there are new events - we will notify you',
        'text_ua': 'Підписка на пошук у реєстрі судових рішень оформлена!'
                   '\n\nКоли будуть нові події - ми повідомимо вас'
    },
    'CourtAssignSearch': {
        'text': 'В едином реестре судебных решений по запросу {full_name} найдено {count} судебных дел которые назначенные к рассмотрению',
        'text_en': 'In the unified register of court decisions, at the request of {full_name}, {count} court cases were found that are scheduled for consideration',
        'text_ua': 'В єдиному реєстрі судових рішень на запит {full_name} знайдено {count} судових справ, які призначені до розгляду',
        'buttons': [
            {
                'text': 'Смотреть',
                'text_en': 'View',
                'text_ua': 'Дивитися',
                'row': 0,
                'callback_data': '{show_call}'
            },
            {
                'text': 'Подписаться',
                'text_en': 'Subscribe',
                'text_ua': 'Підписатися',
                'row': 1,
                'callback_data': 'subs#{id_sub}'
            }
        ]
    },
    'CourtAssignDetail': {
        'text': '<b>Дата рассмотрения:</b> {dt_meet}'
                '\n<b>Состав судей:</b> {judges}'
                '\n<b>Номер дела:</b> {number}'
                '\n<b>Суд:</b> {name_court}'
                '\n<b>Зал судебных заседани:</b> {room_court}'
                '\n<b>Стороны по делу:</b> {involved}'
                '\n<b>Суть Дела:</b> {description}'
                '\n<b>Адрес:</b> {address}',
        'text_en': '<b>Consideration date:</b> {dt_meet}'
                   '\n<b>Judges:</b> {judges}'
                   '\n<b>Case number:</b> {number}'
                   '\n<b>Court:</b> {name_court}'
                   '\n<b>Court room:</b> {room_court}'
                   '\n<b>Parties To The Case:</b> {involved}'
                   '\n<b>Description:</b> {description}'
                   '\n<b>Address:</b> {address}',
        'text_ua': '<b>Дата розгляду:</b> {dt_meet}'
                   '\n<b>Склад суду:</b> {judges}'
                   '\n<b>Номер справи:</b> {number}'
                   '\n<b>Суд:</b> {name_court}'
                   '\n<b>Зал судових засідань:</b> {room_court}'
                   '\n<b>Сторони у справі:</b> {involved}'
                   '\n<b>Суть справи:</b> {description}'
                   '\n<b>Адреса:</b> {address}',
        'buttons': [
            {
                'text': 'Показать еще',
                'text_en': 'Show more',
                'text_ua': 'Показати ще',
                'callback_data': 'next#{page}'
            }
        ]
    },
    'CourtAssignSubscribe': {
        'text': 'Подписка на поиск в реестре судебных дел, предназначенных для рассмотрения оформлена!'
                '\n\nКогда будут новые события - мы сообщим вас',
        'text_en': 'The subscription to the search in the register of court cases scheduled for review has been completed!'
                   '\n\nWhen there are new events - we will notify you',
        'text_ua': 'Підписка на пошук у реєстрі судових справ, призначених до розгляду оформлена!'
                   '\n\nКоли будуть нові події - ми повідомимо вас'
    },
    'WantedDetailSearch': {
        'text': 'В реестре министерства внутренних дел по запросу {full_name}'
                ' найдено {count} результатов',
        'text_en': 'In the register of the Ministry of Internal Affairs,'
                   ' {full_name} found {count} results',
        'text_ua': 'У реєстрі міністерства внутрішніх справ за запитом'
                   ' {full_name} знайдено {count} результатів',
        'buttons': [
            {
                'text': 'Смотреть',
                'text_en': 'View',
                'text_ua': 'Дивитися',
                'row': 0,
                'callback_data': '{show_data}'
            }
        ]
    },
    'WantedDetailElem': {
        'text': 'Регион: {region}'
                '\nКатегория: {category}'
                '\nДата исчезновения: {disappearance}'
                '\nСтатья обвинений: {accusations}'
                '\nДата рождения: {birth}'
                '\nМера пресечения: {precaution}',
        'text_en': 'Region: {region}'
                   '\nCategory: {category}'
                   '\nDisappearance date: {disappearance}'
                   '\nAccusations article: {accusations}'
                   '\nDate of birth: {birth}'
                   '\nPrecaution: {precaution}',
        'text_ua': 'Регіон: {region}'
                   '\nКатегорія: {category}'
                   '\nДата зникнення: {disappearance}'
                   '\nСтаття звинувачень: {accusations}'
                   '\nДата народження: {birth}'
                   '\nЗапобіжний захід: {precaution}',
        'buttons': [
            {
                'text': 'Посмотреть',
                'text_en': 'View',
                'text_ua': 'Переглянути',
                'row': 0,
                'url': '{link}',
                'url_en': '{link}',
                'url_ua': '{link}'
            },
            {
                'text': 'Подписаться',
                'text_en': 'Subscribe',
                'text_ua': 'Підписатися',
                'row': 1,
                'callback_data': 'subs#{mvs_id}'
            },
            {
                'text': 'Показать еще',
                'text_en': 'Show more',
                'text_ua': 'Показати ще',
                'row': 2,
                'callback_data': 'next#{page}'
            }
        ]
    },
    'SubscribeWanted': {
        'text': 'Подписка на поиск в реестре министерства внутренних'
                ' дел оформлена!'
                '\n\nКогда будут новые события - мы сообщим вас',
        'text_en': 'Subscription to the search in the register of the'
                   ' Ministry of the Interior has been issued!'
                   '\n\nWhen there are new events - we will notify you',
        'text_ua': 'Підписка на пошук у реєстрі міністерства внутрішніх '
                   'справ оформлена!'
                   '\n\nКоли будуть нові події - ми повідомимо вас'
    },
    'DebtorsDetailSearch': {
        'text': 'В едином реестре должников по запросу {full_name} '
                'найдено {count} результатов',
        'text_en': '{count} results were found in the unified register of debtors for {full_name}',
        'text_ua': 'В єдиному реєстрі боржників за запитом {full_name}'
                   ' знайдено {count} результатів',
        'buttons': [
            {
                'text': 'Смотреть',
                'text_en': 'View',
                'text_ua': 'Дивитися',
                'row': 0,
                'callback_data': '{show_data}'
            },
            {
                'text': 'Отписаться',
                'text_en': 'Unsubscribe',
                'text_ua': 'Відписатися',
                'row': 1,
                'callback_data': 'debt_u#{subs_id}'
            },
            {
                'text': 'Подписаться',
                'text_en': 'Subscribe',
                'text_ua': 'Підписатися',
                'row': 1,
                'callback_data': 'subs#{deb_id}'
            }
        ]
    },
    'DebtorsDetailElem': {
        'text': '<b>Дата рождения:</b> {birth}'
                '\n<b>Документ выдан: {publisher}'
                '\n<b>Связь:</b> {connection}'
                '\n<b>ВП номер:</b> {number}'
                '\n<b>Категория взысканий:</b> {deduction}',
        'text_en': '<b>Date of birth:</b> {birth}'
                   '\n<b>Document issued by:</b> {publisher}'
                   '\n<b>Connection:</b> {connection}'
                   '\n<b>VP number:</b> {number}'
                   '\n<b>Deduction Category:</b> {deduction}',
        'text_ua': '<b>Дата народження:</b> {birth}'
                   '\n<b>Документ видано:</b> {publisher}'
                   '\n<b>Зв\'язок:</b> {connection}'
                   '\n<b>ВП номер:</b> {number}'
                   '\n<b>Категорія стягнень:</b> {deduction}',
        'buttons': [
            {
                'text': 'Показать еще',
                'text_en': 'Show more',
                'text_ua': 'Показати ще',
                'row': 0,
                'callback_data': 'next#{page}'
            }
        ]
    },
    'SubscribeDebtors': {
        'text': 'Подписка на поиск в едином реестре должников оформлена!'
                '\n\nКогда будут новые события - мы сообщим вас',
        'text_en': 'Subscription to search in the unified register of debtors is issued!'
                   '\n\nWhen there are new events - we will notify you',
        'text_ua': 'Підписка на пошук у єдиному реєстрі боржників оформлена!'
                   '\n\nКоли будуть нові події - ми повідомимо вас'
    },
    'UnSubscribeDebtors': {
        'text': 'Подписка на поиск в едином реестре по запросу {full_name} должников отменена!',
        'text_en': 'The subscription to the search in the unified registry at the request of {full_name} debtors has been cancelled!',
        'text_ua': 'Підписка на пошук в єдиному реєстрі на запит {full_name} боржників скасована!',
        'buttons': [
            {
                'text': 'Подписаться',
                'text_en': 'Subscribe',
                'text_ua': 'Підписатися',
                'row': 1,
                'callback_data': 'subs#{deb_id}'
            }
        ]
    },
    'AsvpDetailSearch': {
        'text': 'В автоматизированной системе исполнительного производства'
                ' по запросу {full_name} найдено {count} результатов',
        'text_en': '{count} results were found in the automated system of enforcement proceedings for {full_name}',
        'text_ua': 'В автоматизованій системі виконавчого провадження за'
                   ' запитом {full_name} знайдено {count} результатів',
        'buttons': [
            {
                'text': 'Смотреть',
                'text_en': 'View',
                'text_ua': 'Дивитися',
                'row': 0,
                'callback_data': '{show_data}'
            }
        ]
    },
    'AsvpDetailElem': {
        'text': '<b>Коллектор:</b> {creditors_name}'
                '\n<b>Исполнитель:</b> {agency}'
                '\n<b>Дата открытия:</b> {date_open}'
                '\n<b>Дата рождения:</b> {birth}'
                '\n<b>Должник:</b> {debtors}'
                '\n<b>АСВП номер:</b> {number}'
                '\n<b>Cтатус:</b> {status}',
        'text_en': '<b>Collector:</b> {creditors_name}'
                   '\n<b>Artist:</b> {agency}'
                   '\n<b>Open date:</b> {date_open}'
                   '\n<b>Date of birth:</b> {birth}'
                   '\n<b>Debtor:</b> {debtors}'
                   '\n<b>ASVP number:</b> {number}'
                   '\n<b>Status:</b> {status}',
        'text_ua': '<b>Стягувач:</b> {creditors_name}'
                   '\n<b>Виконавець:</b> {agency}'
                   '\n<b>Дата відкриття:</b> {date_open}'
                   '\n<b>Дата народження:</b> {birth}'
                   '\n<b>Боржник:</b> {debtors}'
                   '\n<b>АСВП номер:</b> {number}'
                   '\n<b>Статус:</b> {status}',
        'buttons': [
            {
                'text': 'Подписаться',
                'text_en': 'Subscribe',
                'text_ua': 'Підписатися',
                'row': 0,
                'callback_data': 'subs#{asvp_id}'
            },
            {
                'text': 'Отписаться',
                'text_en': 'Unsubscribe',
                'text_ua': 'Відписатися',
                'row': 0,
                'callback_data': 'asvp_u#{subs_id}'
            },
            {
                'text': 'Показать еще',
                'text_en': 'Show more',
                'text_ua': 'Показати ще',
                'row': 1,
                'callback_data': 'next#{page}'
            }
        ]
    },
    'SubscribeAsvp': {
        'text': 'Подписка на поиск в автоматизированной системе'
                ' исполнительного производства оформлена!'
                '\n\nКогда будут новые события - мы сообщим вас',
        'text_en': 'Subscribe to the search in the automated executive'
                   ' production system is decorated!'
                   '\n\nWhen there are new events - we will notify you',
        'text_ua': 'Підписка на пошук в автоматизованій системі виконавчого'
                   ' провадження оформлена!'
                   '\n\nКоли будуть нові події - ми повідомимо вас'
    },
    'CrossingTheBorder': {
        'text': 'В этом меню собрана информация о правилах и процедурах '
                'пересечения границы 🛂, а также особенностях таможенного '
                'законодательства Украины 🛄. Для этого, а также чтобы '
                'узнаете, как действовать в случае депортации ⛔️ и запрета '
                'на въезд в Украину ❗️ воспользуйтесь кнопками ниже 👇',
        'text_en': 'This menu contains information about the rules and '
                   'procedures of the border crossing 🛂, as well as the '
                   'specifics of Ukrainian legislation 🛄. For someone else, '
                   'and also to know how to get deported ⛔️ that fence on '
                   'the way to Ukraine ❗️ speed up with the buttons below 👇',
        'text_ua': 'В этом меню зібрана інформація о правилах та процедуры '
                   'перетину кордону 🛂, а так же особливості митного '
                   'законодавства України 🛄. Для этого, а також щоб узнать как '
                   'діяти у випадку депортации ⛔️ и заборони на в\'їзд в '
                   'Україну ❗️ скористайтесь кнопками нижче 👇',
        'buttons': [
            {
                'text': '🛄 Правила таможенного контроля',
                'text_en': '🛄 Customs control rules',
                'text_ua': '🛄 Правила митного контролю',
                'row': 0,
                'url': 'https://telegra.ph/Pravila-tamozhennogo-kontrolya'
                       '-rus-09-23',
                'url_en': 'https://telegra.ph/Pravila-tamozhennogo-kontrolya'
                          '-angl-09-23',
                'url_ua': 'https://telegra.ph/Pravila-tamozhennogo-kontrolya'
                          '-ukr-09-23'
            },
            {
                'text': '🛂 Правила пограничного контроля',
                'text_en': '🛂 Border control rules',
                'text_ua': '🛂 Правила прикордонного контролю',
                'row': 1,
                'url': 'https://telegra.ph/Pravila-pogranichnogo-kontrolya'
                       '-rus-09-23',
                'url_en': 'https://telegra.ph/Pravila-pogranichnogo'
                          '-kontrolya-angl-09-23',
                'url_ua': 'https://telegra.ph/Pravila-pogranichnogo'
                          '-kontrolya-ukr-09-23'
            },
            {
                'text': '⛔️ Запрет на въезд в Украину',
                'text_en': '⛔️ Prohibition on entry into Ukraine',
                'text_ua': '⛔️ Заборона на в\'їзд в Україну',
                'row': 2,
                'url': 'https://telegra.ph/Zapret-na-vezd-v-Ukrainu-rus-09-23',
                'url_en': 'https://telegra.ph/Zapret-na-vezd-v-Ukrainu-angl'
                          '-09-23',
                'url_ua': 'https://telegra.ph/Zapret-na-vezd-v-Ukrainu-ukr'
                          '-09-23'
            },
            {
                'text': '❗️ Депортация из Украины',
                'text_en': '❗️ Deportation from Ukraine',
                'text_ua': '❗️ Депортація з України',
                'row': 3,
                'url': 'https://telegra.ph/Deportaciya-iz-Ukrainy-rus-09-23',
                'url_en': 'https://telegra.ph/Deportaciya-iz-Ukrainy-angl-09'
                          '-23',
                'url_ua': 'https://telegra.ph/Deportaciya-iz-Ukrainy-ukr-09-23'
            },
            {
                'text': 'Меню',
                'text_en': 'Menu',
                'text_ua': 'Меню',
                'row': 4,
                'callback_data': 'menu'
            },
        ]
    },
    'CancelSubs': {
        'text': 'Вы прекратили платную подписку.'
                '\n\nДата окончания пользования дополнительными функциями '
                'бота {date}',
        'text_en': 'You have terminated your paid subscription.'
                   '\n\nEnd date for using additional bot features {date}',
        'text_ua': 'Ви припинили платну підписку.'
                   '\n\nДата завершення користування додатковими функціями '
                   'робота {date}',
        'buttons': [
            {
                'text': '⬅️ Назад',
                'text_en': '⬅️ Back',
                'text_ua': '⬅️ Повернутися',
                'row': 1,
                'callback_data': 'profile_back'
            }
        ]
    },
    'PaymentResub': {
        'text': 'Статус вашего аккаунта "Продвинутый"'
                '\n\nВы можете использовать дополнительные функции бота.'
                '\nДата действия подписки {date_pay}',
        'text_en': 'Your Advanced Account Status'
                   '\n\nYou can use additional features of the bot.'
                   '\n\nSubscription validity date {date_pay}',
        'text_ua': 'Статус вашого облікового запису "Просунутий"'
                   '\n\nВи можете користуватися додатковими функціями бота.'
                   '\n\nДата дії передплати {date_pay}',
        'buttons': [
            {
                'text': 'Продолжить с помощью “LiqPay“',
                'text_en': 'Continue with “LiqPay“',
                'text_ua': 'Продовжити за допомогою “LiqPay“',
                'row': 0,
                'url': '{liq_url}',
                'url_en': '{liq_url}',
                'url_ua': '{liq_url}'
            },
            {
                'text': 'Продолжить с помощью “PortMone“',
                'text_en': 'Continue with “PortMone“',
                'text_ua': 'Продовжити за допомогою “PortMone“',
                'row': 1,
                'url': '{port_url}',
                'url_en': '{port_url}',
                'url_ua': '{port_url}'
            },
            {
                'text': '⬅️ Назад',
                'text_en': '⬅️ Back',
                'text_ua': '⬅️ Повернутися',
                'row': 2,
                'callback_data': '{back_callback}'
            },
            {
                'text': 'Меню',
                'text_en': 'Menu',
                'text_ua': 'Меню',
                'row': 2,
                'callback_data': 'menu'
            }
        ]
    },
    'MySubscribe': {
        'text': 'У вас {count} подписок:',
        'text_en': 'You have {count} subscriptions:',
        'text_ua': 'У вас {count} підписок:',
        'buttons': [
            {
                'text': 'Меню',
                'text_en': 'Menu',
                'text_ua': 'Меню',
                'row': 0,
                'reply': True
            }
        ]
    },
    'FinesSub': {
        'text': 'Штрафы по Авто с № {car_number}'
                '\nПоследний:'
                '\n<b>#️⃣Номер постановления:</b> {resolution}'
                '\n<b>📅Дата нарушения:</b> {date}'
                '\n<b>💳Сумма штрафа:</b> {value}грн'
                ' {payment}',
        'text_en': 'Penalties for Cars with № {car_number}'
                   '\nLast:'
                   '\n<b>#️⃣Resolution number:</b> {resolution}'
                   '\n<b>📅Violation date:</b> {date}'
                   '\n<b>💳Fine amount:</b> {value}UAH'
                   ' {payment}',
        'text_ua': 'Штрафи по Авто з №{car_number}'
                   '\nОстанній:'
                   '\n<b>#️⃣Номер постанови:</b> {resolution}'
                   '\n<b>📅Дата порушення:</b> {date}'
                   '\n<b>💳Сума штрафу:</b> {value}грн'
                   ' {payment}',
        'buttons': [
            {
                'text': 'Отписаться',
                'text_en': 'Unsubscribe',
                'text_ua': 'Відписатися',
                'row': 0,
                'callback_data': 'bdr_u#{subs_id}'
            },
            {
                'text': 'Просмотреть',
                'text_en': 'View',
                'text_ua': 'Переглянути',
                'row': 1,
                'callback_data': 'bdr_v#{subs_id}'
            }
        ]
    },
    'DepartSub': {
        'text': '{text}',
        'text_en': '{text}',
        'text_ua': '{text}',
        'buttons': [
            {
                'text': 'Отписаться',
                'text_en': 'Unsubscribe',
                'text_ua': 'Відписатися',
                'row': 0,
                'callback_data': 'depart_u#{subs_id}'
            }
        ]
    },
    'DocsSub': {
        'text': 'Проверка готовности {doc_type} на основе {doc_for} {number}'
                '\nРезультат: {status}',
        'text_en': '{doc_type} readiness check based on {doc_for} {number}'
                   '\nResult: {status}',
        'text_ua': 'Перевірка готовності {doc_type} на основі {doc_for}'
                   ' {number}'
                   '\nРезультат: {status}',
        'buttons': [
            {
                'text': 'Отписаться',
                'text_en': 'Unsubscribe',
                'text_ua': 'Відписатися',
                'row': 0,
                'callback_data': 'doc_u#{subs_id}'
            }
        ]
    },
    'InactiveSub': {
        'text': 'Проверка недействительного документа "{doc_type}" {number}'
                '\nРезультат: {status}',
        'text_en': 'Check for invalid document "{doc_type}" {number}'
                   '\nResult: {status}',
        'text_ua': 'Перевірка недійсного документа "{doc_type}" {number}'
                   '\nРезультат: {status}',
        'buttons': [
            {
                'text': 'Отписаться',
                'text_en': 'Unsubscribe',
                'text_ua': 'Відписатися',
                'row': 0,
                'callback_data': 'idoc_u#{subs_id}'
            }
        ]
    },
    'MvsSub': {
        'text': 'Проверка реестра министерства внутренних дел по запросу "{full_name}"',
        'text_en': 'Checking the registry of the Ministry of the Interior upon request "{full_name}"',
        'text_ua': 'Перевірка реєстру міністерства внутрішніх справ на запит "{full_name}"',
        'buttons': [
            {
                'text': 'Отписаться',
                'text_en': 'Unsubscribe',
                'text_ua': 'Відписатися',
                'row': 0,
                'callback_data': 'mvs_u#{subs_id}'
            },
            {
                'text': 'Просмотреть',
                'text_en': 'View',
                'text_ua': 'Переглянути',
                'row': 1,
                'callback_data': 'mvs_v#{subs_id}'
            }
        ]
    },
    'CourtSub': {
        'text': 'Проверка в реестре судебных решений по делу "{number}"',
        'text_en': 'Checking the register of court decisions in the case '
                   '"{number}"',
        'text_ua': 'Перевірка у реєстрі судових рішень на делу "{number}"',
        'buttons': [
            {
                'text': 'Отписаться',
                'text_en': 'Unsubscribe',
                'text_ua': 'Відписатися',
                'row': 0,
                'callback_data': 'court_u#{subs_id}'
            },
            {
                'text': 'Просмотреть',
                'text_en': 'View',
                'text_ua': 'Переглянути',
                'row': 1,
                'callback_data': 'court_v#{subs_id}'
            }
        ]
    },
    'AsvpSub': {
        'text': 'Проверка в cистемe автоматизированного производства ВП Номер {number}',
        'text_en': 'Check in the automated production systemo VP Number {number}',
        'text_ua': 'Перевірка в системі автоматизованого виробництва ВП Номер {number}',
        'buttons': [
            {
                'text': 'Отписаться',
                'text_en': 'Unsubscribe',
                'text_ua': 'Відписатися',
                'row': 0,
                'callback_data': 'asvp_u#{subs_id}'
            },
            {
                'text': 'Просмотреть',
                'text_en': 'View',
                'text_ua': 'Переглянути',
                'row': 1,
                'callback_data': 'asvp_v#{subs_id}'
            }
        ]
    },
    'FinesUnSubscribe': {
        'text': 'Вы отписались на поиск штрафов по номеру "{car_number}"',
        'text_en': 'Search for fines by number "{car_number}" Unsubscribed!',
        'text_ua': 'Ви відписалися на пошук штрафів за номером "{car_number}"'
    },
    'DepartUnSubs': {
        'text': 'Подписка на расчет дней отменена!',
        'text_en': 'The subscription to the calculation of days has been '
                   'canceled!',
        'text_ua': 'Підписку на розрахунок днів скасовано!'
    },
    'DocUnSubs': {
        'text': 'Подписка на проверку готовности документа отменена!',
        'text_en': 'Subscription to document readiness check has been '
                   'cancelled!',
        'text_ua': 'Підписку на перевірку готовності документа скасовано!'
    },
    'InactiveUnSubs': {
        'text': 'Подписка на проверку недействительного документа отменена!',
        'text_en': 'The subscription to check an invalid document has been '
                   'cancelled!',
        'text_ua': 'Підписку на перевірку недійсного документа скасовано!'
    },
    'CourtUnSubs': {
        'text': 'Подписка на поиск в реестре судебных решений отменена!',
        'text_en': 'The subscription to the search in the register of '
                   'judgments has been cancelled!',
        'text_ua': 'Підписку на пошук у реєстрі судових рішень скасовано!'
    },
    'FopUnSubs': {
        'text': 'Подписка на поиск в реестре физических лиц-предпринимателей '
                'отменена!',
        'text_en': 'The subscription to the search in the register of '
                   'individual entrepreneurs has been cancelled!',
        'text_ua': 'Підписку на пошук у реєстрі фізичних осіб-підприємців '
                   'відмінено!'
    },
    'CompanyUnSubs': {
        'text': 'Подписка на поиск в реестре юридических лиц отменена!',
        'text_en': 'The subscription to the search in the register of legal '
                   'entities has been cancelled!',
        'text_ua': 'Підписку на пошук у реєстрі юридичних осіб скасовано!'
    },
    'MvsUnSubs': {
        'text': 'Подписка на поиск в реестре министерства внутренних дел '
                'отменена!',
        'text_en': 'The subscription to search in the register of the '
                   'Ministry of the Interior has been cancelled!',
        'text_ua': 'Підписку на пошук у реєстрі міністерства внутрішніх '
                   'справ скасовано!'
    },
    'AsvpUnSubs': {
        'text': 'Подписка на поиск в cистемe автоматизированного производства '
                'отменена!',
        'text_en': 'Subscription to search in the automated production '
                   'system has been cancelled!',
        'text_ua': 'Підписка на пошук у системі автоматизованого виробництва'
                   ' скасована!'
    },
    'DepartTwenty': {
        'text': '<b>Обращаем ваше внимание!</b>'
                '\nЧто у вас осталось 20 дней до превышения лимита '
                'пребывания на территории Украины.'
                '\nДля продления срока обратитесь в миграционную службу.',
        'text_en': '<b>Обращаем ваше внимание!</b>'
                   '\nЧто у вас осталось 20 дней до превышения лимита '
                   'пребывания на территории Украины.'
                   '\nДля продления срока обратитесь в миграционную службу.',
        'text_ua': '<b>Обращаем ваше внимание!</b>'
                   '\nЧто у вас осталось 20 дней до превышения лимита '
                   'пребывания на территории Украины.'
                   '\nДля продления срока обратитесь в миграционную службу.',
    },
    'DepartDeparture': {
        'text': '<b>Обращаем ваше внимание!</b>'
                '\nВы превысили лимит дней пребывания на территории Украины.'
                '\nРекомендуем обратиться в миграционную службу!',
        'text_en': '<b>Обращаем ваше внимание!</b>'
                   '\nВы превысили лимит дней пребывания на территории Украины.'
                   '\nРекомендуем обратиться в миграционную службу!',
        'text_ua': '<b>Обращаем ваше внимание!</b>'
                   '\nВы превысили лимит дней пребывания на территории Украины.'
                   '\nРекомендуем обратиться в миграционную службу!'
    }
}
