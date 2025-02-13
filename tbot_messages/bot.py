from loguru import logger
from telebot import TeleBot, logger as tbot_logger

from .models import TBot
from .utils import IsReplyButtonClick


class Bot(TeleBot):
    def __init__(self):
        try:
            self.config = TBot.objects.get(is_active=True)
            self.token = self.config.token

        except Exception as e:
            logger.error(e)
            self.config = None
            self.token = 'foo'

        super().__init__(self.token, parse_mode='HTML', threaded=False)


bot = Bot()
bot.add_custom_filter(IsReplyButtonClick())
