try:
    from . import (commands, monitoring, document, fine, news, chat, search,
                   support, profile, inline_calback, reply)
except Exception as e:
    from loguru import logger
    logger.error(e)